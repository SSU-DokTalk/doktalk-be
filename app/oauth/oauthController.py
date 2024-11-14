from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import (
    random_password,
    TokenData,
    create_access_token,
    create_refresh_token,
)
from app.db.connection import get_db
from app.model.User import OAuth
from app.oauth.oauthSchema import *
from app.oauth.oauthService import *
from app.schema.user import *
from app.service.user import *

router = APIRouter()


@router.get("/{provider}", description="소셜 로그인 및 회원가입")
async def oAuthRegisterController(
    provider: PROVIDER,
    code: str,
    response: Response,
    db: Session = Depends(get_db),
):
    provider = PROVIDER.from_str(provider.name.lower())
    if not provider:
        raise HTTPException(status_code=404)

    try:
        if provider == PROVIDER.KAKAO:
            user_data = auth_kakao(code)
        elif provider == PROVIDER.GOOGLE:
            user_data = auth_google(code)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request"
            )

        # DB에서 oauth 정보로 user 받아오기
        user = (
            db.query(User)
            .join(OAuth, OAuth.userId == User.id)
            .filter(OAuth.id == f"{provider.name} {user_data.uid}")
            .first()
        )

        # 해당 oauth 정보가 없는 경우
        if user == None:
            # 동일한 이메일로 가입된 계정이 있는지 확인
            user = db.query(User).filter(User.email == user_data.email).first()
            if user == None:
                # 해당 이메일로 가입된 계정이 없다면 새로운 유저를 생성
                user = User(
                    BasicRegisterReq(
                        email=user_data.email,
                        password=random_password(),
                        name=user_data.name,
                        profile=user_data.profile,
                    )
                )
                print(user.password)
                user.password = cryptContext.hash(user.password)
                db.add(user)
                db.commit()
                db.refresh(user)

            # oAuth 정보 추가
            oauth = OAuth(
                f"{user_data.provider} {user_data.uid}", user.id, user_data.provider
            )
            db.add(oauth)
            db.commit()

        # access, refresh token
        access_token = create_access_token(TokenData(userId=user.id, name=user.name))
        refresh_token = create_refresh_token(TokenData(userId=user.id, name=user.name))

        response.headers["Authorization"] = access_token
        response.set_cookie(key="Authorization", value=refresh_token)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
