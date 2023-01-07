from datetime import datetime, timedelta

from jose import jwt

import jwt_config
from session import session_schema


def create_session(nick_name: str):
    data = {
        "sub": nick_name,
        "exp": datetime.utcnow() + timedelta(hours=9) + timedelta(minutes=jwt_config.getAccessTokenExpireMinutes())
    }
    access_token = jwt.encode(data, jwt_config.getSecretKey(), algorithm=jwt_config.getAlgorithm())

    return session_schema.Token(access_token=access_token, token_type="bearer", nick_name=nick_name,
                                expire_time=data["exp"])
