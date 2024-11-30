from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from app.schema.debate import DebateSchema
from app.schema.user import BasicUserSchema


class CreateDebateReq(BaseModel):
    isbn: str = Field()
    location: Optional[str] = None
    held_at: Optional[datetime] = None
    title: str = Field(max_length=255)
    content: Optional[str] = None
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None


class BasicDebateRes(DebateSchema):
    user: BasicUserSchema
