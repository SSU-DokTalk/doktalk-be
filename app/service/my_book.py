from fastapi import HTTPException

from app.db.models.soft_delete import BaseSession as Session
from app.model import MyBook, Book
from app.service.book_api import getAPIBookDetailService
from app.schema.book_api import BookAPIResponseSchema


def isInLibraryService(user_id: int, ids: list[int], db: Session) -> list[bool]:
    if ids is None or len(ids) == 0:
        return []
    res = db.query(MyBook).filter(MyBook.user_id == user_id, MyBook.isbn.in_(ids)).all()
    isbns = [r.isbn for r in res]
    return [isbn in isbns for isbn in ids]


def addMyBookService(user_id: int, isbn: int, db: Session) -> int:
    bookResponse = getAPIBookDetailService(isbn)
    if bookResponse["total"] == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    book = db.query(Book).filter(Book.isbn == isbn).one_or_none()
    if book is None:
        book = Book(data=BookAPIResponseSchema(**bookResponse))
        db.add(book)
        db.commit()
        db.refresh(book)

    my_book = MyBook(user_id=user_id, isbn=isbn)
    try:
        db.add(my_book)
        db.commit()
        db.refresh(my_book)
        book.in_library_num += 1
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=409, detail="MyBook already exists")
    return None


def deleteMyBookService(user_id: int, isbn: int, db: Session) -> None:
    book = db.query(Book).filter(Book.isbn == isbn).one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    res = (
        db.query(MyBook).filter(MyBook.user_id == user_id, MyBook.isbn == isbn).delete()
    )
    if res == 0:
        raise HTTPException(status_code=404, detail="MyBook not found")
    book.in_library_num -= 1
    db.commit()
    return None


__all__ = [
    "isInLibraryService",
    "addMyBookService",
    "deleteMyBookService",
]
