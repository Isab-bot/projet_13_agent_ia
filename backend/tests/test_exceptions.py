"""Tests des handlers d'exceptions (sous-étape 2.2).

Une mini-application de test permet de vérifier les handlers sans attendre
les vraies routes (2.4 et 2.6).
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.exceptions import register_exception_handlers
from app.services.fen_validator import validate_fen
from app.services.lichess import LichessUnavailableError

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


@pytest.fixture
def client() -> TestClient:
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/check")
    def check(fen: str) -> dict:
        validate_fen(fen)
        return {"status": "ok"}

    @test_app.get("/lichess-down")
    def lichess_down() -> dict:
        raise LichessUnavailableError("Lichess ne répond pas (délai dépassé)")

    @test_app.get("/boom")
    def boom() -> dict:
        raise RuntimeError("panne simulée")

    # raise_server_exceptions=False : sinon TestClient relance l'exception
    # au lieu de renvoyer la réponse 500 produite par le handler
    return TestClient(test_app, raise_server_exceptions=False)


def test_valid_fen_returns_200(client: TestClient) -> None:
    response = client.get("/check", params={"fen": START_FEN})
    assert response.status_code == 200


def test_invalid_fen_returns_422_with_reason(client: TestClient) -> None:
    response = client.get("/check", params={"fen": "8/8/8/8/8/8/8/8 w - - 0 1"})
    assert response.status_code == 422
    assert "Position impossible" in response.json()["detail"]


def test_unexpected_error_returns_500_without_trace(client: TestClient) -> None:
    response = client.get("/boom")
    assert response.status_code == 500
    assert response.json()["detail"] == "Erreur interne du serveur : RuntimeError"
    assert "panne simulée" not in response.text


def test_lichess_unavailable_returns_503(client: TestClient) -> None:
    response = client.get("/lichess-down")
    assert response.status_code == 503
    assert "Lichess" in response.json()["detail"]