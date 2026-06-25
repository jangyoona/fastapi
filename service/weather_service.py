import httpx
from core.config import SERVICE_KEY, KAKAO_URL, WEATHER_URL

client = httpx.AsyncClient()


async def get_current_location(address: str):
    """입력 주소 기반 좌표 반환"""
    
    headers = {"Authorization": f"KakaoAK {SERVICE_KEY}"}
    response = await client.get(KAKAO_URL + address, headers=headers)
    response.raise_for_status()
    return response.json()


async def get_weather(x: str, y: str):
    """위도/경도 기반 현재 날씨 반환"""

    params = {
        "latitude": y,
        "longitude": x,
        "current": "temperature_2m,weather_code,relative_humidity_2m"
    }
    response = await client.get(WEATHER_URL, params=params)
    response.raise_for_status()

    return format_weather_data(response.json())


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
