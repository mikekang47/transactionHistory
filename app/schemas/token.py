from datetime import datetime

from pydantic import BaseModel


class RefreshToken(BaseModel):
    token: str
    token_type: str
    email: str
    expire_date: datetime

    @property
    def get_token(self):
        return self.token

    class Config:
        orm_mode = True


class AccessToken(BaseModel):
    token: str
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
