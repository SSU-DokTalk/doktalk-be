from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy_utils import Timestamp

from app.db.session import Base, LikeBase
from app.model.DebateCommentLike import DebateCommentLike


class DebateComment(Base, Timestamp, LikeBase):
    __tablename__ = "debate_comment"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreateDebateCommentReq":
            user = kwargs["user"]
            debate_comment_data = kwargs["data"]
            debate_id = kwargs["debate_id"]
            self.user_id = user.id
            self.debate_id = debate_id
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

    # Fields
    content: Union[str, Column] = Column(VARCHAR(1024), nullable=False)

    # Refs
    debate_comment_likes = relationship(
        "DebateCommentLike", backref="debate_comment", cascade="all, delete-orphan"
    )
