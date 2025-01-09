from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.my_book import MyBookSchema
from app.schema.user import BasicUserSchema
from app.schema.book import BookSchema


class CreateMyBookReq(BaseModel):
    pass


class BasicMyBookRes(MyBookSchema):
    user: BasicUserSchema
    book: BookSchema


__all__ = ["CreateMyBookReq", "BasicMyBookRes"]
