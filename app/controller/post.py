from typing import Annotated, List, Union

from fastapi import APIRouter, Depends, Request, Query
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import contains_eager

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.db.models.soft_delete import BaseSession as Session
from app.dto.post import CreatePostReq, BasicPostRes
from app.dto.post_comment import CreatePostCommentReq
from app.model.Post import Post
from app.service.post import *

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
        .order_by(Post.created.desc())
    )


@router.get("s/like")
def getPostLikeController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    ids: Union[List[int], None] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    게시글 좋아요 조회
    """
    return getPostLikeService(ids, request.state.user.id, db)


@router.get("/comments/like")
def getPostLikeController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    ids: Union[List[int], None] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    게시글의 댓글 좋아요 조회
    """
    return getPostCommentLikeService(ids, request.state.user.id, db)


@router.get("/{post_id}")
def getPostController(post_id: int, db: Session = Depends(get_db)) -> BasicPostRes:
    """
    단일 게시글 조회
    """
    return BasicPostRes.model_validate(getPostService(post_id, db))


@router.get("/{post_id}/comments")
def getPostCommentsController(
    post_id: int, size: int = 10, page: int = 1, db: Session = Depends(get_db)
):
    """
    게시글의 댓글들 조회
    """
    return getPostCommentsService(size, page, post_id, db)


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
@router.patch("/{post_id}")
def updatePostController(
    post_id: int,
    post_data: CreatePostReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    게시글 수정
    """
    return updatePostService(request.state.user, post_id, post_data, db)


@router.patch("/comment/{post_comment_id}")
def updatePostCommentController(
    post_comment_id: int,
    post_comment_data: CreatePostCommentReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    게시글의 댓글 수정
    """
    return updatePostCommentService(
        request.state.user, post_comment_id, post_comment_data, db
    )


##############
### DELETE ###
##############
@router.delete("/{post_id}")
def deletePostController(
    post_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    게시글 삭제
    """
    return deletePostService(request.state.user, post_id, db)


@router.delete("/{post_id}/like")
def deletePostLikeController(
    request: Request,
    post_id: int,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    게시글 좋아요 삭제
    """
    return deletePostLikeService(request.state.user, post_id, db)


@router.delete("/comment/{post_comment_id}")
def deletePostCommentController(
    post_comment_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    게시글의 댓글 삭제
    """
    return deletePostCommentService(request.state.user, post_comment_id, db)


@router.delete("/comment/{post_comment_id}/like")
def deletePostCommentLikeController(
    request: Request,
    post_comment_id: int,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    게시글의 댓글 좋아요 삭제
    """
    return deletePostCommentLikeService(request.state.user, post_comment_id, db)
