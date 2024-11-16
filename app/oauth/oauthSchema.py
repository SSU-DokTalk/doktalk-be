from typing import Optional, Union

from pydantic import BaseModel, Field

from app.schema.enums import PROVIDER


class oAuthLoginInfo(BaseModel):
    uid: Optional[int] = Field(description="oauth 유저의 식별 번호")
    email: Optional[str] = Field(description="oauth 유저의 email")
    name: Optional[str] = Field(None, description="oauth 유저의 닉네임")
    profile: Optional[str] = Field(None, description="oauth 유저의 프로필 이미지 URL")
    provider: Union[str, PROVIDER] = Field(description="소셜 로그인 할 서비스")
