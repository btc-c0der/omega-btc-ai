# OMEGA BTC AI - Advanced Crypto Trading System 🔱🚀
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    POSTGRES_DB=omega_db \
    POSTGRES_USER=omega_user \
    POSTGRES_PASSWORD=omega_pass \
    POSTGRES_HOST=postgres \
    POSTGRES_PORT=5432 \
    LOG_LEVEL=INFO

# Create project directories
WORKDIR /app
RUN mkdir -p /app/logs /app/data /app/redis_data /app/postgres_data

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    redis-tools \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY omega_ai/ /app/omega_ai/
COPY tools/ /app/tools/
COPY run_omega_btc_ai.py /app/
COPY start_services.sh /app/

# Make scripts executable
RUN chmod +x /app/start_services.sh /app/tools/*.py /app/tools/*.sh

# Set up volumes
VOLUME ["/app/logs", "/app/data", "/app/redis_data", "/app/postgres_data"]

# Expose ports
EXPOSE 6379 5432 8765 8050

# Start all services
ENTRYPOINT ["bash", "start_services.sh"]
