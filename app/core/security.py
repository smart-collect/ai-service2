from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

# Définition du nom du Header attendu
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Dépendance FastAPI pour valider la clé API présente dans les requêtes.
    Renvoie une erreur 403 si la clé est absente ou invalide.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clé API manquante dans le header X-API-Key",
        )
    if api_key != settings.AI_SERVICE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clé API non valide ou expirée",
        )
    return api_key