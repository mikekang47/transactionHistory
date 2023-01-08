from datetime import datetime

from pydantic import BaseModel


class RefreshToken(BaseModel):
    _token: str
    token_type: str
    expire_date: datetime
    email: str

    @property
    def get_token(self):
        return self._token

    class Config:
        orm_mode = True


class AccessToken(BaseModel):
    _token: str
    token_type: str
    email: str
    expire_date: datetime

    @property
    def get_token(self):
        return self._token

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken

    @property
    def get_access_token(self):
        return self.access_token.get_token

    @property
    def get_refresh_token(self):
        return self.refresh_token.get_token

    class Config:
        orm_mode = True
