import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from service.dependencies import get_db_session, require_request_user
from service.exceptions import UserNotFoundError
from service.models.users import Users
from service.users.schemas import UserSchema

USERS_ROUTER = APIRouter(dependencies=[Depends(require_request_user)])


@USERS_ROUTER.get("/users/{user_id}")
async def get_user(user_id: uuid.UUID, session: Session = Depends(get_db_session)) -> UserSchema:
    user = session.query(Users).filter_by(id=user_id).first()
    if user is None:
        raise UserNotFoundError

    return UserSchema.model_validate(user)
