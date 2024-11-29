from datetime import datetime
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator, EmailStr, HttpUrl

from app.enums import ROLE


class BasicUserSchema(BaseModel):
    id: int = Field()

    profile: Optional[HttpUrl] = None
    name: Optional[str] = None
    role: ROLE = Field(default=ROLE.USER)
    is_deleted: bool = Field(default=False)

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: int = Field()

    email: EmailStr = Field(max_length=255)
    # password: str = Field(min_length=8, max_length=255)
    profile: Optional[HttpUrl] = None
    name: Optional[str] = None
    gender: Optional[bool] = None
    birthday: Optional[datetime] = None
    introduction: Optional[str] = None
    follower_num: int = Field()
    following_num: int = Field()
    role: ROLE = Field(default=ROLE.USER)
    created_at: datetime = Field()
    updated_at: datetime = Field()
    is_deleted: bool = Field(default=False)

    # oauths: Optional[List[oauthSchema]] = None
    # agreements: Optional[List[agreementSchema]] = None
    # posts: Optional[List[postSchema]] = None
    # post_comments: Optional[List[post_commentSchema]] = None
    # post_likes: Optional[List[post_likeSchema]] = None
    # summaries: Optional[List[summarieSchema]] = None
    # summary_comments: Optional[List[summary_commentSchema]] = None
    # summary_comment_likes: Optional[List[summary_comment_likeSchema]] = None
    # debates: Optional[List[debateSchema]] = None
    # debate_comments: Optional[List[debate_commentSchema]] = None
    # debate_likes: Optional[List[debate_likeSchema]] = None
    # debate_comment_likes: Optional[List[debate_comment_likeSchema]] = None
    # my_books: Optional[List[my_bookSchema]] = None

    # @field_validator("password")
    # def validate_password(cls, v):
    #     password_validation = re.compile(
    #         r"^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%*^&+=]).*$"
    #     )
    #     if not password_validation.fullmatch(v):
    #         raise ValueError("Invalid Password")
    #     return v

    class Config:
        from_attributes = True
