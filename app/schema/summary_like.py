from pydantic import BaseModel, Field


class SummaryLikeSchema(BaseModel):
    user_id: int = Field()
    summary_id: int = Field()

    class Config:
        from_attributes = True


__all__ = ["SummaryLikeSchema"]
