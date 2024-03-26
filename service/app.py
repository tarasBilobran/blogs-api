import gunicorn.app.base
from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from service.auth.api import AUTH_ROUTER
from service.blog.api import POSTS_ROUTER
from service.exceptions import PostNotFoundError, PostCommentNotFoundError, UserNotFoundError, \
    AuthenticationFailedError, AuthorizationFailedError, DuplicateUserError
from service.settings import set_default_settings
from service.users.api import USERS_ROUTER

APP = FastAPI()


@APP.get("/_up")
def is_up():
    return {"ok": True}


APP.include_router(
    AUTH_ROUTER,
    prefix="/api/v1/auth"
)
APP.include_router(
    POSTS_ROUTER,
    prefix="/api/v1"
)
APP.include_router(
    USERS_ROUTER,
    prefix="/api/v1"
)


@APP.on_event("startup")
def handle_startup():
    set_default_settings()


@APP.exception_handler(PostNotFoundError)
@APP.exception_handler(PostCommentNotFoundError)
def handle_404_errors(*_) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content="Not Found.")


@APP.exception_handler(UserNotFoundError)
@APP.exception_handler(AuthorizationFailedError)
@APP.exception_handler(DuplicateUserError)
def handle_403_errors(*_) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content="Forbidden.")


@APP.exception_handler(AuthenticationFailedError)
def handle_401_errors(*_):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content="Unauthorized."
    )
