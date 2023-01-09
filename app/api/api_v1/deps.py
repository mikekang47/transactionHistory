from datetime import datetime, timedelta
from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTClaimsError, ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.core.cofig import settings
from app.models import User
from database import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session(get_db),
        token: str = Depends(reusable_oauth2)
) -> User:
    email = extract_email_from_token(token)

    user = crud.user.get_user_by_email(db, email)

    if user.expire_time < datetime.utcnow() + timedelta(hours=9):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token time out",
                            headers={"WWW-Authenticate": "Bearer"})

    return user


def extract_email_from_token(token):
    payload = __verify_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return email


def __verify_token(token):
    try:
        return jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTClaimsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token invalid",
                            headers={"WWW-Authenticate": "Bearer"})
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token time out",
                            headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
