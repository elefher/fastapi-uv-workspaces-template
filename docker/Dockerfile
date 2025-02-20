ARG BASE_IMAGE=python:3.13-slim

FROM ${BASE_IMAGE} AS base

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy files from project root
COPY pyproject.toml uv.lock /app/
COPY app /app/app
COPY packages /app/packages

WORKDIR /app

RUN uv sync --frozen --no-cache

FROM base AS development

CMD ["uv", "run", "uvicorn", "app.main:app_", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS production

CMD ["uv", "run", "uvicorn", "app.main:app_", "--host", "0.0.0.0", "--port", "8000"] 