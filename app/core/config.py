import secrets

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESTH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    PROJECT_NAME: str

    MYSQL_SERVER: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str


settings = Settings()
