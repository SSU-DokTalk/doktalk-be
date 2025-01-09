from typing import Annotated
import base64

from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy.orm import contains_eager
from starlette.responses import JSONResponse

from app.core.security import (
    create_access_token,
    create_refresh_token,
    TokenData,
    oauth2_scheme,
)
from app.core.security import (
    get_token,
    get_token_payload,
    encrypt,
    REFRESH_TOKEN_EXPIRATION,
)
from app.db.connection import get_db
from app.db.models.soft_delete import BaseSession as Session
from app.dto.following import BasicFollowingSchema, BasicFollowerSchema
from app.dto.my_book import BasicMyBookRes
from app.dto.post import BasicPostRes
from app.dto.summary import BasicSummaryRes
from app.dto.debate import BasicDebateRes
from app.dto.user import BasicRegisterReq, BasicLoginReq, UpdateUserInfoReq
from app.model import Post, Summary, User, Following, MyBook, Debate
from app.schema.user import UserSchema
from app.schema.purchase import PurchaseSchema
from app.service.file import FileManager
from app.service.user import *
from app.service.purchase import getPurchasesService

router = APIRouter()


###########
### GET ###
###########
@router.get("/me")
def getMyInfoController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
) -> UserSchema:
    """
    유저 본인의 정보를 반환하는 API
    """
    return UserSchema.model_validate(request.state.user)


@router.get("/purchase")
def getPurchasesController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> PurchaseSchema:
    """
    본인의 구매 내역 조회
    """
    return getPurchasesService(request.state.user.id, db)


@router.get("/{user_id}")
def getUserInfoController(user_id: int, db: Session = Depends(get_db)) -> UserSchema:
    """
    유저의 정보를 반환하는 API
    """
    return getUserInfoService(user_id, db)


@router.get("/{user_id}/posts")
def getUserPostsController(
    user_id: int, db: Session = Depends(get_db)
) -> Page[BasicPostRes]:
    return paginate(
        db.query(Post)
        .join(Post.user)
        .options(contains_eager(Post.user))
        .filter(Post.user_id == user_id)
        .order_by(Post.created.desc())
    )


@router.get("/{user_id}/summaries")
def getUserSummariesController(
    user_id: int, db: Session = Depends(get_db)
) -> Page[BasicSummaryRes]:
    return paginate(
        db.query(Summary)
        .join(Summary.user)
        .join(Summary.book)
        .options(contains_eager(Summary.user))
        .options(contains_eager(Summary.book))
        .filter(Summary.user_id == user_id)
        .order_by(Summary.created.desc())
    )


@router.get("/{user_id}/mybooks")
def getMyBooksController(
    user_id: int, db: Session = Depends(get_db)
) -> Page[BasicMyBookRes]:
    return paginate(
        db.query(MyBook)
        .join(MyBook.user)
        .join(MyBook.book)
        .options(contains_eager(MyBook.user))
        .options(contains_eager(MyBook.book))
        .filter(MyBook.user_id == user_id)
        .order_by(MyBook.created.desc())
    )


@router.get("/{user_id}/purchased-summaries")
def getPurchasedSummariesController(
    user_id: int, db: Session = Depends(get_db)
) -> Page[BasicSummaryRes]:
    pass


@router.get("/{user_id}/debates")
def getUserDebatesController(
    user_id: int, db: Session = Depends(get_db)
) -> Page[BasicDebateRes]:
    return paginate(
        db.query(Debate)
        .join(Debate.user)
        .join(Debate.book)
        .options(contains_eager(Debate.user))
        .options(contains_eager(Debate.book))
        .filter(Debate.user_id == user_id)
        .order_by(Debate.created.desc())
    )


@router.get("/{user_id}/purchased-debates")
def getPurchasedDebatesController(
    user_id: int, db: Session = Depends(get_db)
) -> Page[BasicDebateRes]:
    pass


