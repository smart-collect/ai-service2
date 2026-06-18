from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.tour_optimizer import (
    calculer_distance_totale_tournee,
    optimiser_2opt,
    optimiser_plus_proche_voisin,
)


class Bin(BaseModel):
    id: str
    lat: float
    lng: float
    remplissage: float = Field(..., ge=0, le=100)
    adresse: str | None = None


class OptimizationRequest(BaseModel):
    bacs: List[Bin]
    start_lat: float
    start_lng: float
    method: str = Field(default="nearest", pattern="^(nearest|2opt)$")


class OptimizationResponse(BaseModel):
    success: bool = True
    route: List[Bin]
    distance_km: float
    method: str


router = APIRouter()


@router.post("/tour", response_model=OptimizationResponse)
async def optimize_tour(payload: OptimizationRequest) -> OptimizationResponse:
    """Optimise une tournée de collecte de bacs de déchets."""
    bacs = [bac.dict() for bac in payload.bacs]

    if payload.method == "2opt":
        route = optimiser_2opt(
            optimiser_plus_proche_voisin(bacs, payload.start_lat, payload.start_lng),
            payload.start_lat,
            payload.start_lng,
        )
    else:
        route = optimiser_plus_proche_voisin(bacs, payload.start_lat, payload.start_lng)

    distance = calculer_distance_totale_tournee(route, payload.start_lat, payload.start_lng)

    return OptimizationResponse(
        route=route,
        distance_km=round(distance, 3),
        method=payload.method,
    )
