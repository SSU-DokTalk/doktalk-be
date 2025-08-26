from typing import List

from fastapi import HTTPException
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager

from app.db.models.soft_delete import BaseSession as Session
from app.dto.post import CreatePostReq, BasicPostRes
from app.dto.post_comment import CreatePostCommentReq, BasicPostComment
from app.model import User, Post, PostLike, PostComment, PostCommentLike
from app.schema.post_like import PostLikeSchema
from app.schema.post_comment_like import PostCommentLikeSchema


def getPostListService(
    search: str,
    sortby: str,
    db: Session,
) -> Page[BasicPostRes]:
    """
    게시글 리스트 조회 서비스 (검색 기능 포함)
    """
    conditions = list()

    # 검색어가 있는 경우 title과 content에서 OR 조건으로 검색
    # TODO: MySQL full-text search (MATCH ... AGAINST)
    if search:
        search_conditions = []
        for keyword in search.lower().split():
            search_conditions.extend([
                func.instr(func.lower(Post.title), keyword) > 0,
                func.instr(func.lower(Post.content), keyword) > 0
            ])
        # 각 키워드에 대해 title 또는 content 중 하나라도 매칭되면 포함
        if search_conditions:
            conditions.append(or_(*search_conditions))

    order_by = []
    if sortby == "popular":
        order_by.append(Post.likes_num.desc())
        order_by.append(Post.comments_num.desc())
    # 기본적으로 최신순으로 정렬 (latest)
    order_by.append(Post.created.desc())

    return paginate(
        db.query(Post)
        .join(Post.user)
        .filter(*conditions)
        .order_by(*order_by)
        .options(contains_eager(Post.user))
    )


def getPostService(post_id: int, db: Session):
    res = (
        db.query(Post)
        .join(Post.user)
        .options(contains_eager(Post.user))
        .filter(Post.id == post_id)
        .first()
    )
    if res == None:
        raise HTTPException(status_code=404)
    return res


def getPostLikeService(post_ids: list[int], user_id: int, db: Session) -> List[bool]:
    res = [
        result[0]
        for result in db.query(PostLike.post_id)
        .filter(PostLike.user_id == user_id, PostLike.post_id.in_(post_ids))
        .all()
    ]
    return res


def getPostCommentsService(
    size: int, page: int, post_id: int, db: Session
) -> Page[BasicPostComment]:
    res = paginate(
        db.query(PostComment)
        .join(PostComment.user)
        .options(contains_eager(PostComment.user))
        .filter(PostComment.post_id == post_id)
        .order_by(PostComment.created.desc()),
        Params(size=size, page=page),
    )
    res = {
        "items": [BasicPostComment.model_validate(item) for item in res.items],
        "page": res.page,
        "pages": res.pages,
        "total": res.total,
    }
    return res


def getPostCommentLikeService(
    post_comment_ids: list[int], user_id: int, db: Session
) -> List[bool]:
    res = [
        result[0]
        for result in db.query(PostCommentLike.post_comment_id)
        .filter(
            PostCommentLike.user_id == user_id,
            PostCommentLike.post_comment_id.in_(post_comment_ids),
        )
        .all()
    ]
    return res


def createPostService(user: User, post_data: CreatePostReq, db: Session) -> int:
    try:
        post = Post(user=user, data=post_data)
        db.add(post)
        db.commit()
        db.refresh(post)
    except IntegrityError:
        raise HTTPException(status_code=404)
    return post.id


def createPostLikeService(user: User, post_id: int, db: Session) -> None:
    try:
        post_like = PostLike(user_id=user.id, post_id=post_id)
        db.add(post_like)
        db.commit()
        db.refresh(post_like)

        db.query(Post).filter(Post.id == post_id).update(
            {Post.likes_num: Post.likes_num + 1}
        )
        db.commit()
    except IntegrityError as e:
        # 오류 메시지 분석
        if isinstance(e.orig, PymysqlIntegrityError):
            sql_code = e.orig.args[0]  # MySQL 상태 코드 (1452 또는 1062)

            if sql_code == 1452:  # 외래 키 제약 조건 위반
                raise HTTPException(status_code=404, detail="Entity not found")

            elif sql_code == 1062:  # 중복 키 제약 조건 위반
                raise HTTPException(
                    status_code=409, detail="Duplicate entry for entity like"
                )

        # 기타 IntegrityError 처리
        raise HTTPException(status_code=400, detail="Database integrity error")


