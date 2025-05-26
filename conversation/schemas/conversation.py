from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    chat_session_id: Optional[UUID] = None

class ChatResponse(BaseModel):
    chat_session_id: UUID
    response: str

class ChatMessageResponse(BaseModel):
    id: UUID
    message: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: UUID
    created_at: datetime
    messages: List[ChatMessageResponse]

    class Config:
        from_attributes = True