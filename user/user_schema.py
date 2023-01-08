from pydantic import BaseModel, validator, EmailStr

from error import requests_exception


class UserCreate(BaseModel):
    nick_name: str
    email: EmailStr
    password: str
    retype_password: str

    @validator('nick_name', 'email', 'password', 'retype_password')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise requests_exception.EmptyFieldException()
        return v

    @validator('retype_password')
    def password_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise requests_exception.PasswordNotMatchException()
        return v


class UserResponse(BaseModel):
    nick_name: str
    email: str

    class Config:
        orm_mode = True
