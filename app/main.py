from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.controller import user
from app.core.middleware import JWTMiddleware
from app.oauth import oauthController

origins = [
    "http://127.0.0.1:3000",
]


def createApp() -> FastAPI:

    SWAGGER_HEADERS = {
        "title": "독:Talk API",
        "version": "v1",
        "description": "독:Talk 서비스에서 제공하는 API 목록입니다.",
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

    _app.include_router(user.router, prefix="/user")
    _app.include_router(oauthController.router, prefix="/oauth")
    return _app


app = createApp()
