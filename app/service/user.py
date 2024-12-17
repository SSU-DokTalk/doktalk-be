from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import cryptContext
from app.core.config import settings
from app.db.s3 import s3_client
from app.dto.user import BasicLoginReq, BasicRegisterReq, UpdateUserInfoReq
from app.model.User import User
from app.service.image import ImageFile


def basicRegisterService(user_data: BasicRegisterReq, db: Session) -> int:
    try:
        user_data.password = cryptContext.hash(user_data.password)
        user = User(user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        raise HTTPException(status_code=400)
    return user.id


def basicLoginService(user_data: BasicLoginReq, db: Session) -> User:
    user = db.query(User).filter(User.email == user_data.email).one_or_none()
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


async def updateUserProfileInfoService(
    user_id: int, data: UpdateUserInfoReq, db: Session
) -> User:
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if user == None:
        raise HTTPException(status_code=404)

    if user.profile != data.profile:
        await ImageFile.delete_from_s3(user.profile)
    user.profile = data.profile
    user.introduction = data.introduction
    user.name = data.name
    db.commit()
    db.refresh(user)
    return user


__all__ = [
    "basicRegisterService",
    "basicLoginService",
    "getUserInfoService",
    "updateUserProfileInfoService",
]
