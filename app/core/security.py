from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.token import AccessToken, RefreshToken, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
        subject: str) -> tuple[str, datetime]:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject)}

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, expire


def create_refresh_token(
        subject: str) -> tuple[str, datetime]:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject)}

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, expire


def create_tokens(email) -> Token:
    access_token, access_token_expire_time = create_access_token(email)
    refresh_token, refresh_token_expire_time = create_refresh_token(email)
    _access_token = AccessToken(token=access_token, token_type="bearer", email=email,
                                expire_date=access_token_expire_time)
    _refresh_token = RefreshToken(token=refresh_token, token_type="bearer", email=email,
                                  expire_date=refresh_token_expire_time)

    return Token(access_token=_access_token, refresh_token=_refresh_token)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
