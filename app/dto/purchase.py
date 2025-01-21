from typing import Literal, Optional

from pydantic import BaseModel, Field


class CreatePurchaseReq(BaseModel):
    product_type: Literal["D", "S"] = Field()
    product_id: int = Field()
    content: Optional[str] = None
    price: int = Field()
    quantity: int = Field()

    class Config:
        from_attributes = True


__all__ = ["CreatePurchaseReq"]
