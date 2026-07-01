# fastapi start

<br/>

🤖 fastAPI 학습을 위한 좌표 기반 현재 날씨 조회 및 AI 날씨 요약 서버입니다.


<br/>
<br/>

## 🚀 run

<br/>

### 1. 패키지 설치
```
pip install -r requirements.txt
```

<br/>
<br/>

### 2. 환경 변수 설정
`env/.env` 파일을 생성한 후 아래 내용을 추가합니다.
```
# Kakao API
KAKAO_API_KEY="{kakao api key}"
KAKAO_API_URL="https://dapi.kakao.com/v2/local/search/address.json?query="
KAKAO_COORD_URL="https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"

# Weather API
WEATHER_URL="https://api.open-meteo.com/v1/forecast"

# Gemini AI
GEMINI_API_MODEL="{gemini model}"
GEMINI_API_KEY="{gemini key}"

# Allowed frontend origin
ALLOWED_HOST="localhost"
```
<br/>
<br/>

### 3. 실행
```
uvicorn main:app --reload
```
