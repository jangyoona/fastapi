import logging
import re
import google.generativeai as genai
from http import HTTPStatus
from core.config import GEMINI_API_KEY, GEMINI_API_MODEL

logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_API_MODEL)


async def get_weather_description(weather_data: dict) -> str:
    """날씨 데이터를 자연어 설명으로 변환"""
    try:
        prompt = (
            "너는 날씨 요약 생성기다.\n"
            "반드시 한 문장만 출력한다.\n"
            "설명, 추가 문장, 인사말, 해설은 절대 금지다.\n"
            "출력은 반드시 아래 예시와 같은 문장 형태로만 작성한다.\n\n"
            f"[날씨 정보]\n{weather_data}\n\n"
            "[예시]\n"
            "오늘 기온은 25도 정도이며, 맑고 화창한 날씨로 바람은 약간 불고 습도는 낮습니다."
        )
        response = await model.generate_content_async(prompt)
        return response.text
    
    except Exception as e:
        logger.error(f"Gemini API 호출 실패: {type(e).__name__}: {e}")
        
        if e.code == HTTPStatus.TOO_MANY_REQUESTS:

            retry_seconds = None
            for detail in e.details:
                if hasattr(detail, "retry_delay"):
                    retry_seconds = detail.retry_delay.seconds
                    break
            message = quote_exception_message(retry_seconds)
            return message
        else:
            raise


def quote_exception_message(retry_delay: int):
    """API 사용량 초과 시 응답 메세지 규격"""
    retry_time = "알 수 없음"
    if retry_delay is not None:
        minutes = retry_delay // 60
        seconds = retry_delay % 60

        retry_time = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"
    return f"Gemini API 사용량 초과로 인해<br>{retry_time} 동안 날씨 설명을 제공할 수 없습니다."