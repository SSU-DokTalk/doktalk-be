from datetime import date
from typing import Union

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATE

from app.db.session import Base


class Book(Base):
    __tablename__ = "book"

    def __init__(self, **kwargs):
        class_name = kwargs["data"].__class__.__name__
        if class_name == "BookAPIResponseSchema":
            if len(kwargs["data"].items) == 0:
                return None
            book_data = kwargs["data"].items[0]
            self.isbn = book_data.isbn
            self.title = book_data.title
            self.image = book_data.image
            self.author = book_data.author
            self.publisher = book_data.publisher
            self.pubdate = book_data.pubdate
            self.description = book_data.description

    # Keys
    isbn: Union[int, Column] = Column(BIGINT(unsigned=True), primary_key=True)

    # Fields
    title: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    image: Union[str, Column] = Column(VARCHAR(255))
    author: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    publisher: Union[str, Column] = Column(VARCHAR(255), nullable=False)
    pubdate: Union[date, Column] = Column(DATE(), nullable=False)
    description: Union[str, Column] = Column(VARCHAR(2000))
    in_library_num: Union[int, Column] = Column(
        BIGINT(unsigned=True), default=0, nullable=False, server_default="0"
    )

    # Refs
    my_books = relationship("MyBook", backref="book", cascade="all, delete-orphan")
    debates = relationship("Debate", backref="book", cascade="all, delete-orphan")
    summaries = relationship("Summary", backref="book", cascade="all, delete-orphan")


__all__ = ["Book"]
