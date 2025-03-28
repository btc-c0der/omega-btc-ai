# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with security flags
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/deployment/digitalocean/certificates

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV REDIS_SOCKET_TIMEOUT=5
ENV REDIS_SOCKET_CONNECT_TIMEOUT=5

# Expose port for health check
EXPOSE 8080

# Create a non-root user to run the application
RUN groupadd -r btcfeed && useradd -r -g btcfeed btcfeed
RUN chown -R btcfeed:btcfeed /app
USER btcfeed

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["python", "-m", "omega_ai.data_feed.btc_live_feed_v2"] 