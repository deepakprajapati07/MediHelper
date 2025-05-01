# app/services/chatbot_service.py

from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.utils.unique_id_generation import generate_unique_chat_session_id
from app.utils.helper import format_dialogue
from app.config import settings
from app.database.mongo import chatbot_session_collection, chatbot_history_collection
from app.schemas.chatbot_schemas import (
    ChatResponse,
    NewChatSessionResponse,
    ChatHistoryResponse,
    TitleUpdateResponse
)
from app.services.chatbot_utils import ChatModelService, ChatContextService


class ChatbotService:
    def __init__(self):
        self.model_service = ChatModelService()
        self.context_service = ChatContextService()

    async def chat_inference(self, session_id: str, user_id: str, user_input: str) -> ChatResponse:
        await self._verify_session(session_id, user_id)
        context = await self._build_context(user_input, session_id, user_id)
        assistant_reply = await self._get_response(context, user_input)
        await self._store_message(session_id, user_id, user_input, assistant_reply)

        return ChatResponse(response=assistant_reply)

    async def create_session(self, title: str, user_id: str) -> NewChatSessionResponse:
        session_id = generate_unique_chat_session_id()
        now = datetime.now(timezone.utc)

        chatbot_session_collection.insert_one({
            "session_id": session_id,
            "user_id": user_id,
            "title": title,
            "created_at": now,
            "updated_at": now,
            "is_deleted": False
        })

        return NewChatSessionResponse(
            session_id=session_id,
            user_id=user_id,
            title=title,
            created_at=now
        )

    async def get_chat_history(self, session_id: str, user_id: str) -> ChatHistoryResponse:
        session = chatbot_session_collection.find_one({
            "session_id": session_id,
            "user_id": user_id,
            "is_deleted": False
        })
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        history_doc = chatbot_history_collection.find_one({
            "session_id": session_id,
            "user_id": user_id
        })

        messages = history_doc.get("conversation", []) if history_doc else []

        return ChatHistoryResponse(
            session_id=session_id,
            user_id=user_id,
            title=session["title"],
            created_at=session["created_at"],
            messages=messages
        )

    async def update_chat_title(self, session_id: str, user_id: str, new_title: str) -> TitleUpdateResponse:
        session = chatbot_session_collection.find_one({
            "session_id": session_id,
            "user_id": user_id,
            "is_deleted": False
        })
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        updated_at = datetime.now(timezone.utc)

        chatbot_session_collection.update_one(
            {"session_id": session_id, "user_id": user_id},
            {"$set": {"title": new_title, "updated_at": updated_at}}
        )

        return TitleUpdateResponse(
            session_id=session_id,
            user_id=user_id,
            title=new_title,
            updated_at=updated_at
        )

    async def delete_chat_session(self, session_id: str, user_id: str):
        result = chatbot_session_collection.update_one(
            {"session_id": session_id, "user_id": user_id, "is_deleted": False},
            {"$set": {"is_deleted": True, "updated_at": datetime.now(timezone.utc)}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Chat session not found")

    async def delete_all_sessions(self, user_id: str):
        chatbot_session_collection.update_many(
            {"user_id": user_id, "is_deleted": False},
            {"$set": {"is_deleted": True, "updated_at": datetime.now(timezone.utc)}}
        )

    # --- Internal Helpers ---

    async def _verify_session(self, session_id: str, user_id: str):
        session = chatbot_session_collection.find_one({
            "session_id": session_id,
            "user_id": user_id,
            "is_deleted": False
        })
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")

    async def _build_context(self, user_input: str, session_id: str, user_id: str) -> str:
        history_doc = chatbot_history_collection.find_one({
            "session_id": session_id,
            "user_id": user_id
        })

        messages = history_doc.get("conversation", []) if history_doc else []
        recent_history = format_dialogue(messages[-settings.memory_limit:]) if messages else ""
        retrieved_context = self.context_service.retrieve(user_input)

        return f"{recent_history}\n\n{retrieved_context}"

    async def _get_response(self, context: str, user_input: str) -> str:
        try:
            return self.model_service.generate_response(settings.llm_model_1, context, user_input).content.strip()
        except Exception as primary_error:
            try:
                return self.model_service.generate_response(settings.llm_model_2, context, user_input).content.strip()
            except Exception as fallback_error:
                raise HTTPException(
                    status_code=500,
                    detail=f"Model errors: {str(primary_error)} | {str(fallback_error)}"
                )

    async def _store_message(self, session_id: str, user_id: str, user_input: str, assistant_reply: str):
        now = datetime.now(timezone.utc)
        chatbot_history_collection.update_one(
            {"session_id": session_id, "user_id": user_id},
            {
                "$push": {
                    "conversation": {
                        "user": user_input,
                        "assistant": assistant_reply,
                        "timestamp": now
                    }
                },
                "$setOnInsert": {
                    "created_at": now
                }
            },
            upsert=True
        )

