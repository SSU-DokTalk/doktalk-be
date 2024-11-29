from pydantic import BaseModel, Field


class DebateLikeSchema(BaseModel):
    id: int = Field()
    user_id: int = Field()
    debate_id: int = Field()

    class Config:
        from_attributes = True
