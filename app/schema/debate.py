from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class DebateSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()

    isbn: str = Field()
    location: Optional[str] = None
    held_at: Optional[datetime] = None
    title: str = Field()
    content: Optional[str] = None
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None
    likes_num: int = Field()
    comments_num: int = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Config:
        from_attributes = True
