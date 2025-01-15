from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schema.book_api import BookAPIResponseSchema
from app.service.book_api import *
from app.db.connection import get_db

router = APIRouter()


###########
### GET ###
###########
@router.get("s")
def getBooksController(
    search: str,
    page: int = 1,
    size: int = 10,
    sortby: Literal["latest", "popular"] = "latest",
    db: Session = Depends(get_db),
) -> BookAPIResponseSchema:
    return getAPIBooksService(search, db, page, size, sortby)


@router.get("/{isbn}")
def getBookDetailController(isbn: str) -> BookAPIResponseSchema:
    return getAPIBookDetailService(isbn)
