# syntax=docker/dockerfile:1.7

# ============================================================
# Stage 1 : builder — installe les dépendances dans un venv
# ============================================================
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dépendances d'abord (couche mise en cache tant que pyproject/uv.lock ne changent pas)
COPY pyproject.toml uv.lock ./

# Versions exactes du uv.lock (--frozen), sans pytest/ruff (--no-dev)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project


# ============================================================
# Stage 2 : runtime — image finale légère (sans uv)
# ============================================================
FROM python:3.13-slim-bookworm AS runtime

# curl uniquement pour le HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Utilisateur non-root (sécurité)
RUN useradd --create-home --uid 1000 --shell /bin/bash appuser

WORKDIR /app

# Venv depuis le builder, code depuis le contexte de build
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --chown=appuser:appuser app/ ./app/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000

# Docker appelle la route toutes les 10 s ; 3 échecs de suite → unhealthy
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/healthcheck || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]