# ───────────── Base: builder ─────────────
FROM python:3.12-slim AS builder

# Prevents Python .pyc files and forces unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Poetry (install to ~/.local/bin)
ENV POETRY_VERSION=2.2.1 \
    POETRY_HOME=/root/.local \
    PATH="/root/.local/bin:${PATH}" \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System deps for building wheels (builder-only),
# kept minimal and removed after layer
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      build-essential \
      git \
      libffi-dev \
      libssl-dev \
      pkg-config \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only lock files first to maximize layer cache
COPY pyproject.toml poetry.lock ./

# Install project dependencies into an isolated venv in /opt/venv
# (No dev deps; no project build yet)
RUN python -m venv /opt/venv && . /opt/venv/bin/activate \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --without dev --no-interaction --no-ansi

# ───────────── Runtime ─────────────
FROM python:3.12-slim AS final

# Same Python env knobs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Put venv first on PATH
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

# Runtime-only OS deps (headless browser / GUI libs + tini)
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      tini \
      curl \
      wget \
      unzip \
      fonts-liberation \
      libnss3 \
      libatk-bridge2.0-0 \
      libgtk-3-0 \
      libxss1 \
      libasound2 \
      libxshmfence1 \
      libx11-xcb1 \
      libgbm1 \
      libxcomposite1 \
      libxdamage1 \
      libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r app && useradd -r -g app -d /app app

WORKDIR /app

# Copy prebuilt venv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy app code (use --link in Docker 25+ to reduce size)
COPY app/ ./app
# If main.py is at /app/main.py instead of /app/app/main.py,
# copy it as well:
# COPY main.py ./

# Adjust ownership
RUN chown -R app:app /app
USER app

# Networking / config
EXPOSE 8000
ENV PROFILE=PROD \
    APP_HOST=0.0.0.0

# Healthcheck (adjust path if your app differs)
# HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD \
#  curl -fsS "http://127.0.0.1:8000/health" || exit 1

WORKDIR /app/app

# Entrypoint + command (exec form)
ENTRYPOINT ["tini", "--"]
# If your entry module is /app/main.py, keep this:
CMD ["python", "main.py"]
# CMD ["ls", "-l", "/app"]
# If it's a package entry point, you might prefer:
# CMD ["python", "-m", "app"]
