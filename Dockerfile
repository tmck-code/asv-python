FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY asv /app/asv
COPY LICENSE README.md pyproject.toml uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# -----------------------------------------------
FROM builder AS builder-dev

# Include development dependencies
ENV UV_NO_DEV=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --group dev --group test

RUN uv pip install .

# -----------------------------------------------
FROM python:3.14-alpine AS dev

ARG UID
ARG GID

RUN addgroup -S -g $GID nonroot \
 && adduser -S -G nonroot -u $UID nonroot
COPY --from=builder-dev --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"
USER nonroot
WORKDIR /app
