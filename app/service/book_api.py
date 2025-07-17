import urllib.parse
import urllib.request
from typing import Literal
import json
import requests

from fastapi import HTTPException
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.config import settings
from app.model.Book import Book
from app.schema.book_api import BookAPIResponseSchema

NAVER_BOOK_API_BASE_URL = "https://openapi.naver.com/v1/search"


def getNaverAPIBooksService(
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
            req.add_header("X-Naver-Client-Secret",
                           settings.NAVER_CLIENT_SECRET)
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
                + bool(data["total"] %
                       (data["display"] if data["display"] else 1)),
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


def getGoogleAPIBooksService(
    query: str,
    db: Session,
    start: int = 1,  # Google Books API의 startIndex에 해당
    size: int = 10,  # Google Books API의 maxResults에 해당
    # Google Books API는 정렬 옵션이 제한적
    sort: Literal["latest", "popular"] = "latest"
) -> BookAPIResponseSchema:
    """
    Google Books API를 사용하여 책을 검색하고, 요청된 형식의 응답을 반환합니다.
    isbn이 없는 책 정보들은 건너뜁니다.

    Args:
        query (str): 검색할 책 제목, 저자 등.
        db (Session): SQLAlchemy DB 세션 (현재 함수에서는 사용되지 않음).
        start (int): 검색 결과 시작 인덱스 (1부터 시작).
        size (int): 한 페이지에 반환할 최대 결과 수.
        sort (Literal["latest", "popular"]): 정렬 방식 (Google Books API는 "relevance", "newest"만 지원).
                                              "latest"는 "newest"로 매핑됩니다.

    Returns:
        BookAPIResponseSchema: 요청된 형식의 책 검색 결과 (딕셔너리).

    Raises:
        HTTPException: Google Books API 호출 중 오류가 발생할 경우.
    """
    GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

    # Google Books API의 정렬 방식 매핑
    # 'popular'는 Google API에서 직접 지원하지 않아 'relevance'로 대체합니다.
    order_by = "newest" if sort == "latest" else "relevance"

    # Google Books API는 0부터 시작하는 startIndex를 사용합니다.
    # 클라이언트의 start (1부터 시작)를 0부터 시작하는 인덱스로 변환합니다.
    start_index = max(0, (start - 1) * size)

    params = {
        "q": query,
        "startIndex": start_index,
        "maxResults": size,
        "orderBy": order_by,
    }

    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()  # HTTP 오류 (4xx, 5xx) 발생 시 예외 발생

        google_data: Dict[str, Any] = response.json()

        total_items: int = google_data.get("totalItems", 0)
        items: List[BookItem] = []

        if google_data.get("items"):
            for book_item in google_data["items"]:
                book_item = googleBookDataToBookAPIResponseSchema(book_item)

                if book_item['isbn'] is None:
                    continue  # ISBN이 없으면 건너뜀

                # in library num
                if db:
                    book = (
                        db.query(Book)
                        .filter(Book.isbn.in_([book_item['isbn']]))
                        .first()
                    )
                    if book:
                        book_item['in_library_num'] = book.in_library_num

                # 요청된 형식에 맞춰 데이터 매핑
                items.append(book_item)

        # 총 페이지 수 계산
        # total_items가 0일 경우, pages도 0이 되도록 처리
        pages = (total_items + size - 1) // size if total_items > 0 else 0

        return {
            "total": total_items,
            "items": items,
            "page": start,
            "pages": pages,
        }

    except requests.exceptions.HTTPStatusError as e:
        # HTTP 4xx/5xx 오류 처리
        print(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code,
                            detail=f"Google Book API HTTP Error: {e.response.text}")
    except requests.exceptions.RequestException as e:
        # 네트워크 관련 오류 (연결 끊김, DNS 오류 등) 처리
        print(f"An error occurred while requesting Google Books API: {e}")
        raise HTTPException(
            status_code=500, detail=f"Google Book API Request Error: {e}")
    except Exception as e:
        # 그 외 예상치 못한 오류 처리
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500, detail=f"Google Book API Processing Error: {e}")


def getAPIBookDetailService(isbn: str) -> BookAPIResponseSchema:
    url = f"{NAVER_BOOK_API_BASE_URL}/book_adv.json?d_isbn={isbn}&display=1&start=1"
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", settings.NAVER_CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", settings.NAVER_CLIENT_SECRET)
    res = urllib.request.urlopen(req)
    if res.getcode() != 200:
        raise HTTPException(f"Naver Book API Error {res.getcode()}")
    data = json.loads(res.read().decode("utf-8"))

    if data["total"] > 0:
        return {
            "total": data["total"],
            "items": data["items"],
            "page": data["start"],
            "pages": data["total"] // (data["display"] if data["display"] else 1)
            + bool(data["total"] %
                   (data["display"] if data["display"] else 1)),
        }

    # Naver에 없는경우 Google Books API로 검색
    return getGoogleAPIBooksService(f"isbn:{isbn}", None)


__all__ = [
    "getNaverAPIBooksService",
    "getGoogleAPIBooksService",
    "getAPIBookDetailService",
]


def googleBookDataToBookAPIResponseSchema(data: dict) -> BookAPIResponseSchema:
    volume_info: Dict[str, Any] = data.get("volumeInfo", {})

    # ISBN-13 추출 (여러 식별자 중 ISBN_13 타입 우선)
    isbn_13: Optional[int] = None
    industry_identifiers: Optional[List[Dict[str, str]]] = volume_info.get(
        "industryIdentifiers")
    if industry_identifiers:
        for identifier in industry_identifiers:
            if identifier.get("type") == "ISBN_13":
                isbn_13 = int(identifier.get("identifier"))
                break

    # pubdate YYYYMMDD 형식으로 변환
    pubdate_formatted: Optional[str] = None
    published_date: Optional[str] = volume_info.get(
        "publishedDate")
    if published_date:
        parts = published_date.split('-')
        if len(parts) == 3:  # YYYY-MM-DD
            pubdate_formatted = "".join(parts)
        elif len(parts) == 2:  # YYYY-MM
            pubdate_formatted = parts[0] + \
                parts[1] + "01"  # 일은 01로 가정
        elif len(parts) == 1:  # YYYY
            pubdate_formatted = parts[0] + "0101"  # 월/일은 01로 가정

    return {
        "title": volume_info.get("title"),
        "link": None,  # Google Books API는 직접적인 쇼핑 링크를 제공하지 않음
        "image": volume_info.get("imageLinks", {}).get("thumbnail"),
        "author": ", ".join(volume_info.get("authors", [])) if volume_info.get("authors") else None,
        "discount": None,  # Google Books API는 가격 정보를 제공하지 않음
        "publisher": volume_info.get("publisher"),
        "pubdate": pubdate_formatted,
        "isbn": isbn_13,
        "in_library_num": 0,
        "description": volume_info.get("description"),
    }
