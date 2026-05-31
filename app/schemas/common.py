from typing import Any, Optional
from pydantic import BaseModel, Field

class MetaData(BaseModel):
    computation_time_ms: Optional[float] = Field(None, description="Temps de calcul de l'algorithme en millisecondes")
    model_version: str = Field("1.0.0", description="Version du modèle IA utilisé")

class SuccessResponse(BaseModel):
    success: bool = Field(True, description="Indique si la requête a réussi")
    data: Any = Field(..., description="Le contenu de la réponse (payload)")
    meta: MetaData = Field(default_factory=MetaData, description="Métadonnées de la réponse")

class ErrorDetails(BaseModel):
    code: str = Field(..., description="Code d'erreur standardisé (ex: INVALID_INPUT)")
    message: str = Field(..., description="Message d'erreur lisible")
    details: Optional[Any] = Field(None, description="Détails techniques de l'erreur")

class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Indique l'échec de la requête")
    error: ErrorDetails = Field(..., description="Détails sur l'erreur survenue")
    meta: MetaData = Field(default_factory=MetaData, description="Métadonnées de l'erreur")