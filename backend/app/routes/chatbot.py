# app/routes/chatbot.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.chatbot_schemas import (
    ChatRequest, 
    ChatResponse, 
    NewChatSession,
    NewChatSessionResponse,
    ChatHistoryResponse,
    TitleUpdateResponse
)
from app.services.chatbot_handler import (
    chat_inference_handler,
    create_chat_session_handler,
    chat_history_handler,
    title_update_handler, 
    delete_chat_session_handler,
    delete_all_sessions_handler
)
from app.utils.unique_id_generation import generate_unique_chat_session_id
from app.utils.oauth import get_current_user

router = APIRouter()

@router.post("", response_model=NewChatSessionResponse, status_code=status.HTTP_201_CREATED, summary="Create New Chat Session")
async def create_chat_session(
    title: NewChatSession,
    current_user = Depends(get_current_user)
):
    title = title.title or generate_unique_chat_session_id()
    return await create_chat_session_handler(title, current_user["user_id"])

# Chat Inference
@router.post("/inference/{session_id}", response_model=ChatResponse, status_code=status.HTTP_200_OK, summary="Get Chatbot Inference")
async def chat_inference(
    session_id: str,
    input_data: ChatRequest,
    current_user = Depends(get_current_user)
):
    return await chat_inference_handler(session_id, current_user["user_id"], input_data)


@router.get("/history/{session_id}", response_model=ChatHistoryResponse, status_code=status.HTTP_200_OK, summary="Fetch Chat History")
async def fetch_chat_history(
    session_id: str,
    current_user = Depends(get_current_user)
):
    return await chat_history_handler(session_id, current_user["user_id"])


@router.patch("/title/{session_id}", response_model=TitleUpdateResponse, status_code=status.HTTP_200_OK, summary="Update Chat Session Title")
async def update_chat_title(
    session_id: str,
    new_title: NewChatSession,
    current_user = Depends(get_current_user)
):
    return await title_update_handler(session_id, current_user["user_id"], new_title)

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Chat Session")
async def delete_chat_session(
    session_id: str,
    current_user = Depends(get_current_user)
):
    await delete_chat_session_handler(session_id, current_user["user_id"])
    
@router.delete("", status_code=status.HTTP_204_NO_CONTENT, summary="Delete All Chat Sessions")
async def delete_all_chat_sessions(
    current_user = Depends(get_current_user)
):
    await delete_all_sessions_handler(current_user["user_id"])