@router.get("/{user_id}/followers")
def getFollowersController(
    user_id: int,
    authozation: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> Page[BasicFollowerSchema]:
    """
    user_id의 팔로워 목록 조회
    """
    return paginate(
        db.query(Following)
        .join(User, Following.follower_id == User.id)
        .filter(Following.following_id == user_id)
        .options(contains_eager(Following.follower))
        .order_by(Following.created.desc())
    )


@router.get("/{user_id}/followings")
def getFollowersController(
    user_id: int,
    authozation: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> Page[BasicFollowingSchema]:
    """
    user_id의 팔로잉 목록 조회
    """
    return paginate(
        db.query(Following)
        .join(User, Following.following_id == User.id)
        .filter(Following.follower_id == user_id)
        .options(contains_eager(Following.following))
        .order_by(Following.created.desc())
    )


@router.get("/is-following/{target_user_id}")
def isFollowingController(
    target_user_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> bool:
    """
    팔로우 여부 확인
    """
    return isFollowingService(request.state.user.id, target_user_id, db)


############
### POST ###
############
@router.post("/restore", status_code=201)
def restoreUserController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    user = (
        db.query(User, with_deleted=True)
        .filter(User.id == request.state.user.id)
        .one_or_none()
    )
    if not user.is_deleted:
        raise HTTPException(status_code=400)
    user.restore()
    db.commit()
    return


@router.post("/register", status_code=201)
def basicRegisterController(
    user_data: BasicRegisterReq, db: Session = Depends(get_db)
) -> int:
    """
    시스템 자체 회원가입 기능
    """
    return basicRegisterService(user_data, db)


@router.post("/login", status_code=201)
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
        expires=int(REFRESH_TOKEN_EXPIRATION.total_seconds()),
    )
    return UserSchema.model_validate(user)


@router.post("/access-token", status_code=201)
def refreshAccessToken(
    refresh_token: str, response: Response, db: Session = Depends(get_db)
) -> None:
    """
    refresh token을 이용해 access token 갱신
    """
    token = get_token(refresh_token, base64.b64decode)
    # Bearer 토큰이 아닌 경우
    if token == None:
        return JSONResponse(status_code=401, content={"errorCode": "U1001"})

    try:
        payload = get_token_payload(token)
    except ExpiredSignatureError as e:
        return JSONResponse(status_code=401, content={"errorCode": "U1002"})
    except Exception as e:
        return JSONResponse(status_code=401, content={"errorCode": "U1003"})

    # 토큰 내용물이 없는 경우
    if not payload:
        return JSONResponse(status_code=401, content={"errorCode": "U1004"})

    db: Session = next(get_db())
    try:
        user = db.query(User, with_deleted=True).filter(User.id == payload.sub).first()
        # 존재하지 않는 유저인 경우
        if user == None:
            return JSONResponse(status_code=401, content={"errorCode": "U1005"})

        # access, refresh token
        access_token = create_access_token(TokenData(userId=user.id, name=user.name))
        refresh_token = create_refresh_token(TokenData(userId=user.id, name=user.name))

        response.headers["Authorization"] = encrypt(access_token)
        response.set_cookie(
            key="Authorization",
            value=encrypt(refresh_token, base64.b64encode),
            expires=int(REFRESH_TOKEN_EXPIRATION.total_seconds()),
        )
    finally:
        db.close()

    return


@router.post("/follow/{target_user_id}", status_code=201)
def followUserController(
    target_user_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    유저 팔로우
    """
    return followUserService(request.state.user.id, target_user_id, db)


###########
### PUT ###
###########


#############
### PATCH ###
#############
@router.patch("/me")
async def updateUserInfoController(
    data: UpdateUserInfoReq,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> UserSchema:
    return await updateUserProfileInfoService(request.state.user.id, data, db)


##############
### DELETE ###
##############
@router.delete("/profile")
async def deleteUserProfileController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    user: User = request.state.user
    await FileManager.delete_from_s3(file_path=user.profile)
    user_in_db = db.query(User).filter(User.id == user.id).one_or_none()
    user_in_db.profile = None
    db.commit()
    return


@router.delete("/me")
def deleteUserController(
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    user = db.query(User).filter(User.id == request.state.user.id).one_or_none()
    if user.is_deleted:
        raise HTTPException(status_code=404)
    if user:
        user.soft_delete()
        db.commit()
    return


@router.delete("/follow/{target_user_id}")
def unfollowUserController(
    target_user_id: int,
    request: Request,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> None:
    """
    유저 언팔로우
    """
    return unfollowUserService(request.state.user.id, target_user_id, db)
