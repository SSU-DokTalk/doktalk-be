from pydantic import BaseModel, Field


class PostCommentLikeSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    post_comment_id: int = Field()

    class Config:
        from_attributes = True
