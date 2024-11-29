from datetime import datetime
from typing import Union

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME

from app.db.session import Base
from app.oauth.oauthSchema import PROVIDER


class OAuth(Base):
    __tablename__ = "oauth"

    def __init__(self, new_id: str, new_user_id: int, new_registration: PROVIDER):
        self.id = new_id
        self.user_id = new_user_id
        self.registration = new_registration

    # Keys
    id: Union[str, Column] = Column(VARCHAR(255), primary_key=True)
    user_id: Union[int, Column] = Column(INTEGER(unsigned=True), ForeignKey("user.id"))

    # Fields
    registration: Union[str, Column] = Column(VARCHAR(255))
    created_at: Union[datetime, Column] = Column(
        DATETIME, nullable=False, server_default=func.now()
    )

    # Refs
