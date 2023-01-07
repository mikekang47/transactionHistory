from datetime import datetime, timedelta

from jose import jwt, JWTError, ExpiredSignatureError

import jwt_config
from error import login_fail_exception, credential_exception, user_not_found_exception
from session import session_schema
from user import user_application
from user.user_application import pwd_context
from user.user_model import User


def create_session(db, email: str):
    access_data = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=9) + timedelta(minutes=jwt_config.getAccessTokenExpireMinutes())
    }

    refresh_data = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=9) + timedelta(minutes=jwt_config.getRefreshTokenExpireMinutes())
    }

    encoded_access_token = jwt.encode(access_data, jwt_config.getSecretKey(), algorithm=jwt_config.getAlgorithm())
    encoded_refresh_token = jwt.encode(refresh_data, jwt_config.getSecretKey(), algorithm=jwt_config.getAlgorithm())

    # login 시 expire_time 초기화
    user = user_application.get_user(db, email=email)
    user.refresh_token = encoded_refresh_token
    user.expire_time = refresh_data["exp"]

    _access_token = session_schema.AccessToken(access_token=encoded_access_token, token_type="bearer", email=user.email,
                                               expire_date=access_data["exp"])
    _refresh_token = session_schema.RefreshToken(refresh_token=encoded_refresh_token, token_type="bearer",
                                                 email=user.email, expire_date=refresh_data["exp"])
    return session_schema.Token(access_token=_access_token, refresh_token=_refresh_token)


def delete_session(db, token):
    try:
        payload = jwt.decode(token, key=jwt_config.getSecretKey(), algorithms=[jwt_config.getAlgorithm()])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception.CredentialExcpetion()
    except ExpiredSignatureError:
        raise credential_exception.TokenTimeOutException()
    except JWTError:
        raise credential_exception.CredentialExcpetion()
    else:
        user = user_application.get_user(db, email=email)
        if user is None:
            raise user_not_found_exception.UserNotFoundException()
        user.expire_time = datetime.utcnow() + timedelta(hours=9)

        db.commit()
        return user


def verfiy(user: User, login_data_password: str):
    if not user or not pwd_context.verify(login_data_password, user.password):
        raise login_fail_exception.LoginFailException()
