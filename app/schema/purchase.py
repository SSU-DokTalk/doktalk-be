from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


class PurchaseSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    product_id: int = Field()
    product_type: Literal["D", "S"] = Field()
    content: Optional[str] = None
    price: int = Field()
    quantity: int = Field()
    created: datetime = Field()
    updated: datetime = Field()
    is_deleted: bool = Field()
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


__all__ = ["PurchaseSchema"]
