from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import cryptContext
from app.dto.user import BasicLoginReq, BasicRegisterReq
from app.model.User import User


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
    user = db.query(User).filter(User.email == user_data.email).first()
    if user == None:
        raise HTTPException(status_code=404)
    if not cryptContext.verify(user_data.password, user.password):
        raise HTTPException(status_code=400)
    return user
