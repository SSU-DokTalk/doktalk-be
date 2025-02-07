from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, TEXT
from sqlalchemy_utils import Timestamp

from app.db.session import Base
from app.db.models.postlike import PostlikeEntityBase
from app.db.models.files import FilesEntityBase
from app.model import PostComment, PostLike


class Post(Base, Timestamp, PostlikeEntityBase, FilesEntityBase):
    __tablename__ = "post"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreatePostReq":
            user = kwargs["user"]
            post_data = kwargs["data"]
            self.user_id = user.id
            self.title = post_data.title
            self.content = post_data.content
            if post_data.files:
                self.files = [
                    {"name": file.name, "url": str(file.url)}
                    for file in post_data.files
                ]

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # Fields
    title: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    content: Union[str, Column] = Column(TEXT)

    # Refs
    post_comments = relationship(
        "PostComment", backref="post", cascade="all, delete-orphan"
    )
    post_likes = relationship("PostLike", backref="post", cascade="all, delete-orphan")


__all__ = ["Post"]
