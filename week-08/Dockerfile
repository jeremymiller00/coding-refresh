# Minimal container for the capstone service. A concrete starting point for "ship it".
# Build:  docker build -f week-08/Dockerfile -t capstone .
# Run:    docker run -p 8000:8000 --env-file .env capstone
FROM python:3.12-slim

# uv for fast, reproducible installs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# App code + shared capstone modules
COPY src/ ./src/
COPY week-08/ ./week-08/

EXPOSE 8000
# Secrets (ANTHROPIC_API_KEY) come from the runtime env, never baked into the image.
CMD ["uv", "run", "uvicorn", "week-08.app:app", "--host", "0.0.0.0", "--port", "8000"]
