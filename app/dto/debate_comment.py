from typing import Optional

from pydantic import BaseModel, Field

from app.schema.debate_comment import DabateCommentSchema
from app.schema.user import BasicUserSchema


class CreateDebateCommentReq(BaseModel):
    upper_comment_id: Optional[int] = None
    content: str = Field()


class BasicDebateComment(DabateCommentSchema):
    user: BasicUserSchema = Field()

    class Config:
        from_attributes = True


__all__ = ["CreateDebateCommentReq", "BasicDebateComment"]
