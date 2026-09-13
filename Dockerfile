# ==============================================================================
# Stage 1: Builder
# Handles system dependencies, Poetry installation, and dependency compilation.
# ==============================================================================
FROM python:3.14-slim AS builder

LABEL stage="builder"

WORKDIR /app

# Optimize Python runtime behavior and lock Poetry to non-interactive mode.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install system dependencies required for building native Python packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install the latest stable version of Poetry via pip for modern lockfile compatibility.
RUN pip install --no-cache-dir --upgrade poetry

# Copy dependency manifests first to leverage Docker layer caching.
COPY pyproject.toml poetry.lock ./

# Install production dependencies only, skipping development tools and root package.
RUN poetry install --without dev --no-root


# ==============================================================================
# Stage 2: Runner
# Lightweight, secure production image containing only the app and dependencies.
# ==============================================================================
FROM python:3.14-slim AS runner

LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="Python FastAPI application using Poetry"

WORKDIR /app

# Create a non-privileged system user and group for enhanced container security.
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Configure runtime environment variables and prepend virtualenv bin to PATH.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy the pre-built virtual environment from the builder stage with proper ownership.
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy the application source code with proper ownership.
COPY --chown=appuser:appuser . /app

# Drop root privileges and switch to the non-privileged user.
USER appuser

# Expose the port the application listens on.
EXPOSE 8000

# Verify that the FastAPI application is responding over HTTP.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/docs', timeout=3)" || exit 1

# Run the FastAPI application using Uvicorn.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]