from datetime import datetime

from pydantic import BaseModel, Field


class AgreementSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()

    term: int = Field()
    created: datetime = Field()
    updated: datetime = Field()

    class Config:
        from_attributes = True


__all__ = ["AgreementSchema"]
