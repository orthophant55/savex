from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "0.1.0",
        "app_name": settings.APP_NAME,
        "mock_mode": settings.MOCK_MODE,
    }
