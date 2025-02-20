from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.summary import SummarySchema
from app.schema.user import BasicUserSchema
from app.schema.book import BookSchema
from app.dto.file import FileDto


class CreateSummaryReq(BaseModel):
    isbn: int = Field()
    title: str = Field()
    free_content: Optional[str] = None
    charged_content: Optional[str] = None
    price: int = Field()
    files: Optional[list[FileDto]] = None
    category: int = Field()

    class Config:
        from_attributes = True


class BasicSummaryRes(SummarySchema):
    user: BasicUserSchema
    book: BookSchema


__all__ = ["CreateSummaryReq", "BasicSummaryRes"]
