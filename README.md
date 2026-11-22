# Projet 13 — Agent IA d'aide à l'apprentissage des échecs

POC d'un agent IA qui accompagne un joueur d'échecs dans l'apprentissage des ouvertures
et l'analyse de positions (formation OpenClassrooms AI Engineer).

## 🎯 Objectif

À partir d'une position (notation FEN), l'agent :
- identifie l'ouverture et les coups théoriques (Lichess) ;
- évalue les coups ou analyse la position hors théorie (Stockfish) ;
- enrichit l'explication avec une base documentaire (RAG Wikichess + Milvus) ;
- propose des vidéos pédagogiques (API YouTube) ;
- synthétise une réponse structurée avec un LLM, sans inventer de coups.

## 🏗️ Architecture cible

| Composant | Rôle |
|---|---|
| FastAPI | API backend exposant l'agent |
| LangGraph | Orchestration des outils de l'agent |
| Lichess / Stockfish | Théorie d'ouverture / évaluation des positions |
| Milvus | Base vectorielle du RAG |
| MongoDB | Cache ou historique des analyses (rôle à préciser) |
| Angular | Interface utilisateur (échiquier + recommandations) |
| Docker Compose | Orchestration des services |

## 📁 Structure du projet

```
projet_13_agent_ia/
├── backend/            # API FastAPI (projet uv, Python 3.13)
│   ├── app/
│   └── tests/
├── frontend/           # Interface Angular (étape 5)
├── docker-compose.yml  # Orchestration des services 
├── .env.example        # Modèle des variables d'environnement
└── README.md
```

## 🚀 Démarrage rapide

### Prérequis

- Git
- Docker Desktop (Docker Compose v2)
- [uv](https://docs.astral.sh/uv/) (gestionnaire Python)

### Installation

```bash
git clone <url-du-depot>
cd projet_13_agent_ia
```

### Configuration

```bash
cp .env.example .env
```

| Variable | Rôle | Défaut |
|---|---|---|
| `API_PORT` | Port de la machine hôte pour accéder à l'API | `8000` |

### Environnement de développement (backend)

```bash
cd backend
uv sync --all-groups
```

### Lancement

### Lancement (Docker Compose)

Depuis la racine du projet :

```bash
docker compose up -d --build
docker compose ps        # attendre le statut (healthy)
```

| URL | Contenu |
|---|---|
| http://localhost:8000/api/v1/healthcheck | Signe de vie de l'API |
| http://localhost:8000/docs | Documentation interactive (Swagger) |

Le port `8000` correspond à `API_PORT` dans `.env`.

### Arrêt

```bash
docker compose down
```

## 📌 Avancement

| Étape | Sujet | État |
|---|---|---|
| 1 | Environnement de travail | 🔄 En cours |
| 2 | Agent LangGraph | ⏳ |
| 3 | RAG Milvus | ⏳ |
| 4 | API YouTube | ⏳ |
| 5 | Interface Angular | ⏳ |
| 6 | Packaging | ⏳ |
| 7 | Étude de faisabilité analyse vidéo | ⏳ |