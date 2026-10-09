FROM ghcr.io/astral-sh/uv:0.13.0 AS uv
FROM python:3.13-slim
WORKDIR /app
ENV PYTHONPATH=/app
COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

