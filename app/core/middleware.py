import re

from jwt.exceptions import ExpiredSignatureError
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import get_token, get_token_payload
from app.db.connection import get_db
from app.db.models.soft_delete import BaseSession as Session
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
                r"/debate/(([0-9]+)(/(comments))?)",
                r"/oauth/(kakao|google|naver|facebook)",
                r"/post/((recent)|(([0-9]+)(/(comments))?))",
                r"/summary/(([0-9]+)(/(comments))?)",
                r"/user/(([0-9]+)(/(posts|summaries|mybooks))?)",
                r"/book(s|/([0-9]+))",
            ]
        elif request.method == "POST":
            token_not_needed = [r"/user/(register|login|access-token)"]
        elif request.method == "PUT":
            token_not_needed = []
        elif request.method == "PATCH":
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
            return JSONResponse(status_code=401, content={"errorCode": "MD1000"})

        token = get_token(authorization)
        # Bearer 토큰이 아닌 경우
        if token == None:
            return JSONResponse(status_code=401, content={"errorCode": "MD1001"})

        try:
            payload = get_token_payload(token)
        except ExpiredSignatureError as e:
            return JSONResponse(status_code=401, content={"errorCode": "MD1002"})
        except Exception as e:
            return JSONResponse(status_code=401, content={"errorCode": "MD1003"})

        # 토큰 내용물이 없는 경우
        if not payload:
            return JSONResponse(status_code=401, content={"errorCode": "MD1004"})

        db: Session = next(get_db())
        try:
            user = (
                db.query(
                    User,
                    with_deleted=(
                        True if request.url.path == "/user/restore" else False
                    ),
                )
                .filter(User.id == payload.sub)
                .first()
            )
            # 존재하지 않는 유저인 경우
            if user == None:
                return JSONResponse(status_code=401, content={"errorCode": "MD1005"})
            request.state.user = user
            return await call_next(request)
        finally:
            db.close()
