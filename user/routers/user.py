from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.utils.send_email import send_mail
from core.database import get_db
from user.schemas.users import RegisterUser
from user.services.user_services import create_user


user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.post("/register")
async def register_user(form_data: RegisterUser, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    """
    new_user = create_user(db, form_data)
    if not new_user:
        return {"message": "User already exists"}

    # send mail
    mail_sent = send_mail(email= new_user.email, subject= "Confirm Your Mail",fullName= new_user.full_name, confirmation_link= "mylink", template_path= "confirm_email.html")
    if not mail_sent:
        raise HTTPException(status_code=500, detail="Failed to send email")
    return {"message": "User registered successfully"}