from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from sqlalchemy_utils import Timestamp

from app.db.session import Base


class MyBook(Base, Timestamp):
    __tablename__ = "my_book"

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

    # Refs


__all__ = ["MyBook"]
