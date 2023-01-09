from datetime import datetime

from pydantic import BaseModel


class History(BaseModel):
    money: int
    detail: str


class HistoryCreate(History):
    pass


class HistoryUpdate(History):
    pass


class HistoryResponse(History):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
