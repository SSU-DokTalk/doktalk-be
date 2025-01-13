import urllib.parse
import urllib.request
from typing import Literal
import json

from fastapi import HTTPException

from app.core.config import settings
from app.schema.book_api import BookAPIResponseSchema

NAVER_BOOK_API_BASE_URL = "https://openapi.naver.com/v1/search"


def getAPIBooksService(
    query: str, start: int = 1, sort: Literal["sim", "date"] = "sim"
) -> BookAPIResponseSchema:
    query = urllib.parse.quote(query)
    url = f"{NAVER_BOOK_API_BASE_URL}/book.json?query={query}&display=10&start={start}&sort={sort}"
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", settings.NAVER_CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", settings.NAVER_CLIENT_SECRET)
    res = urllib.request.urlopen(req)
    if res.getcode() != 200:
        raise HTTPException(f"Naver Book API Error {res.getcode()}")
    data = json.loads(res.read().decode("utf-8"))
    return {
        "total": data["total"],
        "items": data["items"],
        "page": data["start"],
        "pages": data["total"] // data["display"]
        + bool(data["total"] % data["display"]),
    }


def getAPIBookDetailService(isbn: str) -> BookAPIResponseSchema:
    url = f"{NAVER_BOOK_API_BASE_URL}/book_adv.json?d_isbn={isbn}&display=1&start=1"
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", settings.NAVER_CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", settings.NAVER_CLIENT_SECRET)
    res = urllib.request.urlopen(req)
    if res.getcode() != 200:
        raise HTTPException(f"Naver Book API Error {res.getcode()}")
    data = json.loads(res.read().decode("utf-8"))
    return {
        "total": data["total"],
        "items": data["items"],
        "page": data["start"],
        "pages": data["total"] // (data["display"] if data["display"] else 1)
        + bool(data["total"] % (data["display"] if data["display"] else 1)),
    }


__all__ = [
    "getAPIBooksService",
    "getAPIBookDetailService",
]
