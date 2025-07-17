from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
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
    api_provider: Literal["naver", "google"] = "naver",
    db: Session = Depends(get_db),
) -> BookAPIResponseSchema:

    if api_provider == "naver":
        return getNaverAPIBooksService(search, db, page, size, sortby)
    elif api_provider == "google":
        return getGoogleAPIBooksService(search, db, page, size, sortby)

    raise HTTPException(status_code=400, detail="Invalid API Provider")


@router.get("/{isbn}")
def getBookDetailController(isbn: str) -> BookAPIResponseSchema:
    return getAPIBookDetailService(isbn)
