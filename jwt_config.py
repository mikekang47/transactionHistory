from starlette.config import Config

config = Config('.env')

__ACCESS_TOKEN_EXPIRE_MINUTES = int(eval(config('ACCESS_TOKEN_EXPIRE_MINUTES'))) #24 * 60 하루
__REFRESH_TOKEN_EXPIRE_MINUTES = int(eval(config('REFRESH_TOKEN_EXPIRE_MINUTES'))) # 24 * 60 * 14 2주
__SECRET_KEY = config('SECRET_KEY')
__ALGORITHM = "HS256"


def getAccessTokenExpireMinutes():
    return __ACCESS_TOKEN_EXPIRE_MINUTES


def getSecretKey():
    return __SECRET_KEY


def getAlgorithm():
    return __ALGORITHM


def getRefreshTokenExpireMinutes():
    return __REFRESH_TOKEN_EXPIRE_MINUTES
