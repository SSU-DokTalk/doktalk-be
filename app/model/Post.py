from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, TEXT, DATETIME

from app.db.session import Base
from app.model.PostComment import PostComment
from app.model.PostLike import PostLike


class Post(Base):
    __tablename__ = "post"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreatePostReq":
            user = kwargs["user"]
            post_data = kwargs["data"]
            self.user_id = user.id
            self.title = post_data.title
            self.content = post_data.content
            self.image1 = post_data.image1
            self.image2 = post_data.image2

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )

    # Fields
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
    post_comments = relationship("PostComment", backref="post")
    post_likes = relationship("PostLike", backref="post")
