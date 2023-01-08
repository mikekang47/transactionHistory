from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from error import security_exception
from user import user_application, user_schema
from util import jwt_util

router = APIRouter(
    prefix="/users",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/session/login")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserResponse)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_application.create_user(db=db, user_create=_user_create)
    return user_schema.UserResponse(nick_name=user.nick_name, email=user.email)


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    email = jwt_util.extract_email_from_token(token)
    user = user_application.get_user(db, email=email)

    if user.expire_time < datetime.utcnow() + timedelta(hours=9):
        raise security_exception.TokenTimeOutException()

    return user
