from datetime import datetime, timedelta

from jose import jwt, ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError

import jwt_config
from error import security_exception
from session import session_schema


def create_tokens(email):
    access_token, access_token_expire_time = __generate_access_token(email)
    refresh_token, refresh_token_expire_time = __generate_refresh_token(email)
    _access_token = session_schema.AccessToken(token=access_token, token_type="bearer", email=email,
                                               expire_date=access_token_expire_time)
    _refresh_token = session_schema.RefreshToken(token=refresh_token, token_type="bearer",
                                                 email=email, expire_date=refresh_token_expire_time)

    return session_schema.Token(access_token=_access_token, refresh_token=_refresh_token)


def extract_email_from_token(token):
    payload = __verify_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise security_exception.CredentialException()
    return email


def __generate_access_token(email):
    access_token_expire_time = datetime.utcnow() + timedelta(hours=9) + timedelta(
        minutes=jwt_config.JwtConfig.get_access_token_expire_minutes())

    access_data = {
        "sub": email,
        "exp": access_token_expire_time
    }

    encoded_access_token = jwt.encode(access_data, jwt_config.JwtConfig.get_secret_key(),
                                      algorithm=jwt_config.JwtConfig.get_algorithm())
    return encoded_access_token, access_token_expire_time


def __generate_refresh_token(email):
    refresh_token_expire_time = datetime.utcnow() + timedelta(hours=9) + timedelta(
        minutes=jwt_config.JwtConfig.get_refresh_token_expire_minutes())

    refresh_data = {
        "sub": email,
        "exp": refresh_token_expire_time
    }

    encoded_refresh_token = jwt.encode(refresh_data, jwt_config.JwtConfig.get_secret_key(),
                                       algorithm=jwt_config.JwtConfig.get_algorithm())
    return encoded_refresh_token, refresh_token_expire_time


def __verify_token(token):
    try:
        return jwt.decode(token, key=jwt_config.JwtConfig.get_secret_key(),
                          algorithms=[jwt_config.JwtConfig.get_algorithm()])
    except JWTClaimsError:
        raise security_exception.TokenInvalidException()
    except ExpiredSignatureError:
        raise security_exception.TokenTimeOutException()
    except JWTError:
        raise security_exception.CredentialException()
