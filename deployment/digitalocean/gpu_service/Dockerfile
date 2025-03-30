FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    curl \
    wget \
    sysstat \
    htop \
    nvidia-utils-535 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Copy startup script and make it executable
COPY deployment/digitalocean/gpu_service/startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Create necessary directories
RUN mkdir -p /app/models /app/data /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Expose ports
EXPOSE 8080 9100

# Start the application with the startup script
CMD ["/bin/bash", "-c", "/app/startup.sh && python3 app.py"] 