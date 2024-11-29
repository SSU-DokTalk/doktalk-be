from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from app.schema.user import BasicUserSchema
from app.schema.post import PostSchema


class CreatePostReq(BaseModel):
    title: str = Field(examples=["test"], max_length=255)
    content: Optional[str] = None
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None


class BasicPostRes(PostSchema):
    user: BasicUserSchema
