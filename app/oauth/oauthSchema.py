from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, Field


class PROVIDER(Enum):
    KAKAO = "kakao"
    NAVER = "naver"
    GOOGLE = "google"
    FACEBOOK = "facebook"

    @classmethod
    def from_str(cls, name: str):
        for enum in cls:
            if enum.value == name:
                return enum


class oAuthLoginInfo(BaseModel):
    uid: Optional[int] = Field(description="oauth 유저의 식별 번호")
    email: Optional[str] = Field(description="oauth 유저의 email")
    name: Optional[str] = Field(None, description="oauth 유저의 닉네임")
    profile: Optional[str] = Field(None, description="oauth 유저의 프로필 이미지 URL")
    provider: Union[str, PROVIDER] = Field(description="소셜 로그인 할 서비스")
