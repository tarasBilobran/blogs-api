import pytest
import os
import pathlib

from starlette.testclient import TestClient

from service.app import APP
from service.db import SessionLocal
from service.settings import override_settings, Settings, JWTSettings, DBSettings

import alembic
import alembic.command
import alembic.config


ALEMBIC_INI_FILE = pathlib.Path(__file__).parent.parent.parent / "alembic.ini"
MIGRATIONS_FOLDER = ALEMBIC_INI_FILE.parent / "migrations"


@pytest.fixture
def api():
    return TestClient(APP)


@pytest.fixture(autouse=True, scope="session")
def set_testing_settings():
    # Set db config to env variable to make sure alembic can use it as well
    os.environ.update({
        "DB_USER": "postgres",
        "DB_PASSWORD": "password",
        "DB_HOST": "127.0.0.1",
        "DB_PORT": "5556",
        "DB_NAME": "db"
    })
    settings = Settings(
        jwt=JWTSettings(secret_key="secret"),
        db=DBSettings.from_env()
    )
    override_settings( settings )

    return settings


@pytest.fixture(autouse=True)
def migrations():
    config = alembic.config.Config(file_=ALEMBIC_INI_FILE)
    config.set_main_option("script_location", str(MIGRATIONS_FOLDER.absolute()))

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def db_session():
    with SessionLocal() as session:
        yield session
