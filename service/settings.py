from __future__ import annotations

from datetime import timedelta
from sqlalchemy import URL
import os

import pydantic


class JWTSettings(pydantic.BaseModel):
    secret_key: str
    issuer: str = "api.blog-project.example.com"
    algorithm: str = "HS256"
    access_token_ttl: timedelta = timedelta(days=2)


class DBSettings(pydantic.BaseModel):
    host: str
    username: str
    password: str
    port: int
    db_name: str

    @classmethod
    def from_env(cls) -> DBSettings:
        return cls(
            host=os.environ["DB_HOST"],
            port=int(os.environ["DB_PORT"]),
            username=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            db_name=os.environ["DB_NAME"],
        )

    def to_connection_url(self) -> URL:
        return URL.create(
            "postgresql+psycopg2",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name,
        )


class Settings(pydantic.BaseModel):
    jwt: JWTSettings
    db: DBSettings


SETTINGS: Settings | None = None


def set_default_settings() -> None:
    global SETTINGS

    if SETTINGS is not None:
        raise RuntimeError

    SETTINGS = Settings(
        jwt=JWTSettings(
            # For demo purposes leave as is.
            secret_key="secret",
        ),
        db=DBSettings.from_env()
    )


def override_settings(settings: Settings) -> None:
    global SETTINGS
    SETTINGS = settings


def get_settings() -> Settings:
    if SETTINGS is None:
        raise RuntimeError

    return SETTINGS
