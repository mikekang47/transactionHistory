from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_user
from app.schemas import UserResponse
from database import get_db

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_requests: schemas.UserCreate
) -> Any:
    user = crud_user.user.create_user(db, user_create=user_requests)
    return UserResponse(nick_name=user.nick_name, email=user.email)
