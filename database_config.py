import os
from functools import lru_cache

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class TestSettings(BaseSettings):
    DB_USERNAME: str = "admin"
    DB_PASSWORD: SecretStr = "1234"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "testing"

    class Config:
        env_file = ".env.test"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    if os.getenv("APP_ENV", "dev").lower() == "test":
        return TestSettings()
    return Settings()


settings = get_settings()
