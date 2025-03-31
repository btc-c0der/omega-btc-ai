# ✨ GBU License Notice - Consciousness Level 8 💫
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

# Build-time ARG to specify service type
ARG SERVICE_TYPE=consciousness

# Build stage image
FROM python:3.9-slim AS builder

# Builder args
ARG SERVICE_TYPE
ENV SERVICE_TYPE=${SERVICE_TYPE}

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create Python virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies based on service type
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Final slim image
FROM python:3.9-slim

# Runtime args
ARG SERVICE_TYPE
ENV SERVICE_TYPE=${SERVICE_TYPE}
ENV PYTHONUNBUFFERED=1

# Add non-root user for enhanced security
RUN groupadd -g 1000 matrix && \
    useradd -m -u 1000 -g matrix matrix

# Set working directory
WORKDIR /app

# Copy Python virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code based on SERVICE_TYPE
COPY src/ /app/src/
COPY temporal/ /app/temporal/

# Create data directories with proper permissions
RUN mkdir -p /app/data && \
    chown -R matrix:matrix /app

# Switch to non-root user
USER matrix

# Expose default port (will be overridden by environment variable)
EXPOSE 8080

# Healthcheck command based on SERVICE_TYPE
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD if [ "$SERVICE_TYPE" = "websocket" ]; then \
    wget -q --spider http://localhost:${PORT:-8095}/health || exit 1; \
    else \
    wget -q --spider http://localhost:${PORT:-8090}/health || exit 1; \
    fi

# Set the entry point based on SERVICE_TYPE
CMD if [ "$SERVICE_TYPE" = "websocket" ]; then \
    python -m uvicorn temporal.websocket_sacred_echo:app --host 0.0.0.0 --port ${PORT:-10095}; \
    else \
    python -m uvicorn src.matrix_news_consciousness:app --host 0.0.0.0 --port ${PORT:-10090}; \
    fi 