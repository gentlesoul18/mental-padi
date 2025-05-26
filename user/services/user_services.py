from sqlalchemy.orm import Session

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