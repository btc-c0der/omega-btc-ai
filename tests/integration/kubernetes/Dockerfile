# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/stable.txt" && \
    curl -LO "https://dl.k8s.io/release/$(cat stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl && \
    rm stable.txt

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Nicole Sewell's Quantum Metrics dependencies
RUN pip install --no-cache-dir numpy pandas

# Copy test files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV KUBERNETES_SERVICE_HOST=host.docker.internal
ENV KUBERNETES_SERVICE_PORT=6443

# Create non-root user
RUN useradd -m -u 1000 testuser
USER testuser

# Default command to run tests
CMD ["pytest", "-v"] 