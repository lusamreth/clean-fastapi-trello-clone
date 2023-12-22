import json
import os
from functools import lru_cache
from typing import Any, Dict, Tuple, Type
from pydantic import validator
from pydantic.fields import FieldInfo
import re
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)
from dotenv import load_dotenv

systemEnv = os.getenv("ENV") or "DEV"

if systemEnv == "DEV":
    load_dotenv(".env.dev")
elif systemEnv == "PROD":
    load_dotenv(".env")
    load_dotenv(".env.prod")


@lru_cache
def getEnvFilename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


def determineFactor(directive: str):
    time_factor = 1

    if directive is not None:
        if directive == "d":
            time_factor = 24 * 3600
        elif directive == "mn":
            time_factor = 60
        elif directive == "s":
            time_factor = 1
        else:
            raise ValueError("Unknown time directive")

    return time_factor


def parseTime(value: str):
    int_val = 0

    matches = re.finditer(r"((\d+)(mn|d|s))", value)

    for match in matches:
        num = match.group(2)
        directive = match.group(3)
        time_factor = 1
        time_factor = determineFactor(directive)

        int_val = int(num) * time_factor

    return str(int_val)


# EnvSettingsSource
# PydanticBaseSettingsSource
class JwtSourceParse(EnvSettingsSource):
    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        if (
            field_name == "ACCESS_TOKEN_EXPIRATION_TIME"
            or field_name == "REFRESH_TOKEN_EXPIRATION_TIME"
        ):
            return parseTime(value)

        if value is None:
            print("found non value", field, field_name)
            return value
        return value
        # return json.loads(value)

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class ApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=(".env", ".env.prod")
    )
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
    HOST: str
    PORT: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            JwtSourceParse(settings_cls),
            env_settings,
            init_settings,
            dotenv_settings,
            file_secret_settings,
        )

    # @classmethod
    # def settings_customise_sources(
    #     cls,
    #     settings_cls: Type[BaseSettings],
    #     init_settings: PydanticBaseSettingsSource,
    #     env_settings: PydanticBaseSettingsSource,
    #     dotenv_settings: PydanticBaseSettingsSource,
    #     file_secret_settings: PydanticBaseSettingsSource,
    # ) -> Tuple[PydanticBaseSettingsSource, ...]:
    #     print(dotenv_settings)
    #     return (
    #         JwtSourceParse(settings_cls),
    #         # dotenv_settings,
    #     )


# os.environ["ACCESS_TOKEN_EXPIRATION_TIME"] = "1,2,3"


@lru_cache
def getSettings() -> ApplicationSettings:
    settings = ApplicationSettings()
    return settings
