from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.logging import LoggingMiddleware

# Initialisation de l'application FastAPI pour Smart-Collect Hysacam
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Micro-service d'algorithmes intelligents pour Smart-Collect Hysacam",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuration CORS pour communiquer avec le backend Node.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des middlewares de gestion d'erreurs et de logs
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)

# Inclusion du routeur principal v1
app.include_router(api_router)

@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {"message": f"Welcome to {settings.APP_NAME} API. Go to /docs for Swagger UI."}