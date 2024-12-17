from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.debate import DebateSchema
from app.schema.user import BasicUserSchema


class CreateDebateReq(BaseModel):
    isbn: str = Field()
    location: Optional[str] = None
    held_at: Optional[datetime] = None
    title: str = Field(max_length=255)
    content: Optional[str] = None
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None

    @field_validator("image1", "image2", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value


class BasicDebateRes(DebateSchema):
    user: BasicUserSchema


__all__ = ["CreateDebateReq", "BasicDebateRes"]
