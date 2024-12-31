from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base, as_declarative
from sqlalchemy.orm import sessionmaker
from app.db.soft_delete import BaseSession

from app.core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DB_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=BaseSession
)

Base = declarative_base()


@as_declarative()
class CommentBase:
    comments_num = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )


@as_declarative()
class LikeBase:
    likes_num = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )


@as_declarative()
class CommentLikeBase:
    comments_num = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )
    likes_num = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )


__all__ = ["Base", "SessionLocal", "CommentBase", "LikeBase", "CommentLikeBase"]
