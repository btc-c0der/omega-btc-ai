FROM python:3.9-slim

WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install specific trading dependencies including CCXT
RUN pip install --no-cache-dir \
    ccxt==3.0.52 \
    ta==0.10.2 \
    numpy==1.24.3 \
    pandas==2.0.1 \
    scipy==1.10.1 \
    statsmodels==0.14.0 \
    asyncio==3.4.3 \
    redis==4.5.4 \
    fastapi==0.95.1 \
    uvicorn==0.22.0 \
    aiohttp==3.8.4 \
    python-dotenv==1.0.0

# Copy application code
COPY . .

# Copy .env file if available (for local development)
RUN if [ -f "/app/.env" ]; then echo "Using existing .env file"; else echo "No .env file found, will use environment variables"; fi

# Create necessary directories
RUN mkdir -p /app/logs /app/data

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LOG_LEVEL=INFO \
    REDIS_HOST=redis \
    REDIS_PORT=6379

# Expose API port
EXPOSE 8080

# Use a non-root user
RUN useradd -m botuser
RUN chown -R botuser:botuser /app
USER botuser

# Command to run a specific bot - will be overridden by kubernetes
CMD ["python", "-m", "src.omega_bot_farm.trading.bots.ccxt_strategic_trader"] 