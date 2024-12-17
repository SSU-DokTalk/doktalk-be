from pydantic import BaseModel, Field

from app.schema.debate_comment import DabateCommentSchema
from app.schema.user import BasicUserSchema


class CreateDebateCommentReq(BaseModel):
    content: str = Field()


class DebateComment(DabateCommentSchema):
    user: BasicUserSchema = Field()

    class Config:
        from_attributes = True


__all__ = ["CreateDebateCommentReq", "DebateComment"]
