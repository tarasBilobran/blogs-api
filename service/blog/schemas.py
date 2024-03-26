import datetime as dt
import uuid

from pydantic import BaseModel, ConfigDict


class PostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    content: str
    author_id: uuid.UUID
    created_at: dt.datetime


class CommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content: str
    author_id: uuid.UUID
    post_id: uuid.UUID
    created_at: dt.datetime
