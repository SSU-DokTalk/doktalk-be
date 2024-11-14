from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.controller import user
from app.oauth import oauthController
from app.core.middleware import JWTMiddleware

origins = [
    "http://127.0.0.1:3000",
]


def createApp() -> FastAPI:

    _app = FastAPI()

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
