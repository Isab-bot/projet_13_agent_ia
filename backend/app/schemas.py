"""Schémas Pydantic : forme des données échangées par l'API."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Réponse de la route /api/v1/healthcheck."""

    status: str
    api_version: str