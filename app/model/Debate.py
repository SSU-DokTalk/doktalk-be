from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, TEXT, DATETIME

from app.db.session import Base

from app.model.DebateComment import DebateComment
from app.model.DebateLike import DebateLike


class Debate(Base):
    __tablename__ = "debate"

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )

    # Fields
    isbn: Union[str, Column] = Column(VARCHAR(13), nullable=False)
    location: Union[str, Column] = Column(VARCHAR(255))
    held_at: Union[datetime, Column] = Column(DATETIME)
    title: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    content: Union[str, Column] = Column(TEXT)
    image1: Union[str, Column] = Column(VARCHAR(255))
    image2: Union[str, Column] = Column(VARCHAR(255))
    likes_num: Union[int, Column] = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )
    comments_num: Union[int, Column] = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )
    created_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )
    updated_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Refs
    debate_comments = relationship("DebateComment", backref="debate")
    debate_likes = relationship("DebateLike", backref="debate")
