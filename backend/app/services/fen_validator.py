"""Validation centralisée des positions FEN.

Deux contrôles successifs (voir synthèse de l'étape 1) :
1. la FEN est-elle bien écrite ?   -> chess.Board(fen) lève ValueError sinon
2. la position est-elle possible ? -> board.is_valid(), board.status() dit pourquoi

La légalité d'un coup (3e contrôle) n'est pas traitée ici : elle sera vérifiée
dans les services Lichess et Stockfish à partir du Board renvoyé.
"""

import chess


class InvalidFENError(Exception):
    """La chaîne reçue n'est pas une FEN utilisable."""


def validate_fen(fen: str) -> chess.Board:
    """Renvoie le Board correspondant à la FEN, ou lève InvalidFENError."""
    # Contrôle 1 : syntaxe
    try:
        board = chess.Board(fen)
    except ValueError as error:
        raise InvalidFENError(f"FEN mal écrite : {error}") from error

    # Contrôle 2 : position possible
    if not board.is_valid():
        reasons = ", ".join(flag.name for flag in board.status())
        raise InvalidFENError(f"Position impossible : {reasons}")

    return board