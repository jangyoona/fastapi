from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os

load_dotenv("env/.env")

serviceKey = os.getenv("SERVICE_KEY")
kakaoUrl = os.getenv("KAKAO_URL")
weatherUrl = os.getenv("WEATHER_URL")

# httpx 클라이언트를 재사용 (커넥션 풀링)
router = APIRouter(prefix="/weather")
client = httpx.AsyncClient()

print(os.getenv("SERVICE_KEY"))


@router.get("/now/{address}")
async def now(address: str):
    data = await currentLocation(address)

    # 주소 검색 결과 없음
    if not data or "documents" not in data or len(data["documents"]) == 0:
        raise HTTPException(status_code=404, detail="주소 위도/경도 데이터 없음")

    x = data["documents"][0].get("x")
    y = data["documents"][0].get("y")

    # x, y 값 없음
    if not x or not y:
        raise HTTPException(status_code=404, detail="좌표 데이터 없음")

    print(f"x: {x}, y: {y}")

    # async 함수 호출 시 await 필수
    result = await getWeather(x, y)

    return result


async def currentLocation(address: str):
    currUrl = kakaoUrl + address
    headers = {
        "Authorization": f"KakaoAK {serviceKey}"
    }

    response = await client.get(
        currUrl, 
        headers=headers
    )
    response.raise_for_status() # 4xx/5xx면 예외 발생

    return response.json()


async def getWeather(x: str, y: str):
    params = {
        "latitude": y,
        "longitude": x,
        "current": "temperature_2m,weather_code,relative_humidity_2m"
    }

    response = await client.get(
        weatherUrl, 
        params=params
    )

    response.raise_for_status() # 4xx/5xx면 예외 발생

    return response.json()