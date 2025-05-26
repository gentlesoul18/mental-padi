from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.database import get_db
from typing import Optional
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

from auth.utils.auth_utils import get_hashed_password
from user.models.users import User
from user.schemas.users import RegisterUser

def create_user(db: Session, user: dict):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (RegisterUser): The user data to create.

    Returns:
        User: The created user object.
    """
    db_user = User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        password=get_hashed_password(user.password),
        is_active=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_email(db: Session, email: str):
    """
    Get a user by email.

    Args:
        db (Session): The database session.
        email (str): The email of the user to retrieve.

    Returns:
        User: The user object if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, 
            os.getenv("SECRET_KEY"), 
            algorithms=[os.getenv("ALGORITHM")]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
        
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
        
    return user