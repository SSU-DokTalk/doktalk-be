from pydantic import BaseModel, Field


class DebateLikeSchema(BaseModel):
    user_id: int = Field()
    debate_id: int = Field()

    class Config:
        from_attributes = True


__all__ = ["DebateLikeSchema"]
