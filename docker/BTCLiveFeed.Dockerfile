FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV TF_FORCE_GPU_ALLOW_GROWTH=true

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    curl \
    netcat-openbsd \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python dependencies
COPY temp_deployment_package/requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY temp_deployment_package/ /app/

# Create log directory
RUN mkdir -p /app/logs

# Create configuration directory
RUN mkdir -p /app/config

# Health check to verify the service is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the BTC Live Feed module
CMD ["python3", "btc_live_feed_cloud.py"] 