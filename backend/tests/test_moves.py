"""Tests de la route GET /api/v1/moves/{fen} (sous-étape 2.4), sans réseau.

monkeypatch remplace le documentaliste Lichess par un acteur pendant le test.
"""

import pytest
from fastapi.testclient import TestClient

import app.main
from app.schemas import TheoreticalMovesResult
from app.services.lichess import LichessUnavailableError

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


@pytest.fixture
def client() -> TestClient:
    return TestClient(app.main.app)


def test_valid_fen_returns_200_and_full_fen(client, monkeypatch) -> None:
    def fake_lichess(board):
        return TheoreticalMovesResult(
            fen=board.fen(), games=0, white_pct=0.0, draws_pct=0.0,
            black_pct=0.0, opening=None, moves=[],
        )

    monkeypatch.setattr(app.main, "get_theoretical_moves", fake_lichess)

    response = client.get(f"/api/v1/moves/{START_FEN}")

    assert response.status_code == 200
    assert response.json()["fen"] == START_FEN  # FEN arrivée entière, / et espaces compris


def test_invalid_fen_returns_422_without_calling_lichess(client, monkeypatch) -> None:
    calls = []
    monkeypatch.setattr(app.main, "get_theoretical_moves", lambda board: calls.append(board))

    response = client.get("/api/v1/moves/8/8/8/8/8/8/8/8 w - - 0 1")

    assert response.status_code == 422
    assert calls == []  # le documentaliste n'a pas été appelé


def test_lichess_down_returns_503(client, monkeypatch) -> None:
    def lichess_down(board):
        raise LichessUnavailableError("Lichess ne répond pas (délai dépassé)")

    monkeypatch.setattr(app.main, "get_theoretical_moves", lichess_down)

    response = client.get(f"/api/v1/moves/{START_FEN}")

    assert response.status_code == 503