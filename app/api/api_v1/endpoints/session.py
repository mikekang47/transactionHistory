from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.api.api_v1.deps import get_current_user
from app.models import User
from app.schemas.token import Token
from database import get_db

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
        db: Session = Depends(get_db),
        login_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.user.authenticate(db, email=login_data.username, password=login_data.password)
    return crud.session.create_session(db, user=user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)) -> Any:
    crud.session.delete_session(db, current_user=current_user)


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token)
def get_access_token(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)) -> Any:
    return crud.session.get_access_token(db, current_user=current_user)
