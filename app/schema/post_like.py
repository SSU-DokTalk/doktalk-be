from pydantic import BaseModel, Field


class PostLikeSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    post_id: int = Field()

    class Config:
        from_attributes = True
