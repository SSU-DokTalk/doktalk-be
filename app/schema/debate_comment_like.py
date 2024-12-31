from pydantic import BaseModel, Field


class DebateCommentLikeSchema(BaseModel):
    user_id: int = Field()
    debate_comment_id: int = Field()

    class Config:
        from_attributes = True


__all__ = ["DebateCommentLikeSchema"]
