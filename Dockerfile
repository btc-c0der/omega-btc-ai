# OMEGA BTC AI - Advanced Crypto Trading System 🔱🚀
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OMEGA_ENV="production"

# Install system dependencies for Plotly and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8051

# Start Redis and the dashboard
CMD service redis-server start && python -m omega_ai.visualization.dashboard
