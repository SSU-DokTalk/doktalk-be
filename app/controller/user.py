from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    TokenData,
    oauth2_scheme,
)
from app.db.connection import get_db
from app.model.User import User
from app.service.user import basicRegisterService, basicLoginService
from app.schema.user import BasicRegisterReq, BasicLoginReq

router = APIRouter()


@router.post("/register")
def basicRegisterController(user_data: BasicRegisterReq, db: Session = Depends(get_db)):
    """
    시스템 자체 회원가입 기능
    """
    userId = basicRegisterService(user_data, db)
    return userId


@router.post("/login")
def basicLoginController(
    user_data: BasicLoginReq, response: Response, db: Session = Depends(get_db)
):
    """
    시스템 자체 로그인 기능
    """
    user = basicLoginService(user_data, db)

    # access, refresh token
    access_token = create_access_token(TokenData(userId=user.id, name=user.name))
    refresh_token = create_refresh_token(TokenData(userId=user.id, name=user.name))

    response.headers["Authorization"] = access_token
    response.set_cookie(key="Authorization", value=refresh_token)
    return user


@router.get("/me")
def getMyInfoController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    """
    유저 본인의 정보를 반환하는 API
    """
    user: User = request.state.user

    return user
