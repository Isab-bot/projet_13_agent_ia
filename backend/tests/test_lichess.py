"""Tests du service Lichess (sous-étape 2.3), sans réseau.

httpx.MockTransport remplace Lichess : chaque test choisit la réponse simulée.
"""

import chess
import httpx
import pytest

from app.services.lichess import LichessUnavailableError, get_theoretical_moves

# Extrait d'une vraie réponse de /masters pour la position de départ (26/11/2026)
START_RESPONSE = {
    "white": 958331,
    "draws": 1346565,
    "black": 692516,
    "moves": [
        {
            "uci": "e2e4",
            "san": "e4",
            "averageRating": 2390,
            "white": 431551,
            "draws": 610338,
            "black": 326236,
            "game": None,
            "opening": {"eco": "B00", "name": "King's Pawn Game"},
        },
        {
            "uci": "d2d3",
            "san": "d3",
            "averageRating": 2329,
            "white": 272,
            "draws": 269,
            "black": 288,
            "game": None,
            "opening": {"eco": "A00", "name": "Mieses Opening"},
        },
    ],
    "topGames": [],
    "opening": None,
}


def make_client(handler) -> httpx.Client:
    """Client httpx dont les requêtes sont traitées par `handler`, sans réseau."""
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_known_position_returns_structured_moves() -> None:
    client = make_client(lambda request: httpx.Response(200, json=START_RESPONSE))

    result = get_theoretical_moves(chess.Board(), client=client)

    assert result.opening is None  # position de départ : pas encore d'ouverture
    assert [move.san for move in result.moves] == ["e4", "d3"]
    e4 = result.moves[0]
    assert e4.games == 1368125
    assert (e4.white_pct, e4.draws_pct, e4.black_pct) == (31.5, 44.6, 23.8)
    assert e4.opening.name == "King's Pawn Game"


def test_unknown_position_returns_empty_list() -> None:
    empty = {"white": 0, "draws": 0, "black": 0, "moves": [], "topGames": [], "opening": None}
    client = make_client(lambda request: httpx.Response(200, json=empty))

    result = get_theoretical_moves(chess.Board(), client=client)

    assert result.moves == []
    assert result.games == 0


def test_timeout_raises_lichess_unavailable() -> None:
    def timeout(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("délai dépassé", request=request)

    with pytest.raises(LichessUnavailableError, match="délai"):
        get_theoretical_moves(chess.Board(), client=make_client(timeout))


def test_illegal_move_from_lichess_is_ignored() -> None:
    bad = dict(START_RESPONSE, moves=[dict(START_RESPONSE["moves"][0], uci="e7e5", san="e5")])
    client = make_client(lambda request: httpx.Response(200, json=bad))

    result = get_theoretical_moves(chess.Board(), client=client)

    assert result.moves == []  # e7e5 est illégal au trait des blancs