from typing import Optional
from pydantic import BaseModel, Field

from app.schema.post_comment import PostCommentSchema
from app.schema.user import BasicUserSchema


class CreatePostCommentReq(BaseModel):
    upper_comment_id: Optional[int] = None
    content: str = Field()


class BasicPostComment(PostCommentSchema):
    user: BasicUserSchema = Field()

    class Config:
        from_attributes = True


__all__ = ["CreatePostCommentReq", "PostComment"]
