from typing import Annotated
import base64

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session, contains_eager
from starlette.responses import JSONResponse

from app.core.security import (
    create_access_token,
    create_refresh_token,
    TokenData,
    oauth2_scheme,
)
from app.core.security import get_token, get_token_payload, encrypt
from app.db.connection import get_db
from app.dto.user import BasicRegisterReq, BasicLoginReq
from app.dto.post import BasicPostRes
from app.model.User import User
from app.model.Post import Post
from app.schema.user import UserSchema
from app.service.user import basicRegisterService, basicLoginService

router = APIRouter()


@router.post("/register")
def basicRegisterController(
    user_data: BasicRegisterReq, db: Session = Depends(get_db)
) -> int:
    """
    시스템 자체 회원가입 기능
    """
    return basicRegisterService(user_data, db)


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

    response.headers["Authorization"] = encrypt(access_token)
    response.set_cookie(
        key="Authorization",
        value=encrypt(refresh_token, base64.b64encode),
    )
    return UserSchema.model_validate(user)


@router.get("/{user_id}/posts")
def getUserPostsController(
    user_id: int, db: Session = Depends(get_db)
) -> Page[BasicPostRes]:
    return paginate(
        db.query(Post)
        .join(Post.user)
        .options(contains_eager(Post.user))
        .filter(Post.user_id == user_id)
        .order_by(Post.created_at.desc())
    )


@router.get("/me")
def getMyInfoController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
) -> UserSchema:
    """
    유저 본인의 정보를 반환하는 API
    """
    return UserSchema.model_validate(request.state.user)


@router.post("/access-token")
def refreshAccessToken(
    refresh_token: str, response: Response, db: Session = Depends(get_db)
) -> None:
    """
    refresh token을 이용해 access token 갱신
    """
    token = get_token(refresh_token, base64.b64decode)
    # Bearer 토큰이 아닌 경우
    if token == None:
        return JSONResponse(status_code=401, content={"detail": "Wrong Token"})

    try:
        payload = get_token_payload(token)
    except ExpiredSignatureError as e:
        return JSONResponse(status_code=401, content={"detail": "Token Expired"})

    # 토큰 내용물이 없는 경우
    if not payload:
        return JSONResponse(status_code=401, content={"detail": "Wrong Token"})

    db: Session = next(get_db())
    try:
        user = db.query(User).filter(User.id == payload.sub).first()
        # 존재하지 않는 유저인 경우
        if user == None:
            return JSONResponse(status_code=401, content={"detail": "Wrong Token"})
        access_token = create_access_token(TokenData(userId=user.id, name=user.name))
        response.headers["Authorization"] = encrypt(access_token)
    finally:
        db.close()

    return
