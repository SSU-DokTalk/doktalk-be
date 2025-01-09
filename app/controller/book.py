from typing import Literal

from fastapi import APIRouter

from app.schema.book_api import BookAPIResponseSchema
from app.service.book_api import *

router = APIRouter()


###########
### GET ###
###########
@router.get("s")
def getBooksController(
    query: str, start: int = 1, sort: Literal["sim", "date"] = "sim"
) -> BookAPIResponseSchema:
    return getAPIBooksService(query, start, sort)


@router.get("/{isbn}")
def getBookDetailController(isbn: str) -> BookAPIResponseSchema:
    return getAPIBookDetailService(isbn)
