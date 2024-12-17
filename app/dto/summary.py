from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.summary import SummarySchema
from app.schema.user import BasicUserSchema


class CreateSummaryReq(BaseModel):
    isbn: str = Field()
    title: str = Field()
    free_content: Optional[list[str]] = None
    charged_content: Optional[list[str]] = None
    price: int = Field()
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None

    @field_validator("image1", "image2", mode="before")
    def empty_string_to_none(value: str) -> Optional[str]:
        if value == "":  # 빈 문자열인 경우 None으로 변환
            return None
        return value

    class Config:
        from_attributes = True


class BasicSummaryRes(SummarySchema):
    user: BasicUserSchema


__all__ = ["CreateSummaryReq", "BasicSummaryRes"]
