from fastapi import HTTPException
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, contains_eager

from app.dto.summary import CreateSummaryReq
from app.dto.summary_comment import CreateSummaryCommentReq
from app.model.Summary import Summary
from app.model.SummaryLike import SummaryLike
from app.model.SummaryComment import SummaryComment
from app.model.SummaryCommentLike import SummaryCommentLike
from app.model.User import User


def getSummaryService(summary_id: int, db: Session):
    res = (
        db.query(Summary)
        .join(Summary.user)
        .options(contains_eager(Summary.user))
        .filter(Summary.id == summary_id)
        .first()
    )
    if res == None:
        raise HTTPException(status_code=404)
    return res


def createSummaryService(
    user: User, summary_data: CreateSummaryReq, db: Session
) -> int:
    try:
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
