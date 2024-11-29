from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PostCommentSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    post_id: int = Field()
    content: Optional[str] = None
    likes_num: int = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Config:
        from_attributes = True
