# Stage 1: Build dependencies and install the project
FROM ghcr.io/astral-sh/uv:python3.11-alpine AS builder

# Set working directory and environment variables for build
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Use cache for dependencies to speed up builds
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the full source code
COPY . /app

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Stage 2: Final lightweight image
FROM ghcr.io/astral-sh/uv:python3.11-alpine

# Set working directory
WORKDIR /app

# Copy only necessary artifacts from the builder stage
COPY --from=builder /app /app

# Set environment variables
ENV UV_COMPILE_BYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint
ENTRYPOINT []

# Define the default command
CMD ["python", "bot.py"]
