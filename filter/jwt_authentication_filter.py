from datetime import datetime
from datetime import timedelta
from typing import Optional, Callable

from fastapi import HTTPException, Depends, Security, requests
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from database import get_db
from error import security_exception
from jwt_config import JwtConfig, get_jwt_config
from user import user_application
from user.user_model import User
from util.jwt_util import extract_email_from_token

HEADER_KEY = "Authorization"


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
        api_key: str = Security(GetAPIKeyHeader(name=HEADER_KEY)),
        jwt_config: JwtConfig = Depends(get_jwt_config),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise security_exception.UnknownHeaderException()
    if token_prefix != jwt_config.get_token_prefix():
        raise security_exception.UnknownHeaderException()
    return token


async def get_authorization_header_optional(
        api_key: str = Security(GetAPIKeyHeader(name=HEADER_KEY)),
        jwt_config: JwtConfig = Depends(get_jwt_config),
) -> str:
    if api_key:
        return get_authorization_header(api_key, jwt_config)
    return ""


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(get_authorization_header_retriever()),
) -> User:
    email = extract_email_from_token(token)
    user = user_application.get_user(db, email)

    if user.expire_time < datetime.utcnow() + timedelta(hours=9):
        raise security_exception.TokenTimeOutException()
    return user


async def get_current_user_optional(
        db: Session = Depends(get_db),
        token: str = Depends(get_authorization_header_retriever(required=False)),
) -> Optional[User]:
    if token:
        return await get_current_user(db, token)
    return None
