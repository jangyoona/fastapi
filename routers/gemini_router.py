from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from service.weather_service import resolve_location, get_weather
from service.gemini_service import get_weather_description
from utils.comon import is_allowed_host
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gemini")


@router.post("/weather")
async def weather_with_description(request: dict, req: Request):
    """주소 또는 좌표로 현재 날씨를 조회하고 Gemini가 자연어로 설명"""
    
    # 요청 host 검증
    host = (req.headers.get("x-forwarded-host") or req.headers.get("host") or req.url.hostname).split(":")[0]
    if not is_allowed_host(host):
        raise HTTPException(status_code=403, detail="허용되지 않은 host 입니다.")

    x, y, address = await resolve_location(
        address=request.get("address"),
        longitude=request.get("longitude"),
        latitude=request.get("latitude"),
    )

    weather_data = await get_weather(x, y)
    if not weather_data:
        raise HTTPException(500, detail=f"날씨 데이터 처리 실패: x={x}, y={y}")

    description = await get_weather_description(weather_data)

    return {
        "description": description,
        "weather": weather_data["weather"],
        "address": address,
    }
