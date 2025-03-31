# 🔱 OMEGA BTC AI - DIVINE BTC LIVE FEED V3 🔱
# Multi-stage build with Anti-Debt Tech patterns

# 🧱 Stage 1: Builder - "The Sacred Forge"
FROM python:3.9-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for build
WORKDIR /build

# Install Python dependencies
COPY docker/btc-live-feed/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install wheel && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy application source
COPY omega_ai /build/omega_ai/
COPY scripts /build/scripts/

# Clean up the source code (remove __pycache__, .pyc files, etc.)
RUN find /build -type d -name __pycache__ -exec rm -rf {} +

# 🔒 Stage 2: Runtime - "The Incorruptible Vessel"
FROM python:3.9-slim

# Add container metadata
LABEL maintainer="OMEGA BTC AI <divine@omega-btc-ai.com>"
LABEL version="1.0.0"
LABEL anti_debt_protected="true"
LABEL image_signing="dct+cosign"

# Create non-root user
RUN addgroup --system omega && adduser --system --group omega

# Create directory structure with proper permissions
RUN mkdir -p /app /app/data /app/config /tmp/omega && \
    chown -R omega:omega /app /tmp/omega && \
    chmod -R 555 /app && \
    chmod -R 755 /app/data /tmp/omega

# Copy Python dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --from=builder --chown=omega:omega /build/omega_ai /app/omega_ai
COPY --from=builder --chown=omega:omega /build/scripts/run_btc_feed.py /app/
COPY --from=builder --chown=omega:omega /build/scripts/run_btc_live_feed_v3_local.sh /app/

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    TEMPDIR=/tmp/omega \
    BTC_FEED_PORT=8080 \
    REDIS_HOST=localhost \
    REDIS_PORT=6379

# Create a basic healthcheck script
RUN echo '#!/bin/sh\n\
    curl -s http://localhost:$BTC_FEED_PORT/health || exit 1' > /app/healthcheck.sh && \
    chmod +x /app/healthcheck.sh

# Set up health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD /app/healthcheck.sh

# Expose port
EXPOSE 8080

# Use non-root user
USER omega

# Set working directory
WORKDIR /app

# Define entrypoint
ENTRYPOINT ["python", "/app/run_btc_feed.py"]

# Default command with parameters
CMD ["--port", "8080", "--redis-host", "${REDIS_HOST}", "--redis-port", "${REDIS_PORT}"] 