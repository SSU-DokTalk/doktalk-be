from datetime import datetime

from pydantic import BaseModel, Field


class SummaryCommentSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    summary_id: int = Field()
    upper_comment_id: int = Field()

    content: str = Field()
    comments_num: int = Field()
    likes_num: int = Field()
    created: datetime = Field()
    updated: datetime = Field()

    class Config:
        from_attributes = True


__all__ = ["SummaryCommentSchema"]
