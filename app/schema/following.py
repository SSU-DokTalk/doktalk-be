from datetime import datetime

from pydantic import BaseModel, Field


class FollowingSchema(BaseModel):
    follower_id: int = Field()
    following_id: int = Field()
    created: datetime = Field()

    class Config:
        from_attributes = True
