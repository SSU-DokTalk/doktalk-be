from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OAuthSchema(BaseModel):
    id: str = Field()
    user_id: int = Field()

    registration: Optional[str] = None
    created_at: datetime = Field()

    class Config:
        from_attributes = True
