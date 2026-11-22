"""Tests de la route GET /api/v1/healthcheck."""

import pytest
from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Client de test : simule des requêtes HTTP sans lancer de serveur."""
    return TestClient(app)


class TestHealthcheck:
    """Healthcheck : l'API répond et indique sa version."""

    def test_returns_200(self, client: TestClient) -> None:
        """La route répond avec le code HTTP 200 (OK)."""
        response = client.get("/api/v1/healthcheck")
        assert response.status_code == 200

    def test_status_is_ok(self, client: TestClient) -> None:
        """Le champ status vaut 'ok'."""
        response = client.get("/api/v1/healthcheck")
        assert response.json()["status"] == "ok"

    def test_returns_api_version(self, client: TestClient) -> None:
        """Le champ api_version correspond à la version définie dans config.py."""
        response = client.get("/api/v1/healthcheck")
        assert response.json()["api_version"] == API_VERSION