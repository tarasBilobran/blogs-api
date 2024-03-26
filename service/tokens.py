import datetime as dt
import uuid

from jose import JWTError, jwt
from pydantic import ValidationError

from service.exceptions import AuthenticationFailedError
from service.settings import JWTSettings


def decode_jwt(
    token: str,
    settings: JWTSettings,
) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm], issuer=settings.issuer)
    except (ValidationError, JWTError):
        raise AuthenticationFailedError


def generate_access_token(user_id: uuid.UUID, settings: JWTSettings) -> str:
    return _generate_jwt(
        {"user_id": str(user_id)},
        settings,
    )


def _generate_jwt(
    payload: dict,
    settings: JWTSettings
) -> str:
    return jwt.encode(
        {**payload, "exp": dt.datetime.utcnow() + settings.access_token_ttl, "iss": settings.issuer},
        settings.secret_key,
        algorithm=settings.algorithm,
    )
