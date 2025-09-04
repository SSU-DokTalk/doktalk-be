from typing import List
from google import genai
from google.genai import types

from app.var import CHATBOT_SYSTEM_INSTRUCTION
from app.dto.chatbot import ChatMessage, ChatbotRequest, ChatbotResponse


async def send_message(request: ChatbotRequest) -> ChatbotResponse:
    """
    Google Gemini API를 사용하여 사용자 메시지에 대한 챗봇 응답 생성

    Args:
        request (ChatbotRequest): 사용자 메시지와 이전 채팅 히스토리를 포함한 요청 객체
            - message (str): 사용자가 보낸 새로운 메시지
            - chat_history (List[ChatMessage]): 이전 대화 기록 (선택사항)

    Returns:
        ChatbotResponse: 챗봇 응답 객체 (성공/실패 상태 포함)

    Raises:
        Exception: 복구 불가능한 시스템 에러 시에만 발생
    """
    try:
        # ChatbotRequest.chat_history를 ContentDict 리스트로 변환
        history = []
        for chat_message in request.chat_history:
            content_dict = {
                "role": chat_message.role,  # "user" 또는 "model"
                "parts": [{"text": chat_message.message}]
            }
            history.append(content_dict)

        client = genai.Client()

        chat = client.aio.chats.create(
            model='gemini-2.5-flash', history=history, config={
                'system_instruction': CHATBOT_SYSTEM_INSTRUCTION
            }
        )

        response = await chat.send_message(request.message)

        return ChatbotResponse(
            message=response.text,
            success=True,
            # 당장은 필요 없어보여 주석처리함.
            # chat_history=request.chat_history +
            # [
            #     {'role': 'user', 'message': request.message},
            #     {'role': 'model', 'message': response.text}
            # ]
        )

    except Exception as e:
        return ChatbotResponse(
            message="죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            success=False
        )
