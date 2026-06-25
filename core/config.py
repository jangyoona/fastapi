from dotenv import load_dotenv
import os

load_dotenv("env/.env")

SERVICE_KEY = os.getenv("SERVICE_KEY")
KAKAO_URL = os.getenv("KAKAO_URL")
WEATHER_URL = os.getenv("WEATHER_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_MODEL = os.getenv("GEMINI_API_MODEL")