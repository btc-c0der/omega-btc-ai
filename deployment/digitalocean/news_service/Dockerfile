# Use an official Python runtime as the base image
FROM python:3.11.8-slim

# GBU License Notice - Copyright Block
LABEL maintainer="OMEGA BTC AI Team <omega-ai@example.com>"
LABEL description="OMEGA BTC AI News Feed Service - Divine Blockchain Intelligence"
LABEL version="3.0"
LABEL license="GBU License (Genesis-Bloom-Unfoldment) 1.0"

# Set working directory
WORKDIR /workspace

# Copy everything needed for the application
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Debug: Verify directory structure
RUN echo "🔱 VERIFYING DIVINE STRUCTURE 🔱" && \
    echo "Root directory:" && ls -la && \
    echo "News service directory:" && ls -la && \
    echo "Check for omega_ai:" && \
    if [ -d "omega_ai" ]; then echo "✅ Found omega_ai" && ls -la omega_ai; else echo "❌ Missing omega_ai"; fi

# Ensure omega_ai/__init__.py exists
RUN mkdir -p omega_ai && touch omega_ai/__init__.py

# Create necessary directories
RUN mkdir -p data/news logs

# Install the package in development mode
RUN pip install -e .

# Copy and set up the entrypoint script
COPY scripts/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose the port the service will run on
EXPOSE 8080
EXPOSE 8081

# Set environment variables
ENV REDIS_HOST=${REDIS_HOST:-redis}
ENV REDIS_PORT=${REDIS_PORT:-6379}
ENV REDIS_USERNAME=${REDIS_USERNAME:-}
ENV REDIS_PASSWORD=${REDIS_PASSWORD:-}
ENV REDIS_SSL=${REDIS_SSL:-false}
ENV REDIS_USE_TLS=${REDIS_USE_TLS:-false}
ENV REDIS_SSL_CERT_REQS=${REDIS_SSL_CERT_REQS:-none}
ENV PYTHONPATH=/workspace:/workspace/src
ENV NEWS_SERVICE_PORT=8080
ENV TZ=UTC
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the service when the container launches
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "scripts/run_integration.py", "--interval", "1800", "--save"] 