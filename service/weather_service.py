import logging
import httpx
from fastapi import HTTPException
from core.config import KAKAO_API_KEY, KAKAO_API_URL, KAKAO_COORD_URL, WEATHER_URL

logger = logging.getLogger(__name__)
client = httpx.AsyncClient()


async def get_current_coord_location(longitude: float, latitude: float):
    """입력 좌표 기반 주소 반환"""
    try:
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        params = {"x": longitude, "y": latitude}
        response = await client.get(KAKAO_COORD_URL, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"카카오 API 오류: {e.response.status_code} {e.response.text}")
        raise HTTPException(e.response.status_code)
    except httpx.RequestError as e:
        logger.error(f"카카오 API 네트워크 오류: {type(e).__name__}: {e}")
        raise HTTPException(500)


async def resolve_location(address: str | None, longitude: float | None, latitude: float | None) -> tuple[str, str, str]:
    """주소 또는 좌표를 받아 (x, y, address_name) 반환"""
    if latitude and longitude:
        data = await get_current_coord_location(longitude, latitude)
        if not data or "documents" not in data or len(data["documents"]) == 0:
            raise HTTPException(404, detail=f"좌표에 해당하는 주소 없음: x={longitude}, y={latitude}")
        document = data["documents"][0]
        return str(longitude), str(latitude), document.get("address_name")
    else:
        data = await get_current_location(address)
        if not data or "documents" not in data or len(data["documents"]) == 0:
            raise HTTPException(404, detail=f"주소 위도/경도 데이터 없음: {address}")
        document = data["documents"][0]
        x, y = document.get("x"), document.get("y")
        if not x or not y:
            raise HTTPException(404, detail=f"좌표 데이터 없음: x={x}, y={y}")
        return x, y, document.get("address_name")

async def get_current_location(address: str):
    """입력 주소 기반 좌표 반환"""
    try:
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        response = await client.get(KAKAO_API_URL + address, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"카카오 API 오류: {e.response.status_code} {e.response.text}")
        raise HTTPException(e.response.status_code)
    except httpx.RequestError as e:
        logger.error(f"카카오 API 네트워크 오류: {type(e).__name__}: {e}")
        raise HTTPException(500)


async def get_weather(x: str, y: str):
    """위도/경도 기반 현재 날씨 반환"""
    try:
        params = {
            "latitude": y,
            "longitude": x,
            "current": "temperature_2m,weather_code,relative_humidity_2m"
        }
        response = await client.get(WEATHER_URL, params=params)
        response.raise_for_status()
        return format_weather_data(response.json())
    except httpx.HTTPStatusError as e:
        logger.error(f"날씨 API 오류: {e.response.status_code} {e.response.text}")
        raise HTTPException(e.response.status_code)
    except httpx.RequestError as e:
        logger.error(f"날씨 API 네트워크 오류: {type(e).__name__}: {e}")
        raise


def format_weather_data(weather_data):
    """API 응답 포맷팅"""

    if not weather_data or "current" not in weather_data:
        return None

    current = weather_data.get("current")

    temperature = current.get("temperature_2m")

    weather_code = current.get("weather_code")
    weather_str = get_weather_description(weather_code)

    formatted_data = {
        "temperature": temperature,
        "weather": weather_str
    }

    return formatted_data


def get_weather_description(code: int) -> str:
    """API 응답 코드에 따른 날씨 상태 문자열 반환"""

    if code == 0:
        return "맑음"
    elif code in (1, 2, 3):
        return "구름 조금 ~ 흐림"
    elif code in (45, 48):
        return "안개"
    elif code in (51, 53, 55):
        return "이슬비"
    elif code in (61, 63, 65):
        return "비"
    elif code in (71, 73, 75):
        return "눈"
    elif code in (80, 81, 82):
        return "소나기"
    elif code in (95, 99):
        return "뇌우"
    else:
        return "알 수 없음"