def createPostCommentService(
    user: User, post_id: int, post_comment_data: CreatePostCommentReq, db: Session
) -> int:
    try:
        post_comment = PostComment(
            user=user, post_id=post_id, data=post_comment_data)
        db.add(post_comment)
        db.commit()
        db.refresh(post_comment)

        db.query(Post).filter(Post.id == post_id).update(
            {Post.comments_num: Post.comments_num + 1}
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)
    return post_comment.id


def createPostCommentLikeService(user: User, post_comment_id: int, db: Session) -> None:
    try:
        post_comment_like = PostCommentLike(
            user_id=user.id, post_comment_id=post_comment_id
        )
        db.add(post_comment_like)
        db.commit()
        db.refresh(post_comment_like)

        db.query(PostComment).filter(PostComment.id == post_comment_id).update(
            {PostComment.likes_num: PostComment.likes_num + 1}
        )
        db.commit()
    except IntegrityError as e:
        # 오류 메시지 분석
        if isinstance(e.orig, PymysqlIntegrityError):
            sql_code = e.orig.args[0]  # MySQL 상태 코드 (1452 또는 1062)

            if sql_code == 1452:  # 외래 키 제약 조건 위반
                raise HTTPException(status_code=404, detail="Entity not found")

            elif sql_code == 1062:  # 중복 키 제약 조건 위반
                raise HTTPException(
                    status_code=409, detail="Duplicate entry for entity like"
                )

        # 기타 IntegrityError 처리
        raise HTTPException(status_code=400, detail="Database integrity error")


def updatePostService(user: User, post_id: int, update_data: CreatePostReq, db: Session):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()

        if post is None:
            raise HTTPException(status_code=404)

        if post.user_id != user.id:
            raise HTTPException(status_code=403)

        post.update(update_data)

        db.commit()
        db.refresh(post)

    except IntegrityError as e:
        # 오류 메시지 분석
        if isinstance(e.orig, PymysqlIntegrityError):
            sql_code = e.orig.args[0]  # MySQL 상태 코드 (1452 또는 1062)
            if sql_code == 1452:  # 외래 키 제약 조건 위반
                raise HTTPException(status_code=404, detail="Entity not found")

        # 기타 IntegrityError 처리
        raise HTTPException(status_code=400, detail="Database integrity error")
    except Exception as e:
        raise e

    return


def updatePostCommentService(
    user: User,
    post_comment_id: int,
    post_comment_data: CreatePostCommentReq,
    db: Session,
):
    try:
        if user.id != db.query(PostComment).get(post_comment_id).user_id:
            raise HTTPException(status_code=403)
        db.query(PostComment).filter(PostComment.id == post_comment_id).update(
            post_comment_data.model_dump()
        )
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)


def deletePostService(user: User, post_id: int, db: Session) -> None:
    try:
        if user.id != db.query(Post).get(post_id).user_id:
            raise HTTPException(status_code=403)
        db.query(Post).filter(Post.id == post_id).delete()
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)


def deletePostLikeService(user: User, post_id: int, db: Session) -> None:
    try:
        res = (
            db.query(PostLike)
            .filter(PostLike.user_id == user.id, PostLike.post_id == post_id)
            .delete()
        )
        if res == 0:
            raise HTTPException(status_code=404)
        db.query(Post).filter(Post.id == post_id).update(
            {Post.likes_num: Post.likes_num - 1}
        )
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)
    return


def deletePostCommentService(user: User, post_comment_id: int, db: Session) -> None:
    try:
        if user.id != db.query(PostComment).get(post_comment_id).user_id:
            raise HTTPException(status_code=403)
        db.query(PostComment).filter(
            PostComment.id == post_comment_id).delete()
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)


def deletePostCommentLikeService(user: User, post_comment_id: int, db: Session) -> None:
    try:
        res = (
            db.query(PostCommentLike)
            .filter(
                PostCommentLike.user_id == user.id,
                PostCommentLike.post_comment_id == post_comment_id,
            )
            .delete()
        )
        if res == 0:
            raise HTTPException(status_code=404)
        db.query(PostComment).filter(PostComment.id == post_comment_id).update(
            {PostComment.likes_num: PostComment.likes_num - 1}
        )
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)


__all__ = [
    "getPostListService",
    "getPostService",
    "getPostLikeService",
    "getPostCommentsService",
    "getPostCommentLikeService",
    "createPostService",
    "createPostLikeService",
    "createPostCommentService",
    "createPostCommentLikeService",
    "updatePostService",
    "updatePostCommentService",
    "deletePostService",
    "deletePostLikeService",
    "deletePostCommentService",
    "deletePostCommentLikeService",
]
