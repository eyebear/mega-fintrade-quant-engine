# Phase 10.1 — Dockerfile
# Mega Fintrade Quant Engine
#
# This Dockerfile builds the Python quantitative analytics engine
# in a repeatable Linux container.
#
# It supports:
# - installing dependencies from requirements.txt
# - running pytest
# - running the analytics pipeline with python -m src.run_pipeline
#
# Default command:
#   python -m src.run_pipeline

FROM python:3.12-slim

LABEL org.opencontainers.image.title="Mega Fintrade Quant Engine"
LABEL org.opencontainers.image.description="Python quantitative backtesting and analytics engine for the Mega Fintrade Platform."
LABEL org.opencontainers.image.authors="Ao Ao Feng"
LABEL org.opencontainers.image.source="https://github.com/eyebear/mega-fintrade-quant-engine"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src ./src
COPY tests ./tests
COPY data ./data
COPY docs ./docs
COPY reports ./reports

RUN mkdir -p /app/data/raw /app/data/processed /app/data/output /app/reports

CMD ["python", "-m", "src.run_pipeline"]