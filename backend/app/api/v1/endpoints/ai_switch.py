# Placeholder for AI service switch endpoint
from fastapi import APIRouter

router = APIRouter()

@router.get("/ai-service")
async def get_ai_service():
    return {"ai_service": "hybrid"}
