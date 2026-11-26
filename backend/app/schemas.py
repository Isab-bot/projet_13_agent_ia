"""Schémas Pydantic : forme des données échangées par l'API."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Réponse de la route /api/v1/healthcheck."""

    status: str
    api_version: str

   

# --- Lichess (sous-étape 2.3) ----------------------------------------------


class Opening(BaseModel):
    """Ouverture identifiée par Lichess."""

    eco: str  # code ECO, ex. "B00"
    name: str  # ex. "King's Pawn Game"


class TheoreticalMove(BaseModel):
    """Un coup théorique et ses statistiques en parties de maîtres."""

    uci: str  # ex. "e2e4"
    san: str  # ex. "e4"
    average_rating: int  # Elo moyen des joueurs ayant joué ce coup
    games: int  # nombre de parties : indique le poids des pourcentages
    white_pct: float
    draws_pct: float
    black_pct: float
    opening: Opening | None  # ouverture après ce coup


class TheoreticalMovesResult(BaseModel):
    """Réponse du service Lichess pour une position."""

    fen: str
    games: int
    white_pct: float
    draws_pct: float
    black_pct: float
    opening: Opening | None  # None si la position n'a pas de nom (ex. départ)
    moves: list[TheoreticalMove]  # liste vide = aucun coup théorique 