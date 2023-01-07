from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    nick_name: str
    expire_time: datetime

    class Config:
        orm_mode = True
