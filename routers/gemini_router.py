from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from service.weather_service import get_current_location, get_weather
from service.gemini_service import get_weather_description
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gemini")


@router.get("/weather/{address}")
async def weather_with_description(address: str):
    """주소로 현재 날씨를 조회하고 Gemini가 자연어로 설명"""
    data = await get_current_location(address)

    if not data or "documents" not in data or len(data["documents"]) == 0:
        raise HTTPException(404, detail=f"주소 위도/경도 데이터 없음: {address}")

    x = data["documents"][0].get("x")
    y = data["documents"][0].get("y")

    if not x or not y:
        raise HTTPException(404, detail=f"좌표 데이터 없음: x={x}, y={y}")

    weather_data = await get_weather(x, y)
    if not weather_data:
        raise HTTPException(500, detail=f"날씨 데이터 처리 실패: x={x}, y={y}")

    description = await get_weather_description(weather_data)

    return JSONResponse(
        status_code=200,
        content={
            "description": description
        }
    )
