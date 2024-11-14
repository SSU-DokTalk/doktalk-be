import os
from passlib.context import CryptContext
import string
import random
from pydantic import BaseModel, Field
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from typing import Literal
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer

cryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()


def random_password() -> str:

    letter_length = random.randint(1, 20)
    digit_length = random.randint(1, 5)
    punctuation_length = random.randint(1, 5)
    string_pool = (
        [random.choice(string.ascii_letters) for _ in range(letter_length)]
        + [random.choice(string.digits) for _ in range(digit_length)]
        + [random.choice("!@#$%*^&+=") for _ in range(punctuation_length)]
    )
    random.shuffle(string_pool)

    return "".join(string_pool)


SECRET_KEY = os.getenv("JWT_SECRET_KEY")


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
    encoded_jwt = jwt.encode(payload.model_dump(), SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def create_access_token(data: TokenData) -> str:
    return create_token(data, timedelta(minutes=30))


def create_refresh_token(data: TokenData) -> str:
    return create_token(data, timedelta(days=14))


def get_token(token: str) -> str:
    prefix = "Bearer "
    if token[: len(prefix)] != prefix:
        return None
    return token[len(prefix) :]


def validate_token(token: str) -> bool:
    try:
        payload: Payload = Payload(
            **jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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
    return Payload(**jwt.decode(token, SECRET_KEY, algorithms=["HS256"]))
