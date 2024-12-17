import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator, EmailStr, HttpUrl


class BasicRegisterReq(BaseModel):
    email: EmailStr = Field(
        max_length=255,
    )
    password: str = Field(
        examples=["testtest123@"],
        min_length=8,
        max_length=30,
        # 최소 8자. 영문자, 숫자, 특수문자를 각각 최소 1개 이상 포함 -> @field_validator
        # pattern=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%*^&+=])[A-Za-z\d!@#$%*^&+=]{8,}$",
    )
    profile: Optional[HttpUrl] = None
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

    @field_validator("profile", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True


class BasicLoginReq(BaseModel):
    email: EmailStr = Field(
        max_length=255,
        # 이메일 format 검증
    )
    password: str = Field(
        examples=["testtest123@"],
        min_length=8,
        max_length=30,
        # 최소 8자. 영문자, 숫자, 특수문자를 각각 최소 1개 이상 포함 -> @field_validator
        # pattern=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$",
    )

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


class UpdateUserInfoReq(BaseModel):
    profile: Optional[str] = None
    name: Optional[str] = None
    introduction: Optional[str] = None

    @field_validator("profile", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True


__all__ = ["BasicRegisterReq", "BasicLoginReq", "UpdateUserInfoReq"]
