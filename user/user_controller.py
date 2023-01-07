from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

import jwt_config
from database import get_db
from user import user_application, user_schema

router = APIRouter(
    prefix="/users",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserResponse)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_application.create_user(db=db, user_create=_user_create)
    return user_schema.UserResponse(nick_name=user.nick_name, email=user.email)


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_config.getSecretKey(), algorithms=[jwt_config.getAlgorithm()])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_application.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
