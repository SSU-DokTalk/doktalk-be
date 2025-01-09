from typing import Literal

from pydantic import BaseModel, Field


class CreatePurchaseReq(BaseModel):
    user_id: int = Field()
    product_type: Literal["D", "S"] = Field()
    product_id: int = Field()
    content: str = Field()
    price: int = Field()
    quantity: int = Field()

    class Config:
        from_attributes = True


__all__ = ["CreatePurchaseReq"]
