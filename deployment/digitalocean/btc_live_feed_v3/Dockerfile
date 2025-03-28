FROM python:3.11.8-slim

# Set working directory
WORKDIR /workspace

# Copy everything needed for the application
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r deployment/digitalocean/btc_live_feed_v3/requirements.txt

# Debug: Verify directory structure
RUN echo "🔱 VERIFYING DIVINE STRUCTURE 🔱" && \
    echo "Root directory:" && ls -la && \
    echo "Deployment directory:" && ls -la deployment/digitalocean/btc_live_feed_v3 && \
    echo "Check for omega_ai at root:" && \
    if [ -d "omega_ai" ]; then echo "✅ Found omega_ai at root" && ls -la omega_ai; else echo "❌ Missing omega_ai at root"; fi && \
    echo "Check for omega_ai in deployment:" && \
    if [ -d "deployment/digitalocean/btc_live_feed_v3/omega_ai" ]; then echo "✅ Found omega_ai in deployment" && ls -la deployment/digitalocean/btc_live_feed_v3/omega_ai; else echo "❌ Missing omega_ai in deployment"; fi

# Ensure omega_ai/__init__.py exists in both possible locations
RUN mkdir -p omega_ai && touch omega_ai/__init__.py && \
    mkdir -p deployment/digitalocean/btc_live_feed_v3/omega_ai && \
    touch deployment/digitalocean/btc_live_feed_v3/omega_ai/__init__.py

# Copy the run and health scripts (pre-created in the repo)
COPY deployment/digitalocean/btc_live_feed_v3/scripts/run.py /workspace/run.py
COPY deployment/digitalocean/btc_live_feed_v3/scripts/health.py /workspace/health.py
RUN chmod +x /workspace/run.py /workspace/health.py

# Install the package in development mode
RUN cd deployment/digitalocean/btc_live_feed_v3 && pip install -e .

# Expose the ports
EXPOSE 8000
EXPOSE 8080

# Set environment variables
ENV REDIS_HOST=omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com
ENV REDIS_PORT=25061
ENV REDIS_USERNAME=default
ENV REDIS_PASSWORD=AVNS_OXMpU0P0ByYEz337Fgi
ENV REDIS_SSL=true
ENV REDIS_USE_TLS=true
ENV REDIS_SSL_CERT_REQS=none
ENV PYTHONPATH=/workspace:/workspace/deployment/digitalocean/btc_live_feed_v3

# Run the health check server with BTC feed as a background task
WORKDIR /workspace
CMD ["python", "health.py"] 