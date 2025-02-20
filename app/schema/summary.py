from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.dto.file import FileDto


class SummarySchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    isbn: int = Field()

    title: str = Field()
    free_content: Optional[str] = None
    charged_content: Optional[str] = None
    price: int = Field()
    files: Optional[list[FileDto]] = None
    category: int = Field()
    likes_num: int = Field()
    comments_num: int = Field()
    created: datetime = Field()
    updated: datetime = Field()

    class Config:
        from_attributes = True


__all__ = ["SummarySchema"]
