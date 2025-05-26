from datetime import timedelta
from tempfile import template
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.schemas.login import Login
from auth.schemas.token import Token
from auth.services.auth import authenticate_user, confirm_email, create_access_token
from auth.utils.send_email import send_mail
from core.database import get_db


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/login")
async def login(
    form_data: Login,
    db: Session = Depends(get_db)
):
    """
    Login endpoint for user authentication.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the user's credentials.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    # Authenticate user
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Create access token
    access_token_expires = timedelta(minutes=5000)
    access_token = create_access_token(data={"email": user.email, "username": user.username, "full_name":user.full_name},expires_delta=access_token_expires)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in= 5000 # Set the expiration time as needed
    )

@auth_router.patch("/verify-email")
async def verify_email(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Verify the user's email.

    Args:
        email (str): The email of the user to verify.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the verification status.
    """
    # Implement your email verification logic here
    user = confirm_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")
    
    # If the email is found, you can proceed with the verification proces

    # Create access token
    access_token_expires = timedelta(minutes=5000)
    access_token = create_access_token(data={"email": user.email, "username": user.username, "full_name":user.full_name},expires_delta=access_token_expires)
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in= 5000 # Set the expiration time as needed
    )