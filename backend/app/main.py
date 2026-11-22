"""Point d'entrée de l'API FastAPI.

Crée l'application et expose les routes.
Étape 1 : seulement la route de santé (healthcheck).
"""

from fastapi import APIRouter, FastAPI

from app.config import API_DESCRIPTION, API_PREFIX, API_TITLE, API_VERSION
from app.schemas import HealthResponse

# --- Application -----------------------------------------------------------

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

# --- Routes versionnées (/api/v1/...) --------------------------------------

router = APIRouter(prefix=API_PREFIX)


@router.get(
    "/healthcheck",
    response_model=HealthResponse,
    summary="Vérifie que l'API est en vie",
    tags=["monitoring"],
)
def healthcheck() -> HealthResponse:
    """Signe de vie de l'API, appelé par le HEALTHCHECK Docker."""
    return HealthResponse(status="ok", api_version=API_VERSION)


app.include_router(router)


# --- Accueil ---------------------------------------------------------------


@app.get("/", include_in_schema=False)
def root() -> dict:
    """Page d'accueil minimaliste : indique où trouver la doc et le healthcheck."""
    return {
        "service": API_TITLE,
        "version": API_VERSION,
        "docs": "/docs",
        "health": f"{API_PREFIX}/healthcheck",
    }