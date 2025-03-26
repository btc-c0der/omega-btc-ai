# OMEGA BTC AI - Advanced Crypto Trading System 🔱🚀
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OMEGA_ENV="production"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose WebSocket port
EXPOSE 8765

# Run the WebSocket server
CMD ["python", "-m", "omega_ai.mm_trap_detector.mm_websocket_server"]
