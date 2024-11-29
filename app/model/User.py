from datetime import datetime
from typing import Union

from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import (
    INTEGER,
    VARCHAR,
    DATETIME,
    BOOLEAN,
    ENUM,
)
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.model.OAuth import OAuth
from app.model.Agreement import Agreement
from app.model.Post import Post
from app.model.PostComment import PostComment
from app.model.PostLike import PostLike
from app.model.Summary import Summary
from app.model.SummaryComment import SummaryComment
from app.model.SummaryCommentLike import SummaryCommentLike
from app.model.Debate import Debate
from app.model.DebateComment import DebateComment
from app.model.DebateLike import DebateLike
from app.model.DebateCommentLike import DebateCommentLike
from app.model.MyBook import MyBook
from app.enums import ROLE


class User(Base):
    __tablename__ = "user"

    def __init__(self, data):
        if data.__class__.__name__ == "BasicRegisterReq":
            self.email = data.email
            self.password = data.password
            self.profile = data.profile
            self.name = data.name
            self.gender = data.gender
            self.age = data.age

    # Keys
    id: Union[int, Column] = Column(INTEGER(unsigned=True), primary_key=True)

    # Fields
    email: Union[str, Column] = Column(VARCHAR(255), unique=True, nullable=False)
    password: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    profile: Union[str, Column] = Column(VARCHAR(255))
    name: Union[str, Column] = Column(VARCHAR(255))
    gender: Union[bool, Column] = Column(BOOLEAN)
    birthday: Union[datetime, Column] = Column(DATETIME)
    introduction: Union[str, Column] = Column(VARCHAR(255))
    follower_num: Union[int, Column] = Column(
        INTEGER, nullable=False, default=0, server_default="0"
    )
    following_num: Union[int, Column] = Column(
        INTEGER, nullable=False, default=0, server_default="0"
    )
    role: Union[ROLE, Column] = Column(
        ENUM(ROLE), nullable=False, default=ROLE.USER, server_default=ROLE.USER.name
    )
    created_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )
    updated_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    is_deleted: Union[bool, Column] = Column(BOOLEAN, nullable=False, default=False)

    # Refs
    oauths = relationship("OAuth", backref="user")
    agreements = relationship("Agreement", backref="user")
    posts = relationship("Post", backref="user")
    post_comments = relationship("PostComment", backref="user")
    post_likes = relationship("PostLike", backref="user")
    summaries = relationship("Summary", backref="user")
    summary_comments = relationship("SummaryComment", backref="user")
    summary_comment_likes = relationship("SummaryCommentLike", backref="user")
    debates = relationship("Debate", backref="user")
    debate_comments = relationship("DebateComment", backref="user")
    debate_likes = relationship("DebateLike", backref="user")
    debate_comment_likes = relationship("DebateCommentLike", backref="user")
    my_books = relationship("MyBook", backref="user")
