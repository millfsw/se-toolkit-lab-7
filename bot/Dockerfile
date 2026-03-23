# Bot Dockerfile - Multi-stage build using uv
# Follows the same pattern as backend/Dockerfile

# ---
# Stage 1: Build the application in the `/app` directory
# ---

ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads, use system interpreter
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy lock file and project metadata first (better layer caching)
COPY uv.lock pyproject.toml ./
COPY bot/pyproject.toml ./bot/

# Sync dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project

# Copy the bot source code
COPY bot ./bot

# ---
# Stage 2: Final runtime image
# ---

ARG REGISTRY_PREFIX=harbor.pg.innopolis.university/docker-hub-cache/
FROM ${REGISTRY_PREFIX}python:3.14.2-slim-bookworm

# Environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Create non-root user for security
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the application from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Use non-root user
USER nonroot

# Working directory
WORKDIR /app

# Run the bot
CMD ["python", "bot/bot.py"]
