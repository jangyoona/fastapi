from dotenv import load_dotenv
import os

load_dotenv("env/.env")

KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")
KAKAO_API_URL = os.getenv("KAKAO_API_URL")
KAKAO_COORD_URL = os.getenv("KAKAO_COORD_URL")
WEATHER_URL = os.getenv("WEATHER_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_MODEL = os.getenv("GEMINI_API_MODEL")
ALLOWED_HOST = os.getenv("ALLOWED_HOST")