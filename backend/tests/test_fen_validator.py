"""Tests du module de validation FEN (sous-étape 2.1)."""

import chess
import pytest

from app.services.fen_validator import InvalidFENError, validate_fen

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_valid_fen_returns_board():
    board = validate_fen(START_FEN)
    assert isinstance(board, chess.Board)
    assert board.fen() == START_FEN


def test_malformed_fen_raises():
    with pytest.raises(InvalidFENError, match="mal écrite"):
        validate_fen("nimporte quoi")


def test_impossible_position_raises():
    with pytest.raises(InvalidFENError, match="Position impossible") as exc_info:
        validate_fen("8/8/8/8/8/8/8/8 w - - 0 1")
    assert "NO_WHITE_KING" in str(exc_info.value)