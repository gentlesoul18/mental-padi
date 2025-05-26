import uuid
from core.database import Base
from sqlalchemy import Column, UUID, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    
    # Relationships
    messages = relationship("Conversation", back_populates="chat_session")
    user = relationship("User", back_populates="chat_sessions")