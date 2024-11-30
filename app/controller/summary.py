from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.dto.summary import CreateSummaryReq, BasicSummaryRes
from app.dto.summary_comment import CreateSummaryCommentReq
from app.service.summary import (
    getSummaryService,
    createSummaryService,
    createSummaryCommentService,
    createSummaryLikeService,
    createSummaryCommentLikeService,
)


router = APIRouter()


###########
### GET ###
###########
@router.get("/{summary_id}")
def getSummaryController(
    summary_id: int, db: Session = Depends(get_db)
) -> BasicSummaryRes:
    """
    단일 요약 조회
    """
    return BasicSummaryRes.model_validate(getSummaryService(summary_id, db)).model_dump(
        exclude={"charged_content"}
    )


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
