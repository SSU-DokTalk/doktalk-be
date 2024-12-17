from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class DebateSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()

    isbn: str = Field()
    location: Optional[str] = None
    held_at: Optional[datetime] = None
    title: str = Field()
    content: Optional[str] = None
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None
    likes_num: int = Field()
    comments_num: int = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    @field_validator("image1", "image2", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True
