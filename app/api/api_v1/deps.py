from datetime import datetime
from datetime import timedelta
from typing import Optional, Callable

from fastapi import HTTPException, Depends, Security, requests
from fastapi.security import APIKeyHeader
from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.core.config import settings
from app.core.session import SessionLocal
from app.models.user import User

HEADER_KEY = "Authorization"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class GetAPIKeyHeader(APIKeyHeader):
    async def __call__(
            self,
            request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except HTTPException:
            return None


def get_current_user_authorizer(
        *,
        required: bool = False
) -> Callable:
    return get_current_user if required else get_current_user_optional


def get_authorization_header_retriever(
        *,
        required: bool = False
) -> Callable:
    return get_authorization_header if required else get_authorization_header_optional


def get_authorization_header(
        api_key: str = Security(GetAPIKeyHeader(name=HEADER_KEY))
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unknown Header")
    if token_prefix != settings.TOKEN_PREFIX:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unknown Header")
    return token


async def get_authorization_header_optional(
        api_key: str = Security(GetAPIKeyHeader(name=HEADER_KEY)),
) -> str:
    if api_key:
        return get_authorization_header(api_key)
    return ""


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(get_authorization_header_retriever()),
) -> User:
    email = extract_email_from_token(token)
    user = crud.user.get_user_by_email(db, email=email)

    if user.expire_time < datetime.utcnow() + timedelta(hours=9):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token time out",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


async def get_current_user_optional(
        db: Session = Depends(get_db),
        token: str = Depends(get_authorization_header_retriever(required=False)),
) -> Optional[User]:
    if token:
        return await get_current_user(db, token)
    return None


def extract_email_from_token(token):
    payload = __verify_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token invalid",
                            headers={"WWW-Authenticate": "Bearer"})
    return email


def __verify_token(token):
    try:
        return jwt.decode(token, key=settings.SECRET_KEY,
                          algorithms=[settings.ALGORITHM])
    except JWTClaimsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token time out",
                            headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
