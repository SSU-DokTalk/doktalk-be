from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class SummarySchema(BaseModel):
    id: int = Field()
    user_id: int = Field()

    isbn: str = Field()
    title: str = Field()
    free_content: Optional[list[str]] = None
    charged_content: Optional[list[str]] = None
    price: int = Field()
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None
    likes_num: int = Field()
    comments_num: int = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Config:
        from_attributes = True
