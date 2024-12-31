from typing import Union

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, ENUM
from sqlalchemy_utils import Timestamp

from app.db.session import Base
from app.oauth.oauthSchema import PROVIDER


class OAuth(Base, Timestamp):
    __tablename__ = "oauth"

    def __init__(self, new_id: str, user_id: int, provider: PROVIDER):
        self.id = new_id
        self.user_id = user_id
        self.provider = provider

    # Keys
    id: Union[str, Column] = Column(VARCHAR(255), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True),
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # Fields
    provider: Union[PROVIDER, Column] = Column(ENUM(PROVIDER), nullable=False)

    # Refs
