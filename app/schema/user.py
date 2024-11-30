from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, HttpUrl

from app.enums import ROLE


class BasicUserSchema(BaseModel):
    id: int = Field()

    profile: Optional[HttpUrl] = None
    name: Optional[str] = None
    role: ROLE = Field(default=ROLE.USER)
    is_deleted: bool = Field(default=False)

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
    created_at: datetime = Field()
    updated_at: datetime = Field()
    is_deleted: bool = Field(default=False)

    class Config:
        from_attributes = True
