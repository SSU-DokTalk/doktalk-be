from fastapi import APIRouter
from app.dto.chatbot import ChatbotRequest, ChatbotResponse
from app.service.chatbot import send_message

router = APIRouter()


@router.post("", response_model=ChatbotResponse)
async def chat(request: ChatbotRequest) -> ChatbotResponse:
    """
    챗봇과 대화하기
    - 사용자 메시지와 채팅 히스토리를 받아서 AI 응답을 반환
    """

    response = await send_message(request)

    # Service에서 이미 에러 처리를 했으므로 그대로 반환
    return response
