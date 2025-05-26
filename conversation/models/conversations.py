import uuid
import enum
from core.database import Base
from sqlalchemy import Column, String, Boolean, UUID, TIMESTAMP, text, ForeignKey, Enum
from sqlalchemy.orm import relationship

class MessageRole(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

    # Relationships
    user = relationship("User", back_populates="conversations")
    chat_session = relationship("ChatSession", back_populates="messages")