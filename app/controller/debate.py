from typing import Annotated, List

from fastapi import APIRouter, Depends, Request, Query
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.db.models.soft_delete import BaseSession as Session
from app.dto.debate import *
from app.dto.debate_comment import *
from app.service.debate import *

router = APIRouter()


###########
### GET ###
###########
@router.get("s/like")
def getDebateLikeController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    debate_ids: List[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    토론의 좋아요 조회
    """
    return getDebateLikeService(request.state.user.id, debate_ids, db)


@router.get("/comments/like")
def getDebateCommentLikeController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    debate_comment_ids: List[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    토론의 댓글 좋아요 조회
    """
    return getDebateCommentLikeService(request.state.user.id, debate_comment_ids, db)


@router.get("/{debate_id}")
def getDebateController(
    debate_id: int, db: Session = Depends(get_db)
) -> BasicDebateRes:
    """
    단일 토론 조회
    """
    return BasicDebateRes.model_validate(getDebateService(debate_id, db))


@router.get("/{debate_id}/comments")
def getDebateCommentsController(debate_id: int, db: Session = Depends(get_db)):
    """
    토론의 댓글 조회
    """
    return getDebateCommentsService(debate_id, db)


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
@router.delete("/{debate_id}/like")
def deleteDebateLikeController(
    debate_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    토론의 좋아요 삭제
    """
    return deleteDebateLikeService(request.state.user.id, debate_id, db)


@router.delete("/comment/{debate_comment_id}")
def deleteDebateCommentController(
    debate_comment_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    토론의 댓글 삭제
    """
    return deleteDebateCommentService(request.state.user.id, debate_comment_id, db)


@router.delete("/comment/{debate_comment_id}/like")
def deleteDebateCommentLikeController(
    debate_comment_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    토론의 댓글 좋아요 삭제
    """
    return deleteDebateCommentLikeService(request.state.user.id, debate_comment_id, db)
