from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from sqlalchemy_utils import Timestamp

from app.db.session import Base, LikeBase
from app.model.SummaryCommentLike import SummaryCommentLike


class SummaryComment(Base, Timestamp, LikeBase):
    __tablename__ = "summary_comment"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreateSummaryCommentReq":
            user = kwargs["user"]
            summary_comment_data = kwargs["data"]
            summary_id = kwargs["summary_id"]
            self.user_id = user.id
            self.summary_id = summary_id
            self.content = summary_comment_data.content

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    summary_id: Union[int, Column] = Column(
        BIGINT(unsigned=True),
        ForeignKey("summary.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # Fields
    content: Union[str, Column] = Column(VARCHAR(1024), nullable=False)

    # Refs
    summary_comment_likes = relationship(
        "SummaryCommentLike", backref="summary_comment", cascade="all, delete-orphan"
    )
