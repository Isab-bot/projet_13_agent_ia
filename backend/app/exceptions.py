"""Traduction des exceptions métier en réponses HTTP.

Les services (app/services/) lèvent des exceptions métier sans connaître HTTP ;
les handlers ci-dessous les transforment en code HTTP + JSON {"detail": ...}.
Ils sont enregistrés dans app/main.py via register_exception_handlers(app).

Repris du Projet 8 (api/exceptions.py) :
- generic_exception_handler : gardé (500 sans trace d'erreur côté client)
- model_not_loaded_handler  : adapté en invalid_fen_handler (même principe, code 422)
  et en lichess_unavailable_handler (code 503 conservé)
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.services.fen_validator import InvalidFENError
from app.services.lichess import LichessUnavailableError

logger = logging.getLogger(__name__)


async def invalid_fen_handler(request: Request, exc: InvalidFENError) -> JSONResponse:
    """FEN envoyée par le client inutilisable -> 422."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": str(exc)},
    )


async def lichess_unavailable_handler(
    request: Request, exc: LichessUnavailableError
) -> JSONResponse:
    """Service externe Lichess indisponible -> 503."""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": str(exc)},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Filet de sécurité : toute exception non prévue -> 500.

    Le détail technique reste dans les logs serveur, pas dans la réponse.
    """
    logger.exception("Erreur non prévue sur %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Erreur interne du serveur : {type(exc).__name__}"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Enregistre les handlers sur l'application FastAPI."""
    app.add_exception_handler(InvalidFENError, invalid_fen_handler)
    app.add_exception_handler(LichessUnavailableError, lichess_unavailable_handler)
    app.add_exception_handler(Exception, generic_exception_handler)