from pydantic import BaseModel, Field

from app.schema.post_comment import PostCommentSchema
from app.schema.user import BasicUserSchema


class CreatePostCommentReq(BaseModel):
    content: str = Field()


class PostComment(PostCommentSchema):
    user: BasicUserSchema = Field()

    class Config:
        from_attributes = True


__all__ = ["CreatePostCommentReq", "PostComment"]
