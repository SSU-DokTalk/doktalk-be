from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, DATETIME

from app.db.session import Base
from app.model.SummaryCommentLike import SummaryCommentLike


class SummaryComment(Base):
    __tablename__ = "summary_comment"

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )
    summary_id: Union[int, Column] = Column(
        BIGINT(unsigned=True), ForeignKey("summary.id"), nullable=False
    )

    # Fields
    content: Union[str, Column] = Column(VARCHAR(1024), nullable=False)
    likes_num: Union[int, Column] = Column(
        INTEGER, nullable=False, default=0, server_default="0"
    )
    created_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )
    updated_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Refs
    summary_comment_likes = relationship(
        "SummaryCommentLike", backref="summary_comment"
    )
