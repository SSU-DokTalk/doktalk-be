from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.summary import SummarySchema
from app.schema.user import BasicUserSchema
from app.schema.book import BookSchema


class CreateSummaryReq(BaseModel):
    isbn: int = Field()
    title: str = Field()
    free_content: Optional[str] = None
    charged_content: Optional[str] = None
    price: int = Field()
    files: Optional[list[HttpUrl]] = None

    @field_validator("files", mode="before")
    def remove_empty_strings_from_files(
        value: Optional[List[str]],
    ) -> Optional[List[str]]:
        if value:
            return [file for file in value if (file != "" or file is not None)]
        return value

    class Config:
        from_attributes = True


class BasicSummaryRes(SummarySchema):
    user: BasicUserSchema
    book: BookSchema


__all__ = ["CreateSummaryReq", "BasicSummaryRes"]
