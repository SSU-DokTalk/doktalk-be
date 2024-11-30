from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME, ENUM

from app.db.session import Base
from app.oauth.oauthSchema import PROVIDER


class OAuth(Base):
    __tablename__ = "oauth"

    def __init__(self, new_id: str, user_id: int, provider: PROVIDER):
        self.id = new_id
        self.user_id = user_id
        self.provider = provider

    # Keys
    id: Union[str, Column] = Column(VARCHAR(255), primary_key=True)
    user_id: Union[int, Column] = Column(
        INTEGER(unsigned=True), ForeignKey("user.id"), nullable=False
    )

    # Fields
    provider: Union[PROVIDER, Column] = Column(ENUM(PROVIDER), nullable=False)
    created_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )

    # Refs
