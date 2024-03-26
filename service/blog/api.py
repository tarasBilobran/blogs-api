import uuid
import datetime as dt

import sqlalchemy
from fastapi import APIRouter, Depends, Body
from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from service.blog.schemas import PostSchema, CommentSchema
from service.dependencies import get_db_session, RequestUser, require_request_user
from service.exceptions import PostNotFoundError
from service.models.posts import Posts, Comments

POSTS_ROUTER = APIRouter(dependencies=[Depends(require_request_user)])


@POSTS_ROUTER.post("/posts")
def create_post(
    title: str = Body(...),
    content: str = Body(...),
    session: Session = Depends(get_db_session),
    user: RequestUser = Depends(require_request_user),
) -> PostSchema:
    post = Posts(
        id=uuid.uuid4(),
        title=title,
        content=content,
        author_id=user.id,
        created_at=dt.datetime.now(),
    )
    session.add(post)
    session.commit()
    return PostSchema.model_validate(post)


@POSTS_ROUTER.get("/posts")
def list_posts(session: Session = Depends(get_db_session)) -> list[PostSchema]:
    # TODO: Consider adding pagination
    posts = session.query(Posts).all()
    return TypeAdapter(list[PostSchema]).validate_python(posts)


@POSTS_ROUTER.get("/posts/{id}")
def get_post(id: uuid.UUID, session: Session = Depends(get_db_session)) -> PostSchema:
    post = session.query(Posts).filter_by(id=id).first()
    if post is None:
        raise PostNotFoundError

    return PostSchema.model_validate(post)


@POSTS_ROUTER.post("/posts/{post_id}/comments")
def create_comment(
    post_id: int,
    content: str,
    session: Session = Depends(get_db_session),
    user: RequestUser = Depends(require_request_user),
) -> CommentSchema:
    comment = Comments(
        id=uuid.uuid4(),
        content=content,
        post_id=post_id,
        author_id=user.id,
        created_at=dt.datetime.now()
    )
    session.add(comment)
    try:
        session.commit()
    except sqlalchemy.exc.SQLAlchemyError:
        session.rollback()
        raise PostNotFoundError

    return CommentSchema.model_validate(comment)



@POSTS_ROUTER.get("/posts/{post_id}/comments")
def list_blog_comments(post_id: int, session: Session = Depends(get_db_session)) -> list[CommentSchema]:
    comments = session.query(Comments).filter_by(post_id=post_id).all()
    return TypeAdapter(list[CommentSchema]).validate_python(comments)
