from fastapi import APIRouter, Depends, Response, Security
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.service.user import *
from app.schema.user import *
from fastapi.security import HTTPAuthorizationCredentials
from app.core.security import (
    create_access_token,
    create_refresh_token,
    TokenData,
    oauth2_scheme,
    HTTPBearer,
)
from typing import Annotated

router = APIRouter()


@router.post("/register")
def basicRegisterController(user_data: BasicRegisterReq, db: Session = Depends(get_db)):
    """
    시스템 자체 회원가입 기능입니다.
    """
    userId = basicRegisterService(user_data, db)
    return userId


@router.post("/login")
def basicLoginController(
    user_data: BasicLoginReq, response: Response, db: Session = Depends(get_db)
):
    """
    시스템 자체 로그인 기능입니다.
    """
    user = basicLoginService(user_data, db)

    # access, refresh token
    access_token = create_access_token(TokenData(userId=user.id, name=user.name))
    refresh_token = create_refresh_token(TokenData(userId=user.id, name=user.name))

    response.headers["Authorization"] = access_token
    response.set_cookie(key="Authorization", value=refresh_token)
    return user


@router.get("/test")
def testController(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    print(authorization.credentials)

    return "good"
