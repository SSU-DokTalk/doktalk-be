from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class BasicRegisterReq(BaseModel):
    email: str = Field(
        max_length=255,
        # 이메일 format 검증
        pattern=r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    password: str = Field(
        min_length=8,
        max_length=30,
        # 최소 8자. 영문자, 숫자, 특수문자를 각각 최소 1개 이상 포함 -> @field_validator
        # pattern=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%*^&+=])[A-Za-z\d!@#$%*^&+=]{8,}$",
    )
    name: Optional[str] = None
    gender: Optional[bool] = None
    age: Optional[int] = None

    @field_validator("password")
    def validate_password(cls, v):
        password_validation = re.compile(
            r"^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%*^&+=]).*$"
        )
        if not password_validation.fullmatch(v):
            raise ValueError("Invalid Password")
        return v

    class Config:
        from_attributes = True


class BasicLoginReq(BaseModel):
    email: str = Field(
        max_length=255,
        # 이메일 format 검증
        pattern=r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    password: str = Field(
        min_length=8,
        max_length=30,
        # 최소 8자. 영문자, 숫자, 특수문자를 각각 최소 1개 이상 포함 -> @field_validator
        # pattern=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$",
    )
