from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, validator
from starlette import status


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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="money must be greater than 0")
        return v

    @validator('detail')
    def is_empty(cls, v: str):
        if not v or not v.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="detail must not be empty")
        return v
