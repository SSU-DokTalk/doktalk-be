from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db.models.soft_delete import BaseSession

from app.core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DB_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=BaseSession
)

Base = declarative_base()

__all__ = [
    "Base",
    "SessionLocal",
]
