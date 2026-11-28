"""Service Lichess : coups théoriques d'une position (base des parties de maîtres).

Entrée : un chess.Board déjà validé par validate_fen (sous-étape 2.1).
Sortie : TheoreticalMovesResult ; une liste de coups vide n'est pas une erreur.
Erreur : LichessUnavailableError (timeout, réseau, statut non 2xx, JSON inattendu),
         traduite en 503 par app/exceptions.py.

Repris et adapté du Projet 12 (extract_newsdata.fetch_page) :
requests -> httpx, timeout 30 s -> 5 s, return None -> exception dédiée.
"""

import logging

import chess
import httpx

from app.config import LICHESS_EXPLORER_URL, LICHESS_TIMEOUT_S, LICHESS_TOKEN
from app.schemas import Opening, TheoreticalMove, TheoreticalMovesResult

logger = logging.getLogger(__name__)


class LichessUnavailableError(Exception):
    """Lichess n'a pas fourni de réponse exploitable."""


def _percentages(white: int, draws: int, black: int) -> tuple[int, float, float, float]:
    """Nombre de parties et pourcentages blancs / nulles / noirs (1 décimale)."""
    games = white + draws + black
    if games == 0:
        return 0, 0.0, 0.0, 0.0
    return (
        games,
        round(100 * white / games, 1),
        round(100 * draws / games, 1),
        round(100 * black / games, 1),
    )


def _parse_opening(data: dict | None) -> Opening | None:
    if not data:
        return None
    return Opening(eco=data["eco"], name=data["name"])


def _fetch(board: chess.Board, client: httpx.Client) -> dict:
    """Appelle l'explorateur et renvoie le JSON, ou lève LichessUnavailableError."""
    try:
        response = client.get(LICHESS_EXPLORER_URL, params={"fen": board.fen()})
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException as error:
        logger.error("Lichess : délai dépassé (%s s)", LICHESS_TIMEOUT_S)
        raise LichessUnavailableError("Lichess ne répond pas (délai dépassé)") from error
    except httpx.HTTPStatusError as error:
        status = error.response.status_code
        logger.error("Lichess : statut HTTP %d", status)
        raise LichessUnavailableError(f"Lichess a répondu avec le statut {status}") from error
    except httpx.HTTPError as error:
        logger.error("Lichess : erreur réseau : %s", error)
        raise LichessUnavailableError("Lichess est injoignable") from error
    except ValueError as error:  # corps non JSON
        logger.error("Lichess : réponse non JSON")
        raise LichessUnavailableError("Réponse de Lichess illisible") from error


def get_theoretical_moves(
    board: chess.Board, client: httpx.Client | None = None
) -> TheoreticalMovesResult:
    """Coups théoriques de la position, avec statistiques et ouverture.

    `client` permet aux tests d'injecter un faux transport (aucun appel réseau).
    """
    if client is None:
         # Sans jeton, pas d'en-tête (une valeur "Bearer " vide est refusée par HTTP)
        headers = {"Authorization": f"Bearer {LICHESS_TOKEN}"} if LICHESS_TOKEN else {}
        with httpx.Client(timeout=LICHESS_TIMEOUT_S, headers=headers) as own_client:
            data = _fetch(board, own_client)
    else:
        data = _fetch(board, client)

    try:
        moves = []
        for item in data["moves"]:
            # Contrôle 3 : ne garder que les coups légaux dans cette position
            if chess.Move.from_uci(item["uci"]) not in board.legal_moves:
                logger.warning("Lichess : coup illégal ignoré %s", item["uci"])
                continue
            games, white_pct, draws_pct, black_pct = _percentages(
                item["white"], item["draws"], item["black"]
            )
            moves.append(
                TheoreticalMove(
                    uci=item["uci"],
                    san=item["san"],
                    average_rating=item["averageRating"],
                    games=games,
                    white_pct=white_pct,
                    draws_pct=draws_pct,
                    black_pct=black_pct,
                    opening=_parse_opening(item.get("opening")),
                )
            )
        games, white_pct, draws_pct, black_pct = _percentages(
            data["white"], data["draws"], data["black"]
        )
        return TheoreticalMovesResult(
            fen=board.fen(),
            games=games,
            white_pct=white_pct,
            draws_pct=draws_pct,
            black_pct=black_pct,
            opening=_parse_opening(data.get("opening")),
            moves=moves,
        )
    except (KeyError, TypeError, ValueError) as error:
        logger.error("Lichess : structure de réponse inattendue : %s", error)
        raise LichessUnavailableError("Réponse de Lichess inattendue") from error