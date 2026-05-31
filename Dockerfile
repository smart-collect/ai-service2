# Stage 1: Build des dépendances
FROM python:3.11-slim AS builder

WORKDIR /app

# Installation des outils système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installation de Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copie des fichiers de configuration
COPY pyproject.toml poetry.lock* ./

# Génération du requirements.txt via Poetry pour le stage final
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Image finale d'exécution
FROM python:3.11-slim AS runner

WORKDIR /app

# Configuration de l'environnement Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Récupération du requirements.txt du stage builder
COPY --from=builder /app/requirements.txt .

# Installation des dépendances de production uniquement
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copie du code de l'application
COPY app/ ./app/

# Port d'écoute imposé
EXPOSE 8000

# Commande de démarrage du serveur Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]