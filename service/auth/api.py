import uuid

import sqlalchemy.exc
from fastapi import APIRouter, Form, Depends
from sqlalchemy.orm import Session

from service.auth.hashing import hash_password, is_password_correct
from service.auth.schemas import TokenObject
from service.dependencies import get_db_session, require_request_user, RequestUser, require_jwt_token
from service.exceptions import AuthorizationFailedError, DuplicateUserError
from service.models.session_tokens import SessionTokens
from service.models.users import Users
from service.settings import Settings, get_settings
from service.tokens import generate_access_token

AUTH_ROUTER = APIRouter()


@AUTH_ROUTER.post("/login")
async def login(
        email: str = Form(...),
        password: str = Form(...),
        session: Session = Depends(get_db_session),
        settings: Settings = Depends(get_settings)
) -> TokenObject:
    user = session.query(Users).filter_by(email=email).first()
    if user is None or not is_password_correct(password, user.password_hash):
        raise AuthorizationFailedError

    access_token = generate_access_token(user.id, settings.jwt)
    session.add(SessionTokens(token=access_token, user_id=user.id))
    session.commit()
    return TokenObject(access_token=access_token)


@AUTH_ROUTER.post("/logout")
async def logout(
    token: str = Depends(require_jwt_token),
    user: RequestUser = Depends(require_request_user),
    session: Session = Depends(get_db_session),
):
    session.query(SessionTokens).filter_by(token=token, user_id=user.id).delete()
    session.commit()


@AUTH_ROUTER.post("/registration")
async def registration(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        session: Session = Depends(get_db_session),
        settings: Settings = Depends(get_settings)
) -> TokenObject:
    user = Users(
        id=uuid.uuid4(),
        username=username,
        email=email,
        password_hash=hash_password(password)
    )
    session.add(user)

    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        raise DuplicateUserError

    access_token = generate_access_token(user.id, settings.jwt)
    session.add(SessionTokens(token=access_token, user_id=user.id))
    session.commit()
    return TokenObject(access_token=access_token)
