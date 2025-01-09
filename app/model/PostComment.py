from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from sqlalchemy_utils import Timestamp

from app.db.session import Base
from app.db.models.postlike import PostlikeEntityBase
from app.model.PostCommentLike import PostCommentLike


class PostComment(Base, Timestamp, PostlikeEntityBase):
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
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    post_id: Union[int, Column] = Column(
        BIGINT(unsigned=True),
        ForeignKey("post.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    upper_comment_id: Union[int, Column] = Column(
        BIGINT(unsigned=True),
        ForeignKey("post_comment.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )

    # Fields
    content: Union[str, Column] = Column(VARCHAR(1024), nullable=False)

    # Refs
    lower_comments = relationship(
        "PostComment",
        backref="upper_comment",
        remote_side=[id],
        cascade="all, delete-orphan",
        single_parent=True,
    )
    post_comment_likes = relationship(
        "PostCommentLike", backref="post_comment", cascade="all, delete-orphan"
    )


__all__ = ["PostComment"]
