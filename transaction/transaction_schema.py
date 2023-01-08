from datetime import datetime

from pydantic import BaseModel


class HistoryResponse(BaseModel):
    id: int
    money: int
    detail: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
