FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY omega_ai/trading/strategies/trap_aware_dual_traders.py omega_ai/trading/strategies/
COPY omega_ai/trading/exchanges/dual_position_traders.py omega_ai/trading/exchanges/
COPY omega_ai/utils/ omega_ai/utils/

# Create config directory
RUN mkdir -p /app/config

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the trap-aware traders
CMD ["python", "-m", "omega_ai.trading.strategies.trap_aware_dual_traders"] 