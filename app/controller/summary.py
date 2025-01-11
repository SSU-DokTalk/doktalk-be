from typing import Annotated, Literal, List, Union

from fastapi import APIRouter, Depends, Request, Query
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, literal
from sqlalchemy.orm import contains_eager

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.db.models.soft_delete import BaseSession as Session
from app.dto.summary import *
from app.dto.summary_comment import *
from app.function.generate_dummy import generate_sentence
from app.model import Summary, Book
from app.service.summary import *

router = APIRouter()


###########
### GET ###
###########
@router.get("", response_model=Page[BasicSummaryRes])
def getSummaryListController(
    search: str = "",
    searchby: Literal["bkt", "smt"] = "bkt",
    sort: Literal["latest", "popular"] = "latest",
    lang: Literal["ko", "en"] = "ko",
    db: Session = Depends(get_db),
) -> List[BasicSummaryRes]:
    """
    요약 리스트 조회
    """

    conditions = list()
    if searchby == "bkt":
        conditions = [
            func.instr(func.lower(Book.title), keyword) > 0
            for keyword in search.lower().split()
        ]
    elif searchby == "smt":
        conditions = [
            func.instr(func.lower(Summary.title), keyword) > 0
            for keyword in search.lower().split()
        ]

    order_by = []
    if sort == "popular":
        order_by.append(Summary.like_count.desc())
    # elif sort == "latest":
    order_by.append(Summary.created.desc())

    print(conditions)
    summaries = paginate(
        db.query(Summary)
        .join(Summary.book)
        .filter(*conditions)
        .options(contains_eager(Summary.book))
        .order_by(*order_by)
    )

    # Charged content를 마스킹
    for items in summaries.items:
        items.charged_content = generate_sentence(items.charged_content[:200], lang)
        print(items.charged_content)
    return summaries


@router.get("/recent", response_model=Page[BasicSummaryRes])
def getRecentSummaryListController(
    lang: Literal["ko", "en"] = "ko",
    db: Session = Depends(get_db),
) -> List[BasicSummaryRes]:
    """
    최근 요약 리스트 조회
    """
    summaries = paginate(
        db.query(Summary)
        .join(Summary.book)
        .options(contains_eager(Summary.book))
        .order_by(Summary.created.desc())
    )

    # Charged content를 마스킹
    for items in summaries.items:
        items.charged_content = generate_sentence(items.charged_content[:200], lang)
    return summaries


@router.get("s/like")
def getSummaryLikeController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    ids: Union[List[int], None] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    요약의 좋아요 조회
    """
    return getSummaryLikeService(request.state.user.id, ids, db)


@router.get("/comments/like")
def getSummaryCommentLikeController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    summary_comment_ids: Union[List[int], None] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    요약의 댓글 좋아요 조회
    """
    return getSummaryCommentLikeService(request.state.user.id, summary_comment_ids, db)


@router.get("/{summary_id}")
def getSummaryController(
    summary_id: int, lang: Literal["ko", "en"] = "ko", db: Session = Depends(get_db)
) -> BasicSummaryRes:
    """
    단일 요약 조회
    """
    summary = getSummaryService(summary_id, db)
    summary.charged_content = generate_sentence(summary.charged_content[:200], lang)
    return BasicSummaryRes.model_validate(summary).model_dump()


@router.get("/{summary_id}/charged_content")
def getSummaryChargedContentController(
    request: Request,
    summary_id: int,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> str:
    """
    요약의 유료 컨텐츠 조회
    """
    return getSummaryChargedContentService(request.state.user.id, summary_id, db)


@router.get("/{summary_id}/comments")
def getSummaryCommentController(summary_id: int, db: Session = Depends(get_db)):
    """
    요약의 댓글 조회
    """
    return getSummaryCommentService(summary_id, db)


############
### POST ###
############
@router.post("")
def createSummaryController(
    summary_data: CreateSummaryReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    return createSummaryService(request.state.user, summary_data, db)


@router.post("/{summary_id}/comment")
def createSummaryCommentController(
    summary_id: int,
    summary_comment_data: CreateSummaryCommentReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    """
    요약의 댓글 작성
    """
    return createSummaryCommentService(
        request.state.user, summary_id, summary_comment_data, db
    )


@router.post("/{summary_id}/like")
def createSummaryLikeController(
    summary_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    요약에 좋아요 달기
    """
    return createSummaryLikeService(request.state.user, summary_id, db)


@router.post("/comment/{summary_comment_id}/like")
def createSummaryCommentLikeController(
    summary_comment_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    요약의 댓글에 좋아요 달기
    """
    return createSummaryCommentLikeService(request.state.user, summary_comment_id, db)


###########
### PUT ###
###########

#############
### PATCH ###
#############


##############
### DELETE ###
##############
@router.delete("/{summary_id}/like")
def deleteSummaryLikeController(
    summary_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    요약의 좋아요 삭제
    """
    return deleteSummaryLikeService(request.state.user.id, summary_id, db)


@router.delete("/comment/{summary_comment_id}")
def deleteSummaryCommentController(
    summary_comment_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    요약의 댓글 삭제
    """
    return deleteSummaryCommentService(request.state.user.id, summary_comment_id, db)


@router.delete("/comment/{summary_comment_id}/like")
def deleteSummaryCommentLikeController(
    summary_comment_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    요약의 댓글 좋아요 삭제
    """
    return deleteSummaryCommentLikeService(
        request.state.user.id, summary_comment_id, db
    )
