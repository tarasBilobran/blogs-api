from sqlalchemy import Column, Text, UUID, ForeignKey

from service.db import Base
from service.models.users import Users


class SessionTokens(Base):
    __tablename__ = "session_tokens"

    token = Column(Text, primary_key=True, nullable=False)
    user_id = Column(UUID, ForeignKey(Users.id), nullable=False)
