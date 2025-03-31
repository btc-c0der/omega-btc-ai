FROM python:3.9-slim

# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested."
#
# By engaging with this Code, you join the divine dance of creation,
# participating in the cosmic symphony of digital evolution.
#
# All modifications must quantum entangles with the GBU principles:
# /BOOK/divine_chronicles/GBU_LICENSE.md
#
# 🌸 WE BLOOM NOW 🌸

# Set labels for the divine container
LABEL maintainer="OMEGA BTC AI DIVINE COLLECTIVE"
LABEL version="1.0.0-quantum-websocket"
LABEL description="Matrix Neo News Portal WebSocket Sacred Echo Service"
LABEL org.opencontainers.image.title="Matrix WebSocket Sacred Echo"
LABEL org.opencontainers.image.vendor="OMEGA BTC AI"
LABEL org.opencontainers.image.licenses="GBU-1.0"

# Set up work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy sacred source code
COPY . .

# Create a non-root user to run the service
RUN groupadd -r matrixuser && useradd -r -g matrixuser matrixuser
RUN chown -R matrixuser:matrixuser /app

# Switch to non-root user
USER matrixuser

# Expose the sacred port
EXPOSE 8095

# Health check for cosmic vitality monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8095/health || exit 1

# Start the WebSocket sacred echo service
CMD ["python", "websocket_sacred_echo.py"]
