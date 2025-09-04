from app.dto.chatbot import ChatbotRequest, ChatbotResponse


class ChatbotService:
    def __init__(self):
        # TODO: Google API 클라이언트 초기화
        pass

    async def get_response(self, request: ChatbotRequest) -> ChatbotResponse:
        """
        사용자 메시지에 대한 챗봇 응답 생성

        Args:
            request: 사용자 메시지와 채팅 히스토리

        Returns:
            ChatbotResponse: 챗봇 응답
        """
        # TODO: Google API를 사용한 응답 생성 로직 구현
        # 1. 채팅 히스토리와 새 메시지를 조합
        # 2. Google API에 요청 전송
        # 3. 응답 파싱 및 반환

        # 임시 응답
        response_text = f"받은 메시지: {request.message}"

        return ChatbotResponse(
            response=response_text,
            status="success"
        )
