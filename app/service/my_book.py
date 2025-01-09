from fastapi import HTTPException

from app.db.models.soft_delete import BaseSession as Session
from app.model import MyBook
from app.service.book_api import getAPIBookDetailService


def addMyBookService(user_id: int, isbn: int, db: Session) -> int:
    bookResponse = getAPIBookDetailService(isbn)
    if bookResponse["total"] == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    my_book = MyBook(user_id=user_id, isbn=isbn)
    db.add(my_book)
    db.commit()
    db.refresh(my_book)
    return my_book.id
