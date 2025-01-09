from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DabateCommentSchema(BaseModel):

    id: int = Field()
    user_id: int = Field()
    dabate_id: int = Field()
    upper_comment_id: Optional[int] = None
    content: Optional[str] = None
    comments_num: int = Field()
    likes_num: int = Field()
    created: datetime = Field()
    updated: datetime = Field()

    class Config:
        from_attributes = True


__all__ = ["DabateCommentSchema"]
