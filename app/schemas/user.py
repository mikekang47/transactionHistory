from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator
from starlette import status


class User(BaseModel):
    nick_name: str
    email: EmailStr


class UserCreate(User):
    password: str
    retype_password: str

    @validator('nick_name', 'email', 'password', 'retype_password')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="user information field must not be empty")
        return v

    @validator('retype_password')
    def password_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="password not match")
        return v


class UserResponse(User):
    class Config:
        orm_mod = True
