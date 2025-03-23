FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV FIBONACCI_ALIGNED=true

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir websocket-client redis ccxt matplotlib numpy pandas

# Copy project files
COPY omega_ai /app/omega_ai/
COPY scripts /app/scripts/

# Create directory for logs
RUN mkdir -p /app/logs

# Add version label
LABEL version="1.0.0" \
    description="BTC Live Feed - Part of the Fibonacci-Aligned Architecture (1)" \
    maintainer="OMEGA-BTC-AI"

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import redis; redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=int(os.getenv('REDIS_PORT', '6379'))).ping()" || exit 1

# Set default command
CMD ["python", "-m", "omega_ai.data_feed.btc_live_feed"] 