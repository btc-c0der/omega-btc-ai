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
COPY omega_ai/tools/trap_probability_meter.py omega_ai/tools/
COPY omega_ai/utils/trap_probability_utils.py omega_ai/utils/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the trap probability meter
CMD ["python", "-m", "omega_ai.tools.trap_probability_meter"] 