from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER, DATETIME
from sqlalchemy.orm import relationship

from app.db.session import Base


class Following(Base):
    __tablename__ = "following"

    follower_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False, primary_key=True
    )
    following_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False, primary_key=True
    )
    created_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )

    # Relationship to the User model
    follower = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following",
    )
    following = relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followers",
    )
