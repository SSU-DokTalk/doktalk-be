from fastapi import HTTPException
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager
from fastapi_pagination import Page, paginate

from app.core.security import cryptContext
from app.db.models.soft_delete import BaseSession as Session
from app.dto.user import *
from app.model.User import User
from app.model.Following import Following
from app.service.file import FileManager


def basicRegisterService(user_data: BasicRegisterReq, db: Session) -> int:
    try:
        user_data.password = cryptContext.hash(user_data.password)
        user = User(user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        # 오류 메시지 분석
        if isinstance(e.orig, PymysqlIntegrityError):
            sql_code = e.orig.args[0]  # MySQL 상태 코드 (1452 또는 1062)

            if sql_code == 1062:  # 중복 키 제약 조건 위반
                raise HTTPException(
                    status_code=409, detail="Duplicate entry for entity like"
                )

        # 기타 IntegrityError 처리
        raise HTTPException(status_code=400, detail="Database integrity error")
    return user.id


def basicLoginService(user_data: BasicLoginReq, db: Session) -> User:
    user = (
        db.query(User, with_deleted=True)
        .filter(User.email == user_data.email)
        .one_or_none()
    )
    if user == None:
        raise HTTPException(status_code=404)
    if not cryptContext.verify(user_data.password, user.password):
        raise HTTPException(status_code=400)
    return user


def getUserInfoService(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if user == None:
        raise HTTPException(status_code=404)
    return user


def isFollowingService(user_id: int, target_user_id: int, db: Session) -> bool:
    following_info = (
        db.query(Following)
        .filter(
            Following.follower_id == user_id, Following.following_id == target_user_id
        )
        .one_or_none()
    )
    return following_info != None


async def updateUserProfileInfoService(
    user_id: int, data: UpdateUserInfoReq, db: Session
) -> User:
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if user == None:
        raise HTTPException(status_code=404)

    if user.profile != data.profile:
        await FileManager.delete_from_s3(user.profile)
    user.profile = data.profile
    user.introduction = data.introduction
    user.name = data.name
    db.commit()
    db.refresh(user)
    return user


def followUserService(user_id: int, target_user_id: int, db: Session) -> None:
    try:
        user = db.query(User).filter(User.id == user_id).one_or_none()
        target_user = db.query(User).filter(User.id == target_user_id).one_or_none()
        if target_user == None:
            raise HTTPException(status_code=404)

        following_info = Following(follower_id=user_id, following_id=target_user_id)
        db.add(following_info)
        user.following_num += 1
        target_user.follower_num += 1
        db.commit()
    except IntegrityError as e:
        if isinstance(e.orig, PymysqlIntegrityError):
            sql_code = e.orig.args[0]
            if sql_code == 1062:
                raise HTTPException(status_code=409)
        raise HTTPException(status_code=400)
    return


def unfollowUserService(user_id: int, target_user_id: int, db: Session) -> None:
    # TODO: try-except 구문을 사용하여 IntegrityError 처리
    # update문을 사용하여 follower_num, following_num 업데이트
    user = db.query(User).filter(User.id == user_id).one_or_none()
    target_user = db.query(User).filter(User.id == target_user_id).one_or_none()
    if target_user == None:
        raise HTTPException(status_code=404)

    following_info = (
        db.query(Following)
        .filter(
            Following.follower_id == user_id, Following.following_id == target_user_id
        )
        .delete()
    )
    db.commit()
    if following_info == 0:
        raise HTTPException(status_code=404)

    user.following_num -= 1
    target_user.follower_num -= 1
    db.commit()
    return


__all__ = [
    "basicRegisterService",
    "basicLoginService",
    "getUserInfoService",
    "isFollowingService",
    "followUserService",
    "updateUserProfileInfoService",
    "unfollowUserService",
]
