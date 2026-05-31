from fastapi import APIRouter
from app.api.v1.endpoints import health

api_router = APIRouter(prefix="/api/v1")

# Inclusion du routeur dédié à l'état de santé du service
api_router.include_router(health.router, tags=["System / Health"])