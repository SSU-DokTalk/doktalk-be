from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import Timestamp

from app.db.session import Base
from app.db.models.postlike import PostlikeEntityBase
from app.model.DebateCommentLike import DebateCommentLike


class DebateComment(Base, Timestamp, PostlikeEntityBase):
    __tablename__ = "debate_comment"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreateDebateCommentReq":
            user = kwargs["user"]
            debate_comment_data = kwargs["data"]
            debate_id = kwargs["debate_id"]
            self.user_id = user.id
            self.debate_id = debate_id
            self.upper_comment_id = debate_comment_data.upper_comment_id
            self.content = debate_comment_data.content

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    debate_id: Union[int, Column] = Column(
        BIGINT(unsigned=True),
        ForeignKey("debate.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    upper_comment_id: Union[int, Column] = Column(
        BIGINT(unsigned=True),
        ForeignKey("debate_comment.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )

    # Fields
    content: Union[str, Column] = Column(VARCHAR(1024), nullable=False)

    # Refs
    lower_comments = relationship(
        "DebateComment",
        backref="upper_comment",
        remote_side=[id],
        cascade="all, delete-orphan",
        single_parent=True,
    )
    debate_comment_likes = relationship(
        "DebateCommentLike", backref="debate_comment", cascade="all, delete-orphan"
    )


__all__ = ["DebateComment"]
