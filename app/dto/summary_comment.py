from pydantic import BaseModel, Field

from app.schema.summary_comment import SummaryCommentSchema
from app.schema.user import BasicUserSchema


class CreateSummaryCommentReq(BaseModel):
    upper_comment_id: int = Field()
    content: str = Field()

    class Config:
        from_attributes = True


class BasicSummaryComment(SummaryCommentSchema):
    user: BasicUserSchema = Field()

    class Config:
        from_attributes = True


__all__ = ["CreateSummaryCommentReq", "BasicSummaryComment"]
