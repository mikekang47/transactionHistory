from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from user import user_application, user_schema

router = APIRouter(
    prefix="/users",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/session/login")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserResponse)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_application.create_user(db=db, user_create=_user_create)
    return user_schema.UserResponse(nick_name=user.nick_name, email=user.email)
