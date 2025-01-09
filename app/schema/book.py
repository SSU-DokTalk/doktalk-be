from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class BookSchema(BaseModel):
    isbn: int = Field()
    title: str = Field()
    image: Optional[HttpUrl] = None
    author: str = Field()
    publisher: str = Field()
    pubdate: Optional[date] = Field()
    description: str = Field()

    @field_validator("image", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True
