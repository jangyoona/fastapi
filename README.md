# fastapi start

<br/>
<br/>

## 🚀 run

<br/>

1. 패키지 설치
```
pip install -r requirements.txt
```

<br/>
<br/>

2. env/.env 파일 추가
```
KAKAO_API_KEY="{kakao api key}"
KAKAO_API_URL="https://dapi.kakao.com/v2/local/search/address.json?query="
KAKAO_COORD_URL="https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
WEATHER_URL="https://api.open-meteo.com/v1/forecast"

GEMINI_API_MODEL="{gemini model}"
GEMINI_API_KEY="{gemini key}"

ALLOWED_HOST="localhost"
```
<br/>
<br/>

3. 실행
```
uvicorn main:app --reload
```
