from pydantic import BaseModel, Field


class SummaryLikeSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    summary_id: int = Field()

    class Config:
        from_attributes = True
