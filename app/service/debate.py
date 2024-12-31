from fastapi import HTTPException
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager

from app.db.soft_delete import BaseSession as Session
from app.dto.debate import CreateDebateReq
from app.dto.debate_comment import CreateDebateCommentReq
from app.model.User import User
from app.model.Debate import Debate
from app.model.DebateLike import DebateLike
from app.model.DebateComment import DebateComment
from app.model.DebateCommentLike import DebateCommentLike


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


__all__ = [
    "getDebateService",
    "createDebateService",
    "createDebateLikeService",
    "createDebateCommentService",
    "createDebateCommentLikeService",
]
