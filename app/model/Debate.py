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

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreateDebateReq":
            user = kwargs["user"]
            debate_data = kwargs["data"]
            self.user_id = user.id
            self.isbn = debate_data.isbn
            self.location = debate_data.location
            self.held_at = debate_data.held_at
            self.title = debate_data.title
            self.content = debate_data.content
            self.image1 = debate_data.image1
            self.image2 = debate_data.image2

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
        DATETIME, nullable=False, server_default=func.now()
    )

    # Refs
    debate_comments = relationship(
        "DebateComment", backref="debate", cascade="all, delete-orphan"
    )
    debate_likes = relationship(
        "DebateLike", backref="debate", cascade="all, delete-orphan"
    )
