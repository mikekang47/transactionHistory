from datetime import datetime

from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str
    expire_date: datetime
    email: str

    class Config:
        orm_mode = True


class AccessToken(BaseModel):
    access_token: str
    token_type: str
    email: str
    expire_date: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken

    class Config:
        orm_mode = True
