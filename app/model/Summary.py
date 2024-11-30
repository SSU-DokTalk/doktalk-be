from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR, JSON, DATETIME

from app.db.session import Base
from app.model.SummaryComment import SummaryComment
from app.model.SummaryLike import SummaryLike


class Summary(Base):
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
            self.image1 = summary_data.image1
            self.image2 = summary_data.image2

    # Keys
    id: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )

    # Fields
    isbn: Union[str, Column] = Column(VARCHAR(13), nullable=False)
    title: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    free_content: Union[list[str], Column] = Column(JSON)
    charged_content: Union[list[str], Column] = Column(JSON)
    price: Union[int, Column] = Column(
        INTEGER, nullable=False, default=0, server_default="0"
    )
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
    summary_comments = relationship(
        "SummaryComment", backref="summary", cascade="all, delete-orphan"
    )
    summary_likes = relationship(
        "SummaryLike", backref="summary", cascade="all, delete-orphan"
    )
