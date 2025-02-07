from typing import Optional

from pydantic import BaseModel, Field

from app.dto.file import FileDto
from app.schema.user import BasicUserSchema
from app.schema.post import PostSchema


class CreatePostReq(BaseModel):
    title: str = Field(examples=["test"], max_length=255)
    content: Optional[str] = None
    files: Optional[list[FileDto]] = None


class BasicPostRes(PostSchema):
    user: BasicUserSchema


__all__ = ["CreatePostReq", "BasicPostRes"]
