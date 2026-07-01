from fastapi import FastAPI
from routers.main_router import router as main_router
from routers.weather_router import router as weather_router
from routers.gemini_router import router as gemini_router
from exceptions.handlers import register_exception_handlers
import logging

app = FastAPI()

register_exception_handlers(app)

app.include_router(main_router)
app.include_router(weather_router)
app.include_router(gemini_router)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s    %(levelname)-8s    (%(thread)d)    --   %(name)-30s  :  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)