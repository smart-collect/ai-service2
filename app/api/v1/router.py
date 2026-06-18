from fastapi import APIRouter
from app.api.v1.endpoints import health, optimization

api_router = APIRouter()

# Branchement des routes API v1
api_router.include_router(health.router, tags=["health"])
api_router.include_router(optimization.router, prefix="/optimization", tags=["optimization"])
