# app/schemas/chatbot_schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NewChatSession(BaseModel):
    title: Optional[str] = None

class NewChatSessionResponse(BaseModel):
    title: str
    session_id: str
    user_id: str
    created_at: datetime
    
class TitleUpdateResponse(BaseModel):
    title: str
    session_id: str
    user_id: str
    updated_at: datetime

class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    response: str
    
class MessageEntry(BaseModel):
    user: str
    assistant: str
    timestamp: datetime

class ChatHistoryResponse(BaseModel):
    session_id: str
    user_id: str
    title: str
    created_at: datetime
    messages: List[MessageEntry]


