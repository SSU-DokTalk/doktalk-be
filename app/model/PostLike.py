from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.db.session import Base


class PostLike(Base):
    __tablename__ = "post_like"

    # Keys
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False, primary_key=True
    )
    post_id: Union[int, Column] = Column(
        BIGINT(unsigned=True), ForeignKey("post.id"), nullable=False, primary_key=True
    )

    # Fields

    # Refs
