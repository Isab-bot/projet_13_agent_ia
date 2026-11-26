"""Configuration centralisée de l'API.

Les constantes sont regroupées ici pour éviter les valeurs dispersées
dans le code.
"""

import os

API_TITLE = "Chess Agent API"
API_DESCRIPTION = (
    "API de l'agent IA d'aide à l'apprentissage des ouvertures d'échecs "
    "(Projet 13 - OpenClassrooms AI Engineer)."
)
API_VERSION = "0.1.0"

# Préfixe commun à toutes les routes : permet de versionner l'API
API_PREFIX = "/api/v1"


# --- Lichess (explorateur d'ouvertures, base des parties de maîtres) -------

LICHESS_EXPLORER_URL = "https://explorer.lichess.ovh/masters"
# Un utilisateur attend la réponse : on abandonne vite (P12 : 30 s en tâche de fond)
LICHESS_TIMEOUT_S = 5.0
# Jeton personnel exigé par l'explorateur ; valeur réelle dans .env (jamais dans Git)
LICHESS_TOKEN = os.getenv("LICHESS_TOKEN", "")