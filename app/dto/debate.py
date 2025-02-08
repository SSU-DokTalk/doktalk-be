from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.debate import DebateSchema
from app.schema.user import BasicUserSchema
from app.schema.book import BookSchema
from app.dto.file import FileDto


class CreateDebateReq(BaseModel):
    isbn: int = Field()
    location: Optional[str] = None
    held_at: Optional[datetime] = None
    title: str = Field(max_length=255)
    content: Optional[str] = None
    price: int = Field()
    files: Optional[list[FileDto]] = None
    category: int = Field()


class BasicDebateRes(DebateSchema):
    user: BasicUserSchema
    book: BookSchema


__all__ = ["CreateDebateReq", "BasicDebateRes"]
