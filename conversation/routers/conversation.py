from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from conversation.schemas.conversation import ChatMessageResponse, ChatSessionResponse
from conversation.services.chat import create_chat_response, get_session_chats, get_user_chat_history
from conversation.schemas import ChatRequest, ChatResponse
from core.database import get_db
from user.models.users import User
from user.services.user_services import get_current_user

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@chat_router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    response = await create_chat_response(
        db=db,
        user_id=current_user.id,
        message=request.message,
        chat_session_id=request.chat_session_id
    )
    return response

@chat_router.get("/session/{session_id}", response_model=List[ChatMessageResponse])
async def get_chat_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all messages in a specific chat session"""
    messages = await get_session_chats(db, session_id, current_user.id)
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    return messages

@chat_router.get("/history", response_model=List[ChatSessionResponse])
async def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all chat sessions for the current user"""
    return await get_user_chat_history(db, current_user.id)