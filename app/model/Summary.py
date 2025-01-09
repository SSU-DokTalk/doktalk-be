from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, MEDIUMTEXT
from sqlalchemy_utils import Timestamp

from app.db.session import Base
from app.db.models.postlike import PostlikeEntityBase
from app.db.models.files import FilesEntityBase
from app.model.SummaryComment import SummaryComment
from app.model.SummaryLike import SummaryLike


class Summary(Base, Timestamp, PostlikeEntityBase, FilesEntityBase):
    __tablename__ = "summary"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "CreateSummaryReq":
            user = kwargs["user"]
            summary_data = kwargs["data"]
            self.user_id = user.id
            self.isbn = summary_data.isbn
            self.title = summary_data.title
            self.free_content = summary_data.free_content
            self.charged_content = summary_data.charged_content
            self.price = summary_data.price
            if summary_data.files:
                self.files = [str(file) for file in summary_data.files]

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    isbn: Union[int, Column] = Column(
        BIGINT(unsigned=True),
        ForeignKey("book.isbn", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # Fields
    title: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    free_content: Union[str, Column] = Column(VARCHAR(1000))
    charged_content: Union[str, Column] = Column(MEDIUMTEXT)
    price: Union[int, Column] = Column(
        INTEGER, nullable=False, default=0, server_default="0"
    )

    # Refs
    summary_comments = relationship(
        "SummaryComment", backref="summary", cascade="all, delete-orphan"
    )
    summary_likes = relationship(
        "SummaryLike", backref="summary", cascade="all, delete-orphan"
    )


__all__ = ["Summary"]
