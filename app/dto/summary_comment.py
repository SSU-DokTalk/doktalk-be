from pydantic import BaseModel, Field

from app.schema.post_comment import PostCommentSchema
from app.schema.user import BasicUserSchema


class CreateSummaryCommentReq(BaseModel):
    content: str = Field()


__all__ = ["CreateSummaryCommentReq"]
