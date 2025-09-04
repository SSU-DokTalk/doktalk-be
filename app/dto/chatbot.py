from typing import List, Optional, Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "model"]
    message: str


class ChatbotRequest(BaseModel):
    message: str
    chat_history: Optional[List[ChatMessage]] = []


class ChatbotResponse(BaseModel):
    message: str
    success: bool = True
    # chat_history: Optional[List[ChatMessage]] = []
