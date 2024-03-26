import pydantic


class TokenObject(pydantic.BaseModel):
    access_token: str
