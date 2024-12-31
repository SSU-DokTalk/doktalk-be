from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DabateCommentSchema(BaseModel):

    id: int = Field()
    user_id: int = Field()
    dabate_id: int = Field()
    content: Optional[str] = None
    likes_num: int = Field()
    created: datetime = Field()
    updated: datetime = Field()

    class Config:
        from_attributes = True


__all__ = ["DabateCommentSchema"]
