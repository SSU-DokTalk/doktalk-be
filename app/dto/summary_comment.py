from pydantic import BaseModel, Field

from app.schema.summary_comment import SummaryCommentSchema
from app.schema.user import BasicUserSchema


class CreateSummaryCommentReq(BaseModel):
    content: str = Field()

    class Config:
        from_attributes = True


class SummaryComment(SummaryCommentSchema):
    user: BasicUserSchema = Field()

    class Config:
        from_attributes = True


__all__ = ["CreateSummaryCommentReq"]
