FROM python:3.14.2-alpine3.23
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY app/ /app/

CMD ["/bin/sh", "-c", "uv run alembic upgrade head && uv run main.py"]