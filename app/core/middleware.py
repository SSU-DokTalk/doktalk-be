from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import get_token, get_token_payload
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.model.User import User
from jwt.exceptions import ExpiredSignatureError
from starlette.responses import JSONResponse


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        print(request.url.path)
        print(request.method)

        #
        # 토큰 검증이 필요없다면 넘어가기
        #
        if request.method == "GET":
            token_not_needed = [
                "/docs",
                "/openapi.json",
                "/oauth/kakao",
                "/oauth/google",
            ]
            if request.url.path in token_not_needed:
                return await call_next(request)
        elif request.method == "POST":
            token_not_needed = ["/user/register", "/user/login"]
            if request.url.path in token_not_needed:
                return await call_next(request)
        elif request.method == "PUT":
            token_not_needed = []
            if request.url.path in token_not_needed:
                return await call_next(request)
        elif request.method == "DELETE":
            token_not_needed = []
            if request.url.path in token_not_needed:
                return await call_next(request)

        #
        # 토큰 검증이 필요한 경우
        #
        authorization = request.headers.get("Authorization")

        token = get_token(authorization)
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

            return await call_next(request)
        finally:
            db.close()
