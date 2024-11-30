from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme
from app.db.connection import get_db
from app.dto.summary import CreateSummaryReq
from app.service.summary import createSummaryService


router = APIRouter()


@router.post("")
def createSummaryController(
    summary_data: CreateSummaryReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> int:
    return createSummaryService(request.state.user, summary_data, db)
