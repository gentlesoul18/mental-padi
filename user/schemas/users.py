from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class RegisterUser(UserData):

    class Config:
        orm_mode = True

