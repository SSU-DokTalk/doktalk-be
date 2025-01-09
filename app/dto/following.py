from typing import Optional

from app.schema.user import BasicUserSchema
from app.schema.following import FollowingSchema


class BasicFollowingSchema(FollowingSchema):
    following: Optional[BasicUserSchema] = None

    class Config:
        from_attributes = True


class BasicFollowerSchema(FollowingSchema):
    follower: Optional[BasicUserSchema] = None

    class Config:
        from_attributes = True


__all__ = ["BasicFollowingSchema", "BasicFollowerSchema"]
