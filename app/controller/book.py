from typing import Literal

from fastapi import APIRouter

from app.schema.book import BookResponseSchema
from app.service.book import *

router = APIRouter()


###########
### GET ###
###########
@router.get("s")
def getBooksController(
    query: str, start: int = 1, sort: Literal["sim", "date"] = "sim"
) -> BookResponseSchema:
    return getBooksService(query, start, sort)


@router.get("/{isbn}")
def getBookDetailController(isbn: str) -> BookResponseSchema:
    return getBookDetailService(isbn)
