import secrets

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    TOKEN_PREFIX: str = "Bearer"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    MYSQL_USER: str
    MYSQL_PASSWORD: SecretStr
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DB: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
