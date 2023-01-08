from starlette.config import Config

config = Config('.env')


class JwtConfig:
    __ACCESS_TOKEN_EXPIRE_MINUTES = int(eval(config('ACCESS_TOKEN_EXPIRE_MINUTES')))  # 24 * 60 하루
    __REFRESH_TOKEN_EXPIRE_MINUTES = int(eval(config('REFRESH_TOKEN_EXPIRE_MINUTES')))  # 24 * 60 * 14 2주
    __SECRET_KEY = config('SECRET_KEY')
    __ALGORITHM = "HS256"
    __TOKEN_PREFIX = "Bearer"

    @classmethod
    def get_token_prefix(cls):
        return cls.__TOKEN_PREFIX

    @classmethod
    def get_access_token_expire_minutes(cls):
        return cls.__ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    def get_secret_key(cls):
        return cls.__SECRET_KEY

    @classmethod
    def get_algorithm(cls):
        return cls.__ALGORITHM

    @classmethod
    def get_refresh_token_expire_minutes(cls):
        return cls.__REFRESH_TOKEN_EXPIRE_MINUTES


def get_jwt_config():
    return JwtConfig
