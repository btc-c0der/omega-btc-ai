# OMEGA BTC AI - WebSocket Server 🚀
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH="${PYTHONPATH}:/app" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMEGA_ENV="production" \
    PORT=8765

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy deployment requirements first for better caching
COPY requirements.deploy.txt .
RUN pip install --no-cache-dir -r requirements.deploy.txt

# Copy only necessary application files
COPY omega_ai/mm_trap_detector/mm_websocket_server.py ./omega_ai/mm_trap_detector/
COPY omega_ai/visualizer/backend/ascii_art.py ./omega_ai/visualizer/backend/
COPY omega_ai/utils/redis_manager.py ./omega_ai/utils/
COPY omega_ai/__init__.py ./omega_ai/

# Set proper permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose WebSocket port
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Run the WebSocket server with optimized settings
CMD ["uvicorn", "omega_ai.mm_trap_detector.mm_websocket_server:app", \
    "--host", "0.0.0.0", \
    "--port", "8765", \
    "--workers", "4", \
    "--limit-concurrency", "1000", \
    "--timeout-keep-alive", "30", \
    "--log-level", "info"]
