from datetime import datetime

from pydantic import BaseModel, Field


class MyBookSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    isbn: int = Field()

    created: datetime = Field()
    updated: datetime = Field()

    class Config:
        from_attributes = True


__all__ = ["MyBookSchema"]
