from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PurchaseSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    product_id: int = Field()
    content: str = Field()
    price: int = Field()
    quantity: int = Field()
    created: datetime = Field()
    updated: datetime = Field()

    class Config:
        from_attributes = True


__all__ = ["PurchaseSchema"]
