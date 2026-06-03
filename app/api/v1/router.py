from fastapi import APIRouter
from app.api.v1.endpoints import optimization

api_router = APIRouter()

# Branchement officiel de la route de Borja conforme aux consignes
api_router.include_router(optimization.router, prefix="/optimization", tags=["optimization"])
