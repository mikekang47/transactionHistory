from datetime import datetime

from pydantic import BaseModel, validator


# TODO
# HTTP error로 변경하기

class HistoryResponse(BaseModel):
    id: int
    money: int
    detail: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class HistoryRequest(BaseModel):
    money: int
    detail: str

    @validator('money')
    def is_lower_than_zero(cls, v: int):
        if v < 0:
            raise ValueError('must be greater than zero')
        return v

    @validator('detail')
    def is_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError('must not be empty')
        return v
