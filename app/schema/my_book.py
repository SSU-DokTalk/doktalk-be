from datetime import datetime

from pydantic import BaseModel, Field


class MyBookSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()

    isbn: str = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Config:
        from_attributes = True
