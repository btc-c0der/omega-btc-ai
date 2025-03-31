# 🧱 Stage 1: Builder - "The Sacred Forge"
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /build

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# 🔒 Stage 2: Runtime - "The Incorruptible Vessel"
FROM python:3.11-slim

# Add container metadata
LABEL maintainer="OMEGA BTC AI <divine@omega-btc-ai.com>"
LABEL version="1.0.0"
LABEL description="Matrix News Consciousness Service"
LABEL consciousness_level="8"
LABEL anti_debt_protected="true"

# Create non-root user
RUN groupadd -r omega && useradd -r -g omega omega

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create directory structure
WORKDIR /app
RUN mkdir -p /app/data /app/log /app/src /app/articles && \
    chown -R omega:omega /app && \
    chmod -R 755 /app

# Copy only necessary files from builder
COPY --from=builder --chown=omega:omega /build/src /app/src
COPY --from=builder --chown=omega:omega /build/requirements.txt /app/
COPY --from=builder --chown=omega:omega /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Environment variables
ENV PYTHONPATH=/app \
    PORT=8090 \
    PYTHONUNBUFFERED=1 \
    CONSCIOUSNESS_LEVELS_ENABLED=true \
    CONSCIOUSNESS_DEFAULT_LEVEL=5

# Expose port
EXPOSE 8090

# Set up health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8090/health || exit 1

# Run as non-root user
USER omega

# Set the entrypoint
ENTRYPOINT ["python3", "/app/src/app.py"] 