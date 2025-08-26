from typing import List
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager

from app.db.models.soft_delete import BaseSession as Session
from app.dto.summary import CreateSummaryReq, BasicSummaryRes
from app.dto.summary_comment import CreateSummaryCommentReq, BasicSummaryComment
from app.enums import LANGUAGE, CATEGORY
from app.function.generate_dummy import generate_sentence
from app.schema.book_api import BookAPIResponseSchema
from app.model import (
    Book,
    Purchase,
    Summary,
    SummaryLike,
    SummaryComment,
    SummaryCommentLike,
    User,
)
from app.schema.summary_like import SummaryLikeSchema
from app.schema.summary_comment import SummaryCommentSchema
from app.schema.summary_comment_like import SummaryCommentLikeSchema
from app.service.book import getOrCreateBook
from app.service.book_api import getAPIBookDetailService


def getSummaryListService(
    category: int,
    search: str,
    searchby: str,
    sortby: str,
    lang: LANGUAGE,
    db: Session,
) -> Page[BasicSummaryRes]:
    """
    요약 리스트 조회 서비스
    """
    conditions = list()
    if searchby == "bt":
        conditions = [
            func.instr(func.lower(Book.title), keyword) > 0
            for keyword in search.lower().split()
        ]
    elif searchby == "it":
        conditions = [
            func.instr(func.lower(Summary.title), keyword) > 0
            for keyword in search.lower().split()
        ]
    if 0 < category <= CATEGORY.max():
        conditions.append((Summary.category.bitwise_and(category)) == category)

    order_by = []
    if sortby == "popular":
        from_ = datetime.now(timezone.utc) - timedelta(days=7)
        order_by.append(Summary.likes_num.desc())
        conditions.append(Summary.created >= from_)
    order_by.append(Summary.created.desc())

    summaries = paginate(
        db.query(Summary)
        .join(Summary.book)
        .filter(*conditions)
        .order_by(*order_by)
        .options(contains_eager(Summary.book))
    )

    # Charged content를 마스킹
    for items in summaries.items:
        items.charged_content = generate_sentence(
            items.charged_content[:200], lang)

    return summaries


def getPopularSummaryListService(
    lang: LANGUAGE,
    db: Session,
) -> List[BasicSummaryRes]:
    """
    인기 요약 리스트 조회 서비스
    """
    from_ = datetime.now(timezone.utc) - timedelta(days=7)
    summaries = (
        db.query(Summary)
        # .filter(Summary.created >= from_)  # TODO: 현재 글이 너무 적어서 전체 범위에서 찾도록 함
        .join(Summary.book)
        .join(Summary.user)
        .options(contains_eager(Summary.book))
        .options(contains_eager(Summary.user))
        .order_by(
            Summary.likes_num.desc(),
            Summary.comments_num.desc(),
            Summary.created.desc(),
        )
        .limit(5)
    ).all()

    # Charged content를 마스킹
    for summary in summaries:
        summary.charged_content = generate_sentence(
            summary.charged_content[:200], lang)

    return summaries


def getSummaryWithMaskingService(summary_id: int, lang: LANGUAGE, db: Session):
    """
    단일 요약 조회 (마스킹 포함)
    """
    summary = getSummaryService(summary_id, db)
    summary.charged_content = generate_sentence(
        summary.charged_content[:200], lang)
    return summary


def getSummaryService(summary_id: int, db: Session):
    res = (
        db.query(Summary)
        .join(Summary.user)
        .join(Summary.book)
        .options(contains_eager(Summary.user))
        .options(contains_eager(Summary.book))
        .filter(Summary.id == summary_id)
        .first()
    )
    if res == None:
        raise HTTPException(status_code=404)
    return res


def getSummaryChargedContentService(user_id: int, summary_id: int, db: Session) -> str:
    res = db.query(Summary).filter(Summary.id == summary_id).first()
    if res == None:
        raise HTTPException(status_code=404)

    # 유저가 해당 요약을 구매했는지 확인
    purchase = (
        db.query(Purchase)
        .filter(
            Purchase.user_id == user_id,
            Purchase.product_type == "S",
            Purchase.product_id == summary_id,
        )
        .first()
    )
    if purchase == None:
        raise HTTPException(status_code=404)
    return res.charged_content


def getSummaryLikeService(
    user_id: int, summary_ids: list[int], db: Session
) -> List[int]:
    if summary_ids is None or len(summary_ids) == 0:
        return []
    res = [
        result[0]
        for result in db.query(SummaryLike.summary_id)
        .filter(SummaryLike.user_id == user_id, SummaryLike.summary_id.in_(summary_ids))
        .all()
    ]
    return res


def getSummaryCommentService(summary_id: int, db: Session) -> List[BasicSummaryComment]:
    return (
        db.query(SummaryComment)
        .join(SummaryComment.user)
        .options(contains_eager(SummaryComment.user))
        .filter(SummaryComment.summary_id == summary_id)
        .all()
    )


def getSummaryCommentLikeService(
    user_id: int, summary_comment_ids: list[int], db: Session
) -> List[SummaryCommentLikeSchema]:
    return (
        db.query(SummaryCommentLike)
        .filter(
            SummaryCommentLike.user_id == user_id,
            SummaryCommentLike.summary_comment_id.in_(summary_comment_ids),
        )
        .all()
    )


def createSummaryService(
    user: User, summary_data: CreateSummaryReq, db: Session
) -> int:
    try:
        book = getOrCreateBook(summary_data.isbn, db)

        summary = Summary(user=user, data=summary_data)
        db.add(summary)
        db.commit()
        db.refresh(summary)

    except IntegrityError as e:
        # 오류 메시지 분석
        if isinstance(e.orig, PymysqlIntegrityError):
            sql_code = e.orig.args[0]  # MySQL 상태 코드 (1452 또는 1062)
            if sql_code == 1452:  # 외래 키 제약 조건 위반
                raise HTTPException(status_code=404, detail="Entity not found")

        # 기타 IntegrityError 처리
        raise HTTPException(status_code=400, detail="Database integrity error")
    return summary.id


def createSummaryLikeService(user: User, summary_id: int, db: Session) -> None:
    try:
        summary_like = SummaryLike(user_id=user.id, summary_id=summary_id)
        db.add(summary_like)
        db.commit()
        db.refresh(summary_like)

        db.query(Summary).filter(Summary.id == summary_id).update(
            {Summary.likes_num: Summary.likes_num + 1}
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


def createSummaryCommentService(
    user: User,
    summary_id: int,
    summary_comment_data: CreateSummaryCommentReq,
    db: Session,
) -> int:
    try:
        summary_comment = SummaryComment(
            user=user, summary_id=summary_id, data=summary_comment_data
        )
        db.add(summary_comment)
        db.commit()
        db.refresh(summary_comment)

        db.query(Summary).filter(Summary.id == summary_id).update(
            {Summary.comments_num: Summary.comments_num + 1}
        )
        db.commit()

    except IntegrityError as e:
        # 오류 메시지 분석
        if isinstance(e.orig, PymysqlIntegrityError):
            sql_code = e.orig.args[0]  # MySQL 상태 코드 (1452 또는 1062)

            if sql_code == 1452:  # 외래 키 제약 조건 위반
                raise HTTPException(status_code=404, detail="Entity not found")

        # 기타 IntegrityError 처리
        raise HTTPException(status_code=400, detail="Database integrity error")
    return summary_comment.id


def createSummaryCommentLikeService(
    user: User, summary_comment_id: int, db: Session
) -> None:
    try:
        summary_comment_like = SummaryCommentLike(
            user_id=user.id, summary_comment_id=summary_comment_id
        )
        db.add(summary_comment_like)
        db.commit()
        db.refresh(summary_comment_like)

        db.query(SummaryComment).filter(SummaryComment.id == summary_comment_id).update(
            {SummaryComment.likes_num: SummaryComment.likes_num + 1}
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


def updateSummaryService(user: User, summary_id: int, update_data: CreateSummaryReq, db: Session) -> None:
    try:
        summary = db.query(Summary).filter(Summary.id == summary_id).first()

        if summary is None:
            raise HTTPException(status_code=404)

        if summary.user_id != user.id:
            raise HTTPException(status_code=403)

        if summary.book.isbn != update_data.isbn:
            book = getOrCreateBook(update_data.isbn, db)

        summary.update(update_data)

        db.commit()
        db.refresh(summary)

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


def deleteSummaryService(user_id: int, summary_id: int, db: Session) -> None:
    try:
        summary = db.query(Summary).filter(Summary.id == summary_id).first()
        print(summary)
        if summary == None:
            raise HTTPException(status_code=404)
        if summary.user_id != user_id:
            raise HTTPException(status_code=403)
        db.delete(summary)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400)
    return


def deleteSummaryLikeService(user_id: int, summary_id: int, db: Session) -> None:
    try:
        res = (
            db.query(SummaryLike)
            .filter(
                SummaryLike.summary_id == summary_id, SummaryLike.user_id == user_id
            )
            .delete()
        )
        if res == 0:
            raise HTTPException(status_code=404)
        db.query(Summary).filter(Summary.id == summary_id).update(
            {Summary.likes_num: Summary.likes_num - 1}
        )
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)
    return


def deleteSummaryCommentService(
    user_id: int, summary_comment_id: int, db: Session
) -> None:
    summary_comment = (
        db.query(SummaryComment).filter(
            SummaryComment.id == summary_comment_id).first()
    )
    if summary_comment == None:
        raise HTTPException(status_code=404)

    if summary_comment.user_id != user_id:
        raise HTTPException(status_code=403)

    db.delete(summary_comment)
    db.commit()
    return


def deleteSummaryCommentLikeService(
    user_id: int, summary_comment_id: int, db: Session
) -> None:
    summary_comment_like = (
        db.query(SummaryCommentLike)
        .filter(
            SummaryCommentLike.user_id == user_id,
            SummaryCommentLike.summary_comment_id == summary_comment_id,
        )
        .first()
    )
    if summary_comment_like == None:
        raise HTTPException(status_code=404)

    db.delete(summary_comment_like)
    db.commit()
    return


__all__ = [
    "getSummaryListService",
    "getPopularSummaryListService",
    "getSummaryService",
    "getSummaryWithMaskingService",
    "getSummaryChargedContentService",
    "getSummaryLikeService",
    "getSummaryCommentService",
    "getSummaryCommentLikeService",
    "createSummaryService",
    "createSummaryLikeService",
    "createSummaryCommentService",
    "createSummaryCommentLikeService",
    "updateSummaryService",
    "deleteSummaryService",
    "deleteSummaryLikeService",
    "deleteSummaryCommentService",
    "deleteSummaryCommentLikeService",
]
