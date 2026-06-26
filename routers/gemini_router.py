from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from service.weather_service import resolve_location, get_weather
from service.gemini_service import get_weather_description
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gemini")


@router.post("/weather")
async def weather_with_description(request: dict):
    """주소 또는 좌표로 현재 날씨를 조회하고 Gemini가 자연어로 설명"""
    x, y, address = await resolve_location(
        address=request.get("address"),
        longitude=request.get("longitude"),
        latitude=request.get("latitude"),
    )

    weather_data = await get_weather(x, y)
    if not weather_data:
        raise HTTPException(500, detail=f"날씨 데이터 처리 실패: x={x}, y={y}")

    description = await get_weather_description(weather_data)

    return JSONResponse(
        status_code=200,
        content={
            "description": description,
            "weather": weather_data["weather"],
            "address": address,
        }
    )
