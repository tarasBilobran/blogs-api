from sqlalchemy import Column, UUID, Text, DateTime

from service.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime)
