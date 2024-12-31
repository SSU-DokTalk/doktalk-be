import urllib.parse
import urllib.request
from typing import Literal
import json

from fastapi import HTTPException

from app.core.config import settings
from app.schema.book import BookResponseSchema

NAVER_BOOK_API_BASE_URL = "https://openapi.naver.com/v1/search"


def getBooksService(
    query: str, start: int = 1, sort: Literal["sim", "date"] = "sim"
) -> BookResponseSchema:
    query = urllib.parse.quote(query)
    url = f"{NAVER_BOOK_API_BASE_URL}/book.json?query={query}&display=10&start={start}&sort={sort}"
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", settings.NAVER_CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", settings.NAVER_CLIENT_SECRET)
    res = urllib.request.urlopen(req)
    if res.getcode() != 200:
        raise HTTPException(f"Naver Book API Error {res.getcode()}")
    data = json.loads(res.read().decode("utf-8"))
    return data


def getBookDetailService(isbn: str) -> BookResponseSchema:
    url = f"{NAVER_BOOK_API_BASE_URL}/book_adv.json?d_isbn={isbn}&display=1&start=1"
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", settings.NAVER_CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", settings.NAVER_CLIENT_SECRET)
    res = urllib.request.urlopen(req)
    if res.getcode() != 200:
        raise HTTPException(f"Naver Book API Error {res.getcode()}")
    data = json.loads(res.read().decode("utf-8"))
    return data


__all__ = [
    "getBooksService",
    "getBookDetailService",
]
