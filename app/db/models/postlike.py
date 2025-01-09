from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER


@as_declarative()
class PostlikeEntityBase:
    comments_num = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )
    likes_num = Column(
        INTEGER(unsigned=True), nullable=False, default=0, server_default="0"
    )


__all__ = [
    "PostlikeEntityBase",
]
