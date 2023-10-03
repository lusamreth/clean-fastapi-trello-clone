#
import os
from functools import lru_cache
from pydantic import BaseSettings


@lru_cache
def getEnvFilename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class ApplicationSettings(BaseSettings):
    API_VERSION: str = "1.0"
    APP_NAME: str = "mini-jrello"
    # database
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DEBUG_MODE: bool
    # security
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str

    class Config:
        env_file = getEnvFilename()


@lru_cache
def getSettings() -> ApplicationSettings:
    settings = ApplicationSettings()
    return settings
