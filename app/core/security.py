import string
import random
import base64
from typing import Callable

from fastapi.security import APIKeyHeader
import jwt
from jwt.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

from app.core.config import settings

cryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = APIKeyHeader(name="Authorization")


def random_password() -> str:

    letter_length = random.randint(5, 20)
    digit_length = random.randint(3, 5)
    punctuation_length = random.randint(2, 5)
    string_pool = (
        [random.choice(string.ascii_letters) for _ in range(letter_length)]
        + [random.choice(string.digits) for _ in range(digit_length)]
        + [random.choice("!@#$%*^&+=") for _ in range(punctuation_length)]
    )
    random.shuffle(string_pool)

    return "".join(string_pool)


class TokenData(BaseModel):
    userId: int
    name: str


class Payload(BaseModel):
    sub: int
    name: str = None
    iat: datetime
    exp: datetime


def create_token(data: TokenData, expire_in: timedelta | None = None) -> str:
    now = datetime.now(timezone.utc)
    if expire_in:
        expire = now + expire_in
    else:
        expire = now + timedelta(minutes=15)

    payload = Payload(
        **{"sub": data.userId, "name": data.name, "iat": now, "exp": expire}
    )
    encoded_jwt = jwt.encode(
        payload.model_dump(), settings.JWT_SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def create_access_token(data: TokenData) -> str:
    return create_token(data, timedelta(minutes=30))


def create_refresh_token(data: TokenData) -> str:
    return create_token(data, timedelta(days=14))


def encrypt(token: str, func: Callable[[str], bytes] = base64.b85encode) -> str:
    return func(f"Bearer {token}".encode()).decode()


def get_token(token: str, func: Callable[[str], bytes] = base64.b85decode) -> str:
    token = func(token).decode()
    prefix = "Bearer "
    if not token or len(token) < len(prefix):
        return None
    if token[: len(prefix)] != prefix:
        return None
    return token[len(prefix) :]


def validate_token(token: str) -> bool:
    try:
        payload: Payload = Payload(
            **jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        )
    except:
        return False
    now = datetime.now(timezone.utc)
    if payload.exp < now:
        raise ExpiredSignatureError
    return True


def get_token_payload(token: str) -> Payload:
    if not validate_token(token):
        return None
    return Payload(**jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"]))
