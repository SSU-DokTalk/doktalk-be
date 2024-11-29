from fastapi import HTTPException
from sqlalchemy.orm import Session, contains_eager

from app.core.security import cryptContext
from app.dto.user import BasicLoginReq, BasicRegisterReq
from app.model.User import User
from app.model.Post import Post


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


def getUserPostsService(user_id: int, db: Session):
    return (
        db.query(Post)
        .join(Post.user)
        .options(contains_eager(Post.user))
        .filter(Post.user_id == user_id)
        .order_by(Post.created_at.desc())
        .all()
    )
