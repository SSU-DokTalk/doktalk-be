from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator

from app.enums import ROLE


class BasicUserSchema(BaseModel):
    id: int = Field()

    profile: Optional[HttpUrl] = None
    name: Optional[str] = None
    role: ROLE = Field(default=ROLE.USER)
    is_deleted: bool = Field(default=False)

    @field_validator("profile", mode="before")
    def empty_string_to_none(value: Any) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: int = Field()

    email: EmailStr = Field(max_length=255)
    profile: Optional[HttpUrl] = None
    name: Optional[str] = None
    gender: Optional[bool] = None
    birthday: Optional[datetime] = None
    introduction: Optional[str] = None
    follower_num: int = Field()
    following_num: int = Field()
    role: ROLE = Field(default=ROLE.USER)
    created: datetime = Field()
    updated: datetime = Field()
    deleted_at: Optional[datetime] = None
    is_deleted: bool = Field(default=False)

    @field_validator("profile", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True


__all__ = ["UserSchema", "BasicUserSchema"]
