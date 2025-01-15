import urllib.parse
import urllib.request
from typing import Literal
import json

from fastapi import HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.config import settings
from app.model.Book import Book
from app.schema.book_api import BookAPIResponseSchema

NAVER_BOOK_API_BASE_URL = "https://openapi.naver.com/v1/search"


def getAPIBooksService(
    query: str,
    db: Session,
    start: int = 1,
    size: int = 10,
    sort: Literal["latest", "popular"] = "latest",
) -> BookAPIResponseSchema:
    if sort == "latest":
        query = urllib.parse.quote(query)
        try:
            if query == "":
                return {
                    "total": 0,
                    "items": [],
                    "page": 1,
                    "pages": 0,
                }
            sort = "date"
            url = f"{NAVER_BOOK_API_BASE_URL}/book.json?query={query}&display={size}&start={start*size}&sort={sort}"
            req = urllib.request.Request(url)
            req.add_header("X-Naver-Client-Id", settings.NAVER_CLIENT_ID)
            req.add_header("X-Naver-Client-Secret", settings.NAVER_CLIENT_SECRET)
            res = urllib.request.urlopen(req)
            if res.getcode() != 200:
                raise HTTPException(f"Naver Book API Error {res.getcode()}")
            data = json.loads(res.read().decode("utf-8"))
            data["items"] = [
                item for item in data["items"] if len(item.get("isbn")) == 13
            ]
            books = (
                db.query(Book)
                .filter(Book.isbn.in_([item.get("isbn") for item in data["items"]]))
                .all()
            )
            isbns = [str(book.isbn) for book in books]
            for item in data["items"]:
                if item.get("isbn") in isbns:
                    item["in_library_num"] = books[
                        isbns.index(item["isbn"])
                    ].in_library_num
                else:
                    item["in_library_num"] = 0
            return {
                "total": data["total"],
                "items": data["items"],
                "page": data["start"] // (data["display"] if data["display"] else 1),
                "pages": data["total"] // (data["display"] if data["display"] else 1)
                + bool(data["total"] % (data["display"] if data["display"] else 1)),
            }
        except Exception as e:
            raise HTTPException(400, detail="Naver Book API Error")
    elif sort == "popular":
        sort = "sim"
        try:
            query = urllib.parse.unquote(query)
            conditions = [
                func.instr(func.lower(Book.title), keyword) > 0
                for keyword in query.lower().split()
            ]
            res = paginate(
                db.query(Book)
                .filter(*conditions)
                .order_by(Book.in_library_num.desc(), Book.pubdate.desc()),
                Params(size=size, page=start),
            )
            for item in res.items:
                item.isbn = str(item.isbn)
                item.pubdate = item.pubdate.strftime("%Y%m%d")
            return {
                "total": res.total,
                "items": res.items,
                "page": res.page,
                "pages": res.pages,
            }
        except Exception as e:
            print(e)
            raise HTTPException(400, detail="")


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
