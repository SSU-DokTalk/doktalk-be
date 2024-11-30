from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from app.schema.summary import SummarySchema
from app.schema.user import BasicUserSchema


class CreateSummaryReq(BaseModel):
    isbn: str = Field()
    title: str = Field()
    free_content: Optional[list[str]] = None
    charged_content: Optional[list[str]] = None
    price: int = Field()
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None

    class Config:
        from_attributes = True


class BasicSummaryRes(SummarySchema):
    user: BasicUserSchema
