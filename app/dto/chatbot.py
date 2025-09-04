from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatbotRequest(BaseModel):
    message: str
    chat_history: Optional[List[ChatMessage]] = []


class ChatbotResponse(BaseModel):
    response: str
