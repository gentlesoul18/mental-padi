import uuid
from core.database import Base
from sqlalchemy import Column, String, Boolean, UUID, TIMESTAMP,text

class User(Base):

    __tablename__ = "users"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

