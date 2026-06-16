"""KBO data ingestion API endpoints.

Development-only endpoints for triggering kbo-data scraping.
KBO_DATA_ENABLED must be true to run real scraping.
Default (KBO_DATA_ENABLED=false) returns disabled status.
"""

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.schemas.ingestion import KboGameDataRequest, KboIngestionResult, KboScheduleRequest

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.get("/status")
def ingestion_status():
    return {
        "kbo_data_enabled": settings.KBO_DATA_ENABLED,
        "kbo_ingestion_mode": settings.KBO_INGESTION_MODE,
        "mock_mode": settings.MOCK_MODE,
        "chromedriver_configured": bool(settings.KBO_CHROMEDRIVER_PATH),
        "raw_payload_dir": settings.KBO_RAW_PAYLOAD_DIR,
        "note": (
            "KBO ingestion is disabled. Set KBO_DATA_ENABLED=true and "
            "KBO_INGESTION_MODE=kbo-data in .env to enable."
            if not settings.KBO_DATA_ENABLED
            else "KBO ingestion is enabled."
        ),
    }


@router.post("/kbo-data/schedule", response_model=KboIngestionResult)
def ingest_kbo_schedule(request: KboScheduleRequest):
    if not settings.KBO_DATA_ENABLED:
        raise HTTPException(
            status_code=403,
            detail=(
                "KBO_DATA_ENABLED is false. "
                "Set KBO_DATA_ENABLED=true and KBO_INGESTION_MODE=kbo-data to enable."
            ),
        )
    if settings.KBO_INGESTION_MODE != "kbo-data":
        raise HTTPException(
            status_code=403,
            detail=f"KBO_INGESTION_MODE={settings.KBO_INGESTION_MODE!r}. Set to 'kbo-data' to enable.",
        )

    from app.ingestion.kbo_data_adapter import kbo_data_adapter
    return kbo_data_adapter.fetch_schedule(request)


@router.post("/kbo-data/game-data", response_model=KboIngestionResult)
def ingest_kbo_game_data(request: KboGameDataRequest):
    if not settings.KBO_DATA_ENABLED:
        raise HTTPException(
            status_code=403,
            detail="KBO_DATA_ENABLED is false.",
        )
    if settings.KBO_INGESTION_MODE != "kbo-data":
        raise HTTPException(
            status_code=403,
            detail=f"KBO_INGESTION_MODE={settings.KBO_INGESTION_MODE!r}. Set to 'kbo-data' to enable.",
        )

    from app.ingestion.kbo_data_adapter import kbo_data_adapter
    return kbo_data_adapter.fetch_game_data(request)
