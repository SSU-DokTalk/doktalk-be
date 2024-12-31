from pydantic import BaseModel, Field


class PostLikeSchema(BaseModel):
    user_id: int = Field()
    post_id: int = Field()

    class Config:
        from_attributes = True


__all__ = ["PostLikeSchema"]
