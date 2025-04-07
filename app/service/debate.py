from typing import List
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager

from app.db.models.soft_delete import BaseSession as Session
from app.dto.debate import CreateDebateReq
from app.dto.debate_comment import CreateDebateCommentReq, BasicDebateComment
from app.model import Book, User, Debate, DebateLike, DebateComment, DebateCommentLike
from app.schema.debate_like import DebateLikeSchema
from app.schema.debate_comment_like import DebateCommentLikeSchema
from app.schema.book_api import BookAPIResponseSchema
from app.service.book import getOrCreateBook
from app.service.book_api import getAPIBookDetailService


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


def getPopularDebateListService(db: Session) -> List[Debate]:
    from_ = datetime.now(timezone.utc) - timedelta(days=7)
    return (
        db.query(Debate)
        .filter(Debate.created >= from_)
        .join(Debate.user)
        .join(Debate.book)
        .options(contains_eager(Debate.user))
        .options(contains_eager(Debate.book))
        .order_by(
            Debate.likes_num.desc(), Debate.comments_num.desc(), Debate.created.desc()
        )
        .limit(5)
        .all()
    )


def getDebateLikeService(user_id: int, debate_ids: List[int], db: Session) -> List[int]:
    if debate_ids is None or len(debate_ids) == 0:
        return []
    res = [
        result[0]
        for result in db.query(DebateLike.debate_id)
        .filter(DebateLike.user_id == user_id, DebateLike.debate_id.in_(debate_ids))
        .all()
    ]

    return res


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


def createDebateService(user: User, debate_data: CreateDebateReq, db: Session) -> int:
    try:

        book = db.query(Book).filter(Book.isbn == debate_data.isbn).first()
        if book == None:
            bookData = BookAPIResponseSchema(
                **getAPIBookDetailService(debate_data.isbn)
            )
            bookData = Book(data=bookData)
            db.add(bookData)
            db.commit()

        debate = Debate(user=user, data=debate_data)
        db.add(debate)
        db.commit()
        db.refresh(debate)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Wrong isbn")
    return debate.id


def createDebateLikeService(user: User, debate_id: int, db: Session) -> None:
    try:
        debate_like = DebateLike(user_id=user.id, debate_id=debate_id)
        db.add(debate_like)
        db.commit()
        db.refresh(debate_like)

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


def updateDebateService(user: User, debate_id: int, update_data: CreateDebateReq, db: Session) -> None:
    try:
        debate = (
            db.query(Debate)
            .join(Debate.user)
            .options(contains_eager(Debate.user))
            .filter(Debate.id == debate_id)
            .first()
        )

        if debate is None:
            raise HTTPException(status_code=404)

        if debate.user_id != user.id:
            raise HTTPException(status_code=403)

        if debate.book.isbn != update_data.isbn:
            book = getOrCreateBook(update_data.isbn, db)

        print(vars(update_data))
        debate.update(update_data)

        db.commit()
        db.refresh(debate)

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Wrong isbn")
    except Exception as e:
        raise e

    return


def deleteDebateService(user_id: int, debate_id: int, db: Session) -> None:
    try:
        debate = db.query(Debate).filter(Debate.id == debate_id).first()
        if debate == None:
            raise HTTPException(status_code=404)
        if debate.user_id != user_id:
            raise HTTPException(status_code=403)
        db.delete(debate)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400)
    return


def deleteDebateLikeService(user_id: int, debate_id: int, db: Session) -> None:
    try:
        res = (
            db.query(DebateLike)
            .filter(DebateLike.debate_id == debate_id, DebateLike.user_id == user_id)
            .delete()
        )
        if res == 0:
            raise HTTPException(status_code=404)
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
        db.query(DebateComment).filter(
            DebateComment.id == debate_comment_id).first()
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
    "getPopularDebateListService",
    "getDebateLikeService",
    "getDebateCommentLikeService",
    "getDebateCommentsService",
    "createDebateService",
    "createDebateLikeService",
    "createDebateCommentService",
    "createDebateCommentLikeService",
    "updateDebateService",
    "deleteDebateService",
    "deleteDebateLikeService",
    "deleteDebateCommentService",
    "deleteDebateCommentLikeService",
]
