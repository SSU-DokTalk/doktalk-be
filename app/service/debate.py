from typing import List

from fastapi import HTTPException
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager

from app.db.models.soft_delete import BaseSession as Session
from app.dto.debate import CreateDebateReq
from app.dto.debate_comment import CreateDebateCommentReq, BasicDebateComment
from app.model.User import User
from app.model.Debate import Debate
from app.model.DebateLike import DebateLike
from app.model.DebateComment import DebateComment
from app.model.DebateCommentLike import DebateCommentLike
from app.schema.debate_like import DebateLikeSchema
from app.schema.debate_comment_like import DebateCommentLikeSchema


def getDebateService(debate_id: int, db: Session):
    res = (
        db.query(Debate)
        .join(Debate.user)
        .options(contains_eager(Debate.user))
        .filter(Debate.id == debate_id)
        .first()
    )
    if res == None:
        raise HTTPException(status_code=404)
    return res


def getDebateLikeService(
    user_id: int, debate_ids: List[int], db: Session
) -> List[DebateLikeSchema]:
    return (
        db.query(DebateLike)
        .filter(DebateLike.user_id == user_id, DebateLike.debate_id.in_(debate_ids))
        .all()
    )


def getDebateCommentLikeService(
    user_id: int, debate_comment_ids: List[int], db: Session
) -> List[DebateCommentLikeSchema]:
    return (
        db.query(DebateCommentLike)
        .filter(
            DebateCommentLike.user_id == user_id,
            DebateCommentLike.debate_comment_id.in_(debate_comment_ids),
        )
        .all()
    )


def getDebateCommentsService(debate_id: int, db: Session) -> List[BasicDebateComment]:
    return (
        db.query(DebateComment)
        .join(DebateComment.user)
        .options(contains_eager(DebateComment.user))
        .filter(DebateComment.debate_id == debate_id)
        .all()
    )


def createDebateService(user: User, post_data: CreateDebateReq, db: Session) -> int:
    try:
        debate = Debate(user=user, data=post_data)
        db.add(debate)
        db.commit()
        db.refresh(debate)
    except IntegrityError:
        raise HTTPException(status_code=404)
    return debate.id


def createDebateLikeService(user: User, debate_id: int, db: Session) -> None:
    try:
        post_like = DebateLike(user_id=user.id, debate_id=debate_id)
        db.add(post_like)
        db.commit()
        db.refresh(post_like)

        db.query(Debate).filter(Debate.id == debate_id).update(
            {Debate.likes_num: Debate.likes_num + 1}
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


def createDebateCommentService(
    user: User, debate_id: int, debate_comment_data: CreateDebateCommentReq, db: Session
) -> int:
    try:
        debate_comment = DebateComment(
            user=user, debate_id=debate_id, data=debate_comment_data
        )
        db.add(debate_comment)
        db.commit()
        db.refresh(debate_comment)

        db.query(Debate).filter(Debate.id == debate_id).update(
            {Debate.comments_num: Debate.comments_num + 1}
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)
    return debate_comment.id


def createDebateCommentLikeService(
    user: User, debate_comment_id: int, db: Session
) -> None:
    try:
        debate_comment_like = DebateCommentLike(
            user_id=user.id, debate_comment_id=debate_comment_id
        )
        db.add(debate_comment_like)
        db.commit()
        db.refresh(debate_comment_like)

        db.query(DebateComment).filter(DebateComment.id == debate_comment_id).update(
            {DebateComment.likes_num: DebateComment.likes_num + 1}
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


def deleteDebateLikeService(user: User, debate_id: int, db: Session) -> None:
    try:
        db.query(DebateLike).filter(
            DebateLike.user_id == user.id, DebateLike.debate_id == debate_id
        ).delete()
        db.query(Debate).filter(Debate.id == debate_id).update(
            {Debate.likes_num: Debate.likes_num - 1}
        )
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)
    return


def deleteDebateCommentService(user: User, debate_comment_id: int, db: Session) -> None:
    try:
        db.query(DebateComment).filter(
            DebateComment.id == debate_comment_id, DebateComment.user_id == user.id
        ).delete()
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)
    return


def deleteDebateCommentService(user: User, debate_comment_id: int, db: Session) -> None:
    debate_comment = (
        db.query(DebateComment).filter(DebateComment.id == debate_comment_id).first()
    )
    if debate_comment == None:
        raise HTTPException(status_code=404)

    if debate_comment.user_id != user.id:
        raise HTTPException(status_code=403)

    db.delete(debate_comment)
    db.commit()
    return


def deleteDebateCommentLikeService(
    user: User, debate_comment_id: int, db: Session
) -> None:
    debate_comment_like = (
        db.query(DebateCommentLike)
        .filter(
            DebateCommentLike.user_id == user.id,
            DebateCommentLike.debate_comment_id == debate_comment_id,
        )
        .first()
    )
    if debate_comment_like == None:
        raise HTTPException(status_code=404)

    db.delete(debate_comment_like)
    db.commit()
    return


__all__ = [
    "getDebateService",
    "getDebateLikeService",
    "getDebateCommentLikeService",
    "getDebateCommentsService",
    "createDebateService",
    "createDebateLikeService",
    "createDebateCommentService",
    "createDebateCommentLikeService",
    "deleteDebateLikeService",
    "deleteDebateCommentService",
    "deleteDebateCommentLikeService",
]
