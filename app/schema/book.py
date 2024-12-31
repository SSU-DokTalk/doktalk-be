from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class BookSchema(BaseModel):
    title: str = Field()
    link: Optional[HttpUrl] = Field()
    image: Optional[HttpUrl] = Field()
    author: str = Field()
    discount: str = Field()
    publisher: str = Field()
    pubdate: str = Field()
    isbn: str = Field()
    description: str = Field()

    @field_validator("link", "image", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True


class BookResponseSchema(BaseModel):
    lastBuildDate: datetime = Field()
    total: int = Field()
    start: int = Field()
    display: int = Field()
    items: list[BookSchema] = Field()

    @field_validator("lastBuildDate", mode="before")
    def parse_last_build_date(cls, value: str) -> datetime:
        date_format = "%a, %d %b %Y %H:%M:%S %z"
        return datetime.strptime(value, date_format)

    class Config:
        from_attributes = True


__all__ = ["BookSchema", "BookResponseSchema"]
