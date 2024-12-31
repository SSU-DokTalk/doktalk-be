from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, TEXT, DATETIME
from sqlalchemy_utils import Timestamp

from app.db.session import Base, CommentLikeBase
from app.model.DebateComment import DebateComment
from app.model.DebateLike import DebateLike


class Debate(Base, Timestamp, CommentLikeBase):
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
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # Fields
    ## 도서의 고유번호
    isbn: Union[str, Column] = Column(VARCHAR(13), nullable=False)
    ## 토론 장소
    location: Union[str, Column] = Column(VARCHAR(255))
    ## 토론 온라인 링크
    link: Union[str, Column] = Column(VARCHAR(255))
    ## 토론 일시
    held_at: Union[datetime, Column] = Column(DATETIME)
    title: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    content: Union[str, Column] = Column(TEXT)
    image1: Union[str, Column] = Column(VARCHAR(255))
    image2: Union[str, Column] = Column(VARCHAR(255))

    # Refs
    debate_comments = relationship(
        "DebateComment", backref="debate", cascade="all, delete-orphan"
    )
    debate_likes = relationship(
        "DebateLike", backref="debate", cascade="all, delete-orphan"
    )
