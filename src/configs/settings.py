import json
import os
from functools import lru_cache
from typing import Any
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, EnvSettingsSource, SettingsConfigDict


@lru_cache
def getEnvFilename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class JwtSourceParse(EnvSettingsSource):
    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        if (
            field_name == "ACCESS_TOKEN_EXPIRATION_TIME"
            or field_name == "REFRESH_TOKEN_EXPIRATION_TIME"
        ):
            int_val = 0
            try:
                int_val = int(value)
            except ValueError as e:
                last = value[-1]
                time_factor = 1

                if last == "d":
                    time_factor = 24 * 3600
                elif last == "mn":
                    time_factor = 60
                elif last == "s":
                    time_factor = 1
                else:
                    raise ValueError("Unsupported time unit")
                int_val = int(value[:-1]) * time_factor

            return int_val

        return json.loads(value)


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
    JWT_ACCESS_TOKEN_SECRET: str
    JWT_REFRESH_TOKEN_SECRET: str

    ACCESS_TOKEN_EXPIRATION_TIME: str
    REFRESH_TOKEN_EXPIRATION_TIME: str

    JWT_ISSUER: str

    AES_KEY: str

    # class Config:
    #     env_file = getEnvFilename()

    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=(".env", ".env.prod")
    )


@lru_cache
def getSettings() -> ApplicationSettings:
    settings = ApplicationSettings()
    return settings
