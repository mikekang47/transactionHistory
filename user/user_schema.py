from pydantic import BaseModel, validator, EmailStr


class UserCreate(BaseModel):
    nick_name: str
    email: EmailStr
    password: str
    retype_password: str

    @validator('nick_name', 'email', 'password', 'retype_password')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('must not be empty')
        return v

    @validator('retype_password')
    def password_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserResponse(BaseModel):
    nick_name: str
    email: str

    class Config:
        orm_mode = True
