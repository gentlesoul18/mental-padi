from pydantic import BaseModel

from user.schemas.users import UserData


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    email: str
    username: str

class Login(UserData):
    email: str
    password: str

    class Config:
        orm_mode = True