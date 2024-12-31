from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OAuthSchema(BaseModel):
    id: str = Field()
    user_id: int = Field()

    registration: Optional[str] = None
    created: datetime = Field()

    class Config:
        from_attributes = True


__all__ = ["OAuthSchema"]
