from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.dto.file import FileDto


class DebateSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    isbn: int = Field()

    location: Optional[str] = None
    link: Optional[HttpUrl] = None
    held_at: Optional[datetime] = None
    title: str = Field()
    content: Optional[str] = None
    files: Optional[List[FileDto]] = None
    price: int = Field()
    limit: int = Field()
    category: int = Field()
    likes_num: int = Field()
    comments_num: int = Field()
    created: datetime = Field()
    updated: datetime = Field()

    @field_validator("link", mode="before")
    def remove_empty_strings_from_link(
        value: Optional[HttpUrl],
    ) -> Optional[HttpUrl]:
        if value:
            return value if value != "" else None
        return value

    @field_validator("files", mode="before")
    def remove_empty_strings_from_files(
        value: Optional[List[str]],
    ) -> Optional[List[str]]:
        if value:
            return [file for file in value if (file != "" or file is not None)]
        return value

    class Config:
        from_attributes = True


__all__ = ["DebateSchema"]
