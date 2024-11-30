from typing import Annotated, List

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session, contains_eager

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.dto.debate import CreateDebateReq, BasicDebateRes
from app.dto.debate_comment import CreateDebateCommentReq, DebateComment
from app.model.Debate import Debate
from app.service.debate import (
    getDebateService,
    createDebateService,
    createDebateCommentService,
    createDebateLikeService,
    createDebateCommentLikeService,
)

router = APIRouter()


###########
### GET ###
###########
@router.get("/{debate_id}")
def getDebateController(
    debate_id: int, db: Session = Depends(get_db)
) -> BasicDebateRes:
    """
    단일 토론 조회
    """
    return BasicDebateRes.model_validate(getDebateService(debate_id, db))


############
### POST ###
############
@router.post("")
def createDebateController(
    debate_data: CreateDebateReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    """
    토론 작성
    """
    return createDebateService(request.state.user, debate_data, db)


@router.post("/{debate_id}/comment")
def createDebateCommentController(
    debate_id: int,
    debate_comment_data: CreateDebateCommentReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    """
    토론의 댓글 작성
    """
    return createDebateCommentService(
        request.state.user, debate_id, debate_comment_data, db
    )


@router.post("/{debate_id}/like")
def createDebateLikeController(
    debate_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    토론에 좋아요 달기
    """
    return createDebateLikeService(request.state.user, debate_id, db)


@router.post("/comment/{debate_comment_id}/like")
def createDebateCommentLikeController(
    debate_comment_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    토론의 댓글에 좋아요 달기
    """
    return createDebateCommentLikeService(request.state.user, debate_comment_id, db)


###########
### PUT ###
###########

#############
### PATCH ###
#############

##############
### DELETE ###
##############
