from fastapi import FastAPI
from routers.main_router import router as main_router
from routers.weather_router import router as weather_router

app = FastAPI()

# 라우터 등록
app.include_router(main_router)
app.include_router(weather_router)
