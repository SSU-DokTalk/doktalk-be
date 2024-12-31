from datetime import datetime
from typing import Union

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (
    INTEGER,
    VARCHAR,
    DATETIME,
    BOOLEAN,
    ENUM,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import Timestamp

from app.db.session import Base
from app.db.soft_delete import SoftDeleteMixin
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
from app.model.Purchase import Purchase
from app.model.Following import Following
from app.enums import ROLE


class User(Base, Timestamp, SoftDeleteMixin):
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

    # Refs
    oauths = relationship("OAuth", backref="user", cascade="all, delete-orphan")
    agreements = relationship("Agreement", backref="user", cascade="all, delete-orphan")
    posts = relationship("Post", backref="user", cascade="all, delete-orphan")
    post_comments = relationship(
        "PostComment", backref="user", cascade="all, delete-orphan"
    )
    post_likes = relationship("PostLike", backref="user", cascade="all, delete-orphan")
    summaries = relationship("Summary", backref="user", cascade="all, delete-orphan")
    summary_comments = relationship(
        "SummaryComment", backref="user", cascade="all, delete-orphan"
    )
    summary_comment_likes = relationship(
        "SummaryCommentLike", backref="user", cascade="all, delete-orphan"
    )
    debates = relationship("Debate", backref="user", cascade="all, delete-orphan")
    debate_comments = relationship(
        "DebateComment", backref="user", cascade="all, delete-orphan"
    )
    debate_likes = relationship(
        "DebateLike", backref="user", cascade="all, delete-orphan"
    )
    debate_comment_likes = relationship(
        "DebateCommentLike", backref="user", cascade="all, delete-orphan"
    )
    my_books = relationship("MyBook", backref="user")
    purchases = relationship("Purchase", backref="user")

    # Following relationships (users this user is following)
    following = relationship(
        "Following",
        foreign_keys="Following.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",  # Cascade 설정
    )

    # Follower relationships (users following this user)
    followers = relationship(
        "Following",
        foreign_keys="Following.following_id",
        back_populates="following",
        cascade="all, delete-orphan",  # Cascade 설정
    )
