from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class CreateSummaryReq(BaseModel):
    isbn: str = Field()
    title: str = Field()
    free_content: Optional[list[str]] = None
    charged_content: Optional[list[str]] = None
    price: int = Field()
    image1: Optional[HttpUrl] = None
    image2: Optional[HttpUrl] = None

    class Config:
        from_attributes = True
