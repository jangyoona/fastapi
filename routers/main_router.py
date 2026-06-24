from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def main():
    return "오늘의 날씨가 궁금하신가요?"