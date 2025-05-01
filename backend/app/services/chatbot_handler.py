# app/services/chatbot_handler.py

from app.schemas.chatbot_schemas import (
    ChatRequest, 
    ChatResponse, 
    NewChatSession,
    NewChatSessionResponse,
    ChatHistoryResponse,
    TitleUpdateResponse
)
from app.services.chatbot_service import ChatbotService

async def chat_inference_handler(session_id: str, user_id: str, input_data: ChatRequest)->ChatResponse:
    service = ChatbotService()
    user_input = input_data.user_input 
    
    return await service.chat_inference(session_id, user_id, user_input)


async def create_chat_session_handler(title: NewChatSession, user_id: str)-> NewChatSessionResponse:
    service = ChatbotService()
    
    return await service.create_session(title, user_id)

async def chat_history_handler(session_id: str, user_id: str)-> ChatHistoryResponse:
    service = ChatbotService()
    
    return await service.get_chat_history(session_id, user_id)

async def title_update_handler(session_id: str, user_id: str, new_title: NewChatSession) -> TitleUpdateResponse:
    service = ChatbotService()
    
    return await service.update_chat_title(session_id, user_id, new_title.title)

async def delete_chat_session_handler(session_id: str, user_id: str):
    service = ChatbotService()
    
    return await service.delete_chat_session(session_id, user_id)

async def delete_all_sessions_handler(user_id: str):
    service = ChatbotService()
    
    return await service.delete_all_sessions(user_id)
