from typing import Annotated, List

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session, contains_eager

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.dto.post import CreatePostReq, BasicPostRes
from app.dto.post_comment import CreatePostCommentReq, PostComment
from app.model.Post import Post
from app.service.post import (
    getPostService,
    getPostCommentsService,
    createPostService,
    createPostCommentService,
    createPostLikeService,
    createPostCommentLikeService,
)

router = APIRouter()


###########
### GET ###
###########
@router.get("/recent", response_model=Page[BasicPostRes])
def getRecentPostsController(db: Session = Depends(get_db)):
    """
    최근 게시글 조회
    """
    return paginate(
        db.query(Post)
        .join(Post.user)
        .options(contains_eager(Post.user))
        .order_by(Post.created_at.desc())
    )


@router.get("/{post_id}")
def getPostController(post_id: int, db: Session = Depends(get_db)) -> BasicPostRes:
    """
    단일 게시글 조회
    """
    return BasicPostRes.model_validate(getPostService(post_id, db))


@router.get("/{post_id}/comments")
def getPostCommentsController(
    post_id: int, db: Session = Depends(get_db)
) -> List[PostComment]:
    """
    게시글의 댓글들 조회
    """
    return getPostCommentsService(post_id, db)


############
### POST ###
############
@router.post("")
def createPostController(
    post_data: CreatePostReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    """
    게시글 작성
    """
    return createPostService(request.state.user, post_data, db)


@router.post("/{post_id}/comment")
def createPostCommentController(
    post_id: int,
    post_comment_data: CreatePostCommentReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    """
    게시글의 댓글 작성
    """
    return createPostCommentService(request.state.user, post_id, post_comment_data, db)


@router.post("/{post_id}/like")
def createPostLikeController(
    post_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    return createPostLikeService(request.state.user, post_id, db)


@router.post("/comment/{post_comment_id}/like")
def createPostCommentLikeController(
    post_comment_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    게시글의 댓글에 좋아요 달기
    """
    return createPostCommentLikeService(request.state.user, post_comment_id, db)


###########
### PUT ###
###########

#############
### PATCH ###
#############

##############
### DELETE ###
##############
