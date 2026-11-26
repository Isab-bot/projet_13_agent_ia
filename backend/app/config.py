"""Configuration centralisée de l'API.

Les constantes sont regroupées ici pour éviter les valeurs dispersées
dans le code.
"""

API_TITLE = "Chess Agent API"
API_DESCRIPTION = (
    "API de l'agent IA d'aide à l'apprentissage des ouvertures d'échecs "
    "(Projet 13 - OpenClassrooms AI Engineer)."
)
API_VERSION = "0.1.0"

# Préfixe commun à toutes les routes : permet de versionner l'API
API_PREFIX = "/api/v1"