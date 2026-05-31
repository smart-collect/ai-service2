import time
from fastapi import APIRouter
from app.schemas.common import SuccessResponse, MetaData
from app.core.config import settings

router = APIRouter()
START_TIME = time.time()

@router.get("/health", response_model=SuccessResponse)
async def get_health() -> dict:
    """Retourne l'état opérationnel du service et son uptime."""
    uptime = round(time.time() - START_TIME, 2)
    return {
        "success": True,
        "data": {
            "status": "ok",
            "version": settings.APP_VERSION,
            "uptime_seconds": uptime
        },
        "meta": MetaData(computation_time_ms=0.0, model_version=settings.APP_VERSION)
    }

@router.get("/version", response_model=SuccessResponse)
async def get_version() -> dict:
    """Retourne les détails de version et l'environnement d'exécution."""
    return {
        "success": True,
        "data": {
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV
        },
        "meta": MetaData(computation_time_ms=0.0, model_version=settings.APP_VERSION)
    }