from datetime import datetime, timedelta

from error import session_exception
from user import user_application
from user.user_application import pwd_context
from user.user_model import User
from util import jwt_util


def create_session(db, email: str):
    tokens = jwt_util.create_tokens(email)

    user = user_application.get_user(db, email=email)
    user.refresh_token = tokens.get_refresh_token().get_token()
    user.expire_time = tokens.get_refresh_token().expire_date

    db.commit()

    return tokens


def delete_session(db, token):
    email = jwt_util.extract_email_from_token(token)

    user = user_application.get_user(db, email=email)
    user.expire_time = datetime.utcnow() + timedelta(hours=9)

    db.commit()
    return user


def verify_password(user: User, login_data_password: str):
    if not user or not pwd_context.verify(login_data_password, user.password):
        raise session_exception.LoginFailException()


def get_access_token(db, refresh_token):
    email = jwt_util.extract_email_from_token(refresh_token)
    user = user_application.get_user(db, email=email)

    tokens = jwt_util.create_tokens(email)

    user.refresh_token = tokens.get_refresh_token().get_token()
    user.expire_time = tokens.get_refresh_token().expire_date

    db.commit()

    return tokens
