from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schema.user import BasicUserSchema
from app.schema.post import PostSchema


class CreatePostReq(BaseModel):
    title: str = Field(examples=["test"], max_length=255)
    content: Optional[str] = None
    files: Optional[list[HttpUrl]] = None

    @field_validator("files", mode="before")
    def remove_empty_strings_from_files(
        value: Optional[List[str]],
    ) -> Optional[List[str]]:
        if value:
            return [file for file in value if (file != "" or file is not None)]
        return value


class BasicPostRes(PostSchema):
    user: BasicUserSchema


__all__ = ["CreatePostReq", "BasicPostRes"]
