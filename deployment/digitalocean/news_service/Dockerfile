# Use an official Python runtime as the base image
FROM python:3.9-slim

# GBU License Notice - Copyright Block
LABEL maintainer="OMEGA BTC AI Team <omega-ai@example.com>"
LABEL description="OMEGA BTC AI News Feed Service - Divine Blockchain Intelligence"
LABEL version="3.0"
LABEL license="GBU License (Genesis-Bloom-Unfoldment) 1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    NEWS_SERVICE_PORT=8080

# Working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data/news logs

# Set up the entrypoint script (will create it in next step)
COPY scripts/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose the port the service will run on
EXPOSE ${NEWS_SERVICE_PORT}

# Run the service when the container launches
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "scripts/run_integration.py", "--interval", "1800", "--save"] 