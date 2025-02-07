from pydantic import BaseModel

from app.schema.my_book import MyBookSchema
from app.schema.user import BasicUserSchema
from app.schema.book import BookSchema


class CreateMyBookReq(BaseModel):
    pass


class BasicMyBookRes(MyBookSchema):
    user: BasicUserSchema
    book: BookSchema


__all__ = ["CreateMyBookReq", "BasicMyBookRes"]
