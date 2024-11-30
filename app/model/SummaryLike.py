from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from app.db.session import Base


class SummaryLike(Base):
    __tablename__ = "summary_like"

    # Keys
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False, primary_key=True
    )
    summary_id: Union[int, Column] = Column(
        BIGINT(unsigned=True),
        ForeignKey("summary.id"),
        nullable=False,
        primary_key=True,
    )

    # Fields

    # Refs
