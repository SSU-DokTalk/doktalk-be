from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class BookAPISchema(BaseModel):
    title: str = Field()
    link: Optional[HttpUrl] = None
    image: Optional[HttpUrl] = None
    author: str = Field()
    discount: Optional[int] = None
    publisher: str = Field()
    pubdate: str = Field()
    isbn: int = Field()
    description: str = Field()

    @field_validator("link", "image", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True


class BookAPIResponseSchema(BaseModel):
    total: int = Field()
    items: list[BookAPISchema] = Field()
    page: int = Field()
    pages: int = Field()

    class Config:
        from_attributes = True


__all__ = ["BookAPISchema", "BookAPIResponseSchema"]
