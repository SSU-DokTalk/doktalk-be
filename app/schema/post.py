from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl, field_validator


class PostSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()

    title: str = Field()
    content: Optional[str] = None
    files: Optional[List[HttpUrl]] = None
    likes_num: int = Field()
    comments_num: int = Field()
    created: datetime = Field()
    updated: datetime = Field()

    @field_validator("files", mode="before")
    def remove_empty_strings_from_files(
        value: Optional[List[str]],
    ) -> Optional[List[str]]:
        if value:
            return [file for file in value if (file != "" or file is not None)]
        return value

    class Config:
        from_attributes = True


__all__ = ["PostSchema"]
