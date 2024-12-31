from typing import Generator

from app.db.session import SessionLocal
from app.db.soft_delete import BaseSession as Session


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["get_db"]
