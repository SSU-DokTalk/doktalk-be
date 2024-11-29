from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER, BIT, DATETIME

from app.db.session import Base


class Agreement(Base):
    __tablename__ = "agreement"

    # Keys
    id: Union[int, Column] = Column(INTEGER(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )

    # Fields
    term: Union[int, Column] = Column(BIT(3), nullable=False)
    created_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )
    updated_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Refs
