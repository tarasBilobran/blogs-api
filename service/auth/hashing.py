from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def is_password_correct(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)
