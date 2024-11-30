from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, DATETIME

from app.db.session import Base
from app.model.PostCommentLike import PostCommentLike


class PostComment(Base):
    __tablename__ = "post_comment"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreatePostCommentReq":
            user = kwargs["user"]
            post_comment_data = kwargs["data"]
            post_id = kwargs["post_id"]
            self.user_id = user.id
            self.post_id = post_id
            self.content = post_comment_data.content

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )
    post_id: Union[int, Column] = Column(
        BIGINT(unsigned=True), ForeignKey("post.id"), nullable=False
    )

    # Fields
    content: Union[str, Column] = Column(VARCHAR(1024), nullable=False)
    likes_num: Union[int, Column] = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )
    created_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )
    updated_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )

    # Refs
    post_comment_likes = relationship(
        "PostCommentLike", backref="post_comment", cascade="all, delete-orphan"
    )
