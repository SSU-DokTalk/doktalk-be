from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, DATETIME

from app.db.session import Base
from app.model.DebateCommentLike import DebateCommentLike


class DebateComment(Base):
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
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )
    debate_id: Union[int, Column] = Column(
        BIGINT(unsigned=True), ForeignKey("debate.id"), nullable=False
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
    debate_comment_likes = relationship(
        "DebateCommentLike", backref="debate_comment", cascade="all, delete-orphan"
    )
