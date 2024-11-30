from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dto.summary import CreateSummaryReq
from app.model.Summary import Summary
from app.model.User import User


def createSummaryService(
    user: User, summary_data: CreateSummaryReq, db: Session
) -> int:
    try:
        summary = Summary(user=user, data=summary_data)
        db.add(summary)
        db.commit()
        db.refresh(summary)
    except IntegrityError:
        raise HTTPException(status_code=404)
    return summary.id
