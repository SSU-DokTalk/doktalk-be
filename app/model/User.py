from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from typing import Union
from datetime import datetime
from app.schema.user import BasicRegisterReq
from app.oauth.oauthSchema import PROVIDER


class User(Base):
    __tablename__ = "user"

    def __init__(self, user_data: BasicRegisterReq):
        self.email = user_data.email
        self.password = user_data.password
        self.name = user_data.name
        self.gender = user_data.gender
        self.age = user_data.age

    # Keys
    id: Union[int, Column] = Column(Integer, primary_key=True)

    # Fields
    email: Union[str, Column] = Column(String(255), unique=True, nullable=False)
    password: Union[str, Column] = Column(String(255), nullable=False)
    name: Union[str, Column] = Column(String(255))
    gender: Union[bool, Column] = Column(Boolean)
    age: Union[int, Column] = Column(Integer)
    createdAt: Union[datetime, Column] = Column(
        DateTime, nullable=False, server_default=func.now()
    )
    updatedAt: Union[datetime, Column] = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    isDeleted: Union[bool, Column] = Column(Boolean, nullable=False, default=False)

    # Refs
    oAuths = relationship("OAuth", back_populates="user")


class OAuth(Base):
    __tablename__ = "oauth"

    def __init__(self, new_id: str, new_userId: int, new_registration: PROVIDER):
        self.id = new_id
        self.userId = new_userId
        self.registration = new_registration

    # Keys
    id = Column(String(255), primary_key=True)
    userId = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="oAuths")

    # Fields
    registration = Column(String(255))
    createdAt: Union[datetime, Column] = Column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Refs
