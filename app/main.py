from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from app.controller import user, post, summary, image
from app.core.middleware import JWTMiddleware
from app.oauth import oauthController

origins = ["*"]


def createApp() -> FastAPI:

    SWAGGER_HEADERS = {
        "title": "讀:Talk API",
        "version": "v1",
        "description": "讀:Talk 서비스에서 제공하는 API 목록입니다.",
        "contact": {
            "license_info": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT",
            },
        },
    }

    _app = FastAPI(
        swagger_ui_parameters={
            "deepLinking": True,
            "displayRequestDuration": True,
            "operationsSorter": "method",
            "filter": True,
            "tagsSorter": "alpha",
            "syntaxHighlight.theme": "tomorrow-night",
        },
        **SWAGGER_HEADERS
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(JWTMiddleware)
    add_pagination(_app)

    _app.include_router(user.router, prefix="/user", tags=["사용자 user"])
    _app.include_router(post.router, prefix="/post", tags=["게시글 post"])
    _app.include_router(summary.router, prefix="/summary", tags=["요약 summary"])
    _app.include_router(image.router, prefix="/image", tags=["이미지 업로드 image"])
    _app.include_router(
        oauthController.router, prefix="/oauth", tags=["소셜 로그인 oauth"]
    )
    return _app


app = createApp()
