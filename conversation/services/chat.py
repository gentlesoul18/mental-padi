from typing import List
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from conversation.models.chat_sessions import ChatSession
from conversation.models.conversations import Conversation, MessageRole
from conversation.utils.groq import get_groq_response

async def create_chat_response(
    db: Session,
    user_id: uuid.UUID,
    message: str,
    chat_session_id: uuid.UUID = None
) -> dict:
    # Create new chat session if none exists
    if not chat_session_id:
        chat_session = ChatSession(user_id=user_id)
        db.add(chat_session)
        db.commit()
        chat_session_id = chat_session.id

    # Save user message
    user_message = Conversation(
        chat_session_id=chat_session_id,
        user_id=user_id,
        message=message,
        role=MessageRole.USER
    )
    db.add(user_message)
    
    # Get chat history for context
    chat_history = get_chat_history(db, chat_session_id)

    # add current message to chat history
    chat_history.append({"role": MessageRole.USER, "content": message})

    # Get AI response from Groq
    ai_response = await get_groq_response(message)
    
    # Save AI response
    assistant_message = Conversation(
        chat_session_id=chat_session_id,
        user_id=user_id,
        message=ai_response,
        role=MessageRole.ASSISTANT
    )
    db.add(assistant_message)
    db.commit()
    
    return {
        "chat_session_id": chat_session_id,
        "response": ai_response
    }

def get_chat_history(db: Session, chat_session_id: uuid.UUID) -> List[dict]:
    messages = db.query(Conversation)\
        .filter(Conversation.chat_session_id == chat_session_id)\
        .order_by(Conversation.created_at.asc())\
        .all()
    
    return [{"role": msg.role.value, "content": msg.message} for msg in messages]

async def get_session_chats(
    db: Session, 
    session_id: uuid.UUID, 
    user_id: uuid.UUID
) -> List[Conversation]:
    """Get all messages in a chat session"""
    return db.query(Conversation)\
        .filter(
            Conversation.chat_session_id == session_id,
            Conversation.user_id == user_id
        )\
        .order_by(Conversation.created_at.asc())\
        .all()

async def get_user_chat_history(
    db: Session, 
    user_id: uuid.UUID
) -> List[ChatSession]:
    """Get all chat sessions with their messages for a user"""
    return db.query(ChatSession)\
        .filter(ChatSession.user_id == user_id)\
        .order_by(ChatSession.created_at.desc())\
        .all()