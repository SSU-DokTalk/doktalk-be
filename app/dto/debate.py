from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.debate import DebateSchema
from app.schema.user import BasicUserSchema
from app.schema.book import BookSchema


class CreateDebateReq(BaseModel):
    isbn: int = Field()
    location: Optional[str] = None
    held_at: Optional[datetime] = None
    title: str = Field(max_length=255)
    content: Optional[str] = None
    files: Optional[list[HttpUrl]] = None

    @field_validator("files", mode="before")
    def remove_empty_strings_from_files(
        value: Optional[List[str]],
    ) -> Optional[List[str]]:
        if value:
            return [file for file in value if (file != "" or file is not None)]
        return value


class BasicDebateRes(DebateSchema):
    user: BasicUserSchema
    book: BookSchema


__all__ = ["CreateDebateReq", "BasicDebateRes"]
