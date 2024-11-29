import re

from jwt.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import get_token, get_token_payload
from app.db.connection import get_db
from app.model.User import User


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        # print(f"{request.method} {request.url.path}")

        #
        # 토큰 검증이 필요없다면 넘어가기
        #
        token_not_needed = list()
        if request.method == "GET":
            token_not_needed = [
                r"/(favicon.ico|docs|openapi.json)",
                r"/oauth/(kakao|google|naver|facebook)",
                r"/post/(recent)",
                r"/post/([0-9]+)(/(comments))?",
                r"/user/([0-9]+)/(posts)",
            ]
        elif request.method == "POST":
            token_not_needed = [r"/user/(register|login|access-token)"]
        elif request.method == "PUT":
            token_not_needed = []
        elif request.method == "DELETE":
            token_not_needed = []

        for path in token_not_needed:
            if re.fullmatch(path, request.url.path) is not None:
                return await call_next(request)

        #
        # 토큰 검증이 필요한 경우
        #

        authorization = request.headers.get("Authorization")
        if authorization == None:
            return JSONResponse(status_code=401, content={"detail": "Wrong Token"})

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
            request.state.user = user
            return await call_next(request)
        finally:
            db.close()
