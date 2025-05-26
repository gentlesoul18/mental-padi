import os
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime

from auth.schemas.login import Login
from auth.utils.auth_utils import verify_password
from core.database import get_db
from user.services.user_services import get_user_by_email

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "/api/auth/login")

def authenticate_user(email: str, password: str, db: Session  = Depends(get_db)):
    """
    Authenticate a user and return the user object.

    Args:
        db: The database session.
        user (Login): The user data to authenticate.

    Returns:
        User: The authenticated user object.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    
    return user

def create_access_token(data: dict, expires_delta: int = None):
    """
    Create an access token for the user.

    Args:
        data (dict): The user data to include in the token.
        expires_delta (int, optional): The expiration time for the token. Defaults to None.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": int(expire.timestamp())}) 
        # to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def confirm_email(email: str, db: Session = Depends(get_db)):
    """
    Verify if the email exists in the database.

    Args:
        email (str): The email to verify.
        db (Session): The database session.

    Returns:
        bool: True if the email exists, False otherwise.
    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    
    user.is_active = True
    db.commit()
    return user