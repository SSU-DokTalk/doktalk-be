from fastapi import HTTPException

from app.db.models.soft_delete import BaseSession as Session
from app.schema.book_api import BookAPIResponseSchema
from app.model import (
    Book,
)
from app.service.book_api import getAPIBookDetailService


def getOrCreateBook(isbn: str, db: Session) -> Book:
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if book is None:
        try:
            bookData = BookAPIResponseSchema(
                **getAPIBookDetailService(isbn)
            )
            book = Book(data=bookData)

            if book == None:
                raise HTTPException(status_code=404, detail="Book not found")
            db.add(book)
            db.commit()

        except HTTPException as e:
            # Re-raise HTTPException from book fetching
            raise e
        except Exception as e:
            # Handle potential errors during API call or Book creation
            # Consider logging the error e
            raise HTTPException(
                status_code=500, detail=f"Failed to fetch or create book details for ISBN {isbn}")

    return book
