from sqlalchemy import Column, UUID, Text, ForeignKey, DateTime

from service.db import Base
from service.models.users import Users


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    # TODO: When author is deleted should the post be deleted?
    author_id = Column(UUID, ForeignKey(Users.id), nullable=False)
    created_at = Column(DateTime, nullable=False)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(UUID, primary_key=True)
    content = Column(Text, nullable=False)
    author_id = Column(UUID, ForeignKey(Users.id), nullable=False)
    # TODO: When post is deleted should the comment be deleted?
    post_id = Column(UUID, ForeignKey(Posts.id), nullable=False)
    created_at = Column(DateTime, nullable=False)
