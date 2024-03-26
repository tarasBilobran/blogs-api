import uuid
from typing import NamedTuple

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from service.exceptions import AuthenticationFailedError, UserNotFoundError
from service.db import SessionLocal
from service.models.session_tokens import SessionTokens
from service.models.users import Users
from service.settings import Settings, get_settings
from service.tokens import decode_jwt


class RequestUser(BaseModel):
    id: uuid.UUID


def get_db_session() -> Session:
    with SessionLocal() as session:
        yield session


def require_jwt_token(http_auth: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False))) -> str:
    if http_auth is None:
        raise AuthenticationFailedError

    return http_auth.credentials

def require_request_user(
        token: str = Depends(require_jwt_token),
        settings: Settings = Depends(get_settings),
        session: Session = Depends(get_db_session)
) -> RequestUser:
    payload = decode_jwt(token, settings.jwt)

    user_id = payload["user_id"]
    user = session.query(Users).filter_by(id=user_id).first()
    token_record_exists = session.query(SessionTokens).filter_by(token=token, user_id=user.id).first() is not None
    if user is None or not token_record_exists:
        raise UserNotFoundError

    return RequestUser(id=user.id)
