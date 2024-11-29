from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.db.session import Base


class DebateCommentLike(Base):
    __tablename__ = "debate_comment_like"

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )
    debate_comment_id: Union[int, Column] = Column(
        BIGINT(unsigned=True), ForeignKey("debate_comment.id"), nullable=False
    )

    # Fields

    # Refs