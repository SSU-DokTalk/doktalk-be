from sqlalchemy import Column, Integer, String

from app.db.session import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    author = Column(String(255))
    pages = Column(Integer)
