import contextlib

from sqlalchemy import create_engine, Engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base

from service.settings import get_settings


def get_engine(url: str | URL) -> Engine:
    return create_engine(url)

def SessionLocal():
    settings = get_settings()
    engine = get_engine(settings.db.to_connection_url())
    return sessionmaker(bind=engine)()


Base = declarative_base()
