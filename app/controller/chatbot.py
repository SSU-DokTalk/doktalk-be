from fastapi import APIRouter, HTTPException
from app.dto.chatbot import ChatbotRequest, ChatbotResponse
from app.service.chatbot import ChatbotService

router = APIRouter()

chatbot_service = ChatbotService()


@router.post("", response_model=ChatbotResponse)
async def chat(request: ChatbotRequest):
    """
    챗봇과 대화하기
    - 사용자 메시지와 채팅 히스토리를 받아서 AI 응답을 반환
    """
    try:
        response = await chatbot_service.get_response(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"챗봇 응답 생성 실패: {str(e)}")
