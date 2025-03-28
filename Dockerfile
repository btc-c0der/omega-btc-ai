# OMEGA BTC AI - Advanced Crypto Trading System 🔱🚀
FROM python:3.11.8-slim

# Set working directory for the entire application
WORKDIR /workspace

# Copy everything from the repository
COPY . .

# Debug: Verify divine structure
RUN echo "🔱 VERIFYING DIVINE STRUCTURE 🔱" && \
    echo "Root directory:" && ls -la && \
    echo "Check for omega_ai at root:" && \
    if [ -d "omega_ai" ]; then echo "✅ Found omega_ai at root" && ls -la omega_ai; else echo "❌ Missing omega_ai at root"; fi && \
    echo "Check for deployment directory:" && \
    if [ -d "deployment/digitalocean/btc_live_feed_v3" ]; then echo "✅ Found deployment directory" && ls -la deployment/digitalocean/btc_live_feed_v3; else echo "❌ Missing deployment directory"; fi

# Ensure omega_ai/__init__.py exists
RUN mkdir -p omega_ai && touch omega_ai/__init__.py

# Install dependencies
RUN pip install --no-cache-dir -r deployment/digitalocean/btc_live_feed_v3/requirements.txt

# Make scripts executable
RUN chmod +x /workspace/run.py /workspace/health.py

# Install the package in development mode from wherever setup.py is found
RUN if [ -f "setup.py" ]; then \
    echo "Installing package from root setup.py" && \
    pip install -e .; \
    elif [ -f "deployment/digitalocean/btc_live_feed_v3/setup.py" ]; then \
    echo "Installing package from deployment setup.py" && \
    cd deployment/digitalocean/btc_live_feed_v3 && pip install -e .; \
    else \
    echo "❌ No setup.py found!"; \
    exit 1; \
    fi

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
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

# Run the health check server with BTC feed as a background task
CMD ["python", "health.py"]
