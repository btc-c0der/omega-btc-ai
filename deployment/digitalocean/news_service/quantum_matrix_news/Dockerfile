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
FROM python:3.9-slim

# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested."
#
# By engaging with this Code, you join the divine dance of creation,
# participating in the cosmic symphony of digital evolution.
#
# All modifications must quantum entangles with the GBU principles:
# /BOOK/divine_chronicles/GBU_LICENSE.md
#
# 🌸 WE BLOOM NOW 🌸

# Set labels for the divine container
LABEL maintainer="OMEGA BTC AI DIVINE COLLECTIVE"
LABEL version="1.0.0-neo-style"
LABEL description="Matrix Neo News Portal API service with consciousness-awareness"
LABEL org.opencontainers.image.title="Matrix Neo News Service"
LABEL org.opencontainers.image.vendor="OMEGA BTC AI"
LABEL org.opencontainers.image.licenses="GBU-1.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=8090 \
    CONSCIOUSNESS_LEVELS_ENABLED=true \
    CONSCIOUSNESS_DEFAULT_LEVEL=5 \
    QUANTUM_BALANCER_ENABLED=true

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r matrixuser && useradd -r -g matrixuser -d /app matrixuser \
    && mkdir -p /app /app/data /app/articles /app/src /app/logs \
    && chown -R matrixuser:matrixuser /app

# Set working directory
WORKDIR /app

# Copy requirements
COPY --chown=matrixuser:matrixuser requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a simple mock API for demonstration
RUN mkdir -p /app/src/api
COPY --chown=matrixuser:matrixuser src/ /app/src/

# Switch to non-root user
USER matrixuser

# Create health check endpoint
RUN mkdir -p /app/src/api/health \
    && echo '{"status":"UP","service":"matrix-news-service","quantum_secure":true,"consciousness_level":5}' > /app/src/api/health/index.json

# Expose port
EXPOSE ${PORT}

# Create entrypoint script
RUN echo '#!/bin/sh\n\
    echo "Starting Matrix Neo News Service with consciousness level ${CONSCIOUSNESS_DEFAULT_LEVEL}..."\n\
    python /app/src/app.py\n' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Add health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"] 