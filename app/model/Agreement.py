from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, BIT
from sqlalchemy_utils import Timestamp

from app.db.session import Base


class Agreement(Base, Timestamp):
    __tablename__ = "agreement"

    # Keys
    id: Union[int, Column] = Column(INTEGER(unsigned=True), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # Fields
    ## 동의한 약관을 비트로 표현
    term: Union[int, Column] = Column(BIT(3), nullable=False)

    # Refs
