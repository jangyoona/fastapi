from fastapi import APIRouter, HTTPException
from service.weather_service import get_current_location, get_weather

router = APIRouter(prefix="/weather")


@router.get("/now/{address}")
async def now(address: str):
    data = await get_current_location(address)

    if not data or "documents" not in data or len(data["documents"]) == 0:
        raise HTTPException(status_code=404, detail="주소 위도/경도 데이터 없음")

    x = data["documents"][0].get("x")
    y = data["documents"][0].get("y")

    if not x or not y:
        raise HTTPException(status_code=404, detail="좌표 데이터 없음")

    return await get_weather(x, y)
