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
    && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY temp_deployment_package/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir \
    websocket-client \
    redis \
    ccxt \
    matplotlib \
    numpy \
    pandas \
    cryptography

# Create directory for logs and config
RUN mkdir -p /app/logs /app/config

# Copy redis manager and btc live feed cloud modules
COPY temp_deployment_package/redis_manager_cloud.py /app/redis_manager_cloud.py
COPY temp_deployment_package/btc_live_feed_cloud.py /app/btc_live_feed_cloud.py
COPY temp_deployment_package/btc_gpu_accelerator.py /app/btc_gpu_accelerator.py

# Add version label
LABEL version="0.420" \
    description="BTC Live Feed - Sacred Bitcoin Price Stream" \
    maintainer="OMEGA-BTC-AI"

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import os, redis; password=os.getenv('REDIS_PASSWORD', ''); username=os.getenv('REDIS_USERNAME', ''); host=os.getenv('REDIS_HOST', 'redis'); port=int(os.getenv('REDIS_PORT', '6379')); use_tls=os.getenv('REDIS_USE_TLS', 'false').lower() == 'true'; ssl_ca_certs=os.getenv('REDIS_CERT', None) if use_tls else None; r = redis.Redis(host=host, port=port, username=username, password=password, ssl=use_tls, ssl_ca_certs=ssl_ca_certs); r.ping()" || exit 1

# Set default command to run the cloud-compatible module
CMD ["python", "/app/btc_live_feed_cloud.py"] 