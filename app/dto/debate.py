from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.debate import DebateSchema
from app.schema.user import BasicUserSchema
from app.schema.book import BookSchema
from app.dto.file import FileDto


class CreateDebateReq(BaseModel):
    title: str = Field(max_length=255)
    location: Optional[str] = None
    link: Optional[HttpUrl] = None
    held_at: Optional[datetime] = None
    isbn: int = Field()
    category: int = Field()
    limit: int = Field()
    files: Optional[list[FileDto]] = None
    content: Optional[str] = None
    price: int = Field()


class BasicDebateRes(DebateSchema):
    user: BasicUserSchema
    book: BookSchema


__all__ = ["CreateDebateReq", "BasicDebateRes"]
