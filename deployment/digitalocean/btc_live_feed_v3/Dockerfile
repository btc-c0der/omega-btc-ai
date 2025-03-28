FROM python:3.11.8-slim

WORKDIR /workspace/deployment/digitalocean/btc_live_feed_v3

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and configuration files
COPY src/ ./src/
COPY .env .
COPY Procfile .
COPY setup.py .

# Create a simpler entry point
RUN echo '#!/usr/bin/env python3\nimport os\nimport sys\nimport asyncio\n\n# Add src to path\nsys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3/src")\n\n# Import the feed\nfrom src.omega_ai.data_feed.btc_live_feed_v3 import run_btc_live_feed_v3\n\nif __name__ == "__main__":\n    print("Starting BTC Live Feed v3...")\n    asyncio.run(run_btc_live_feed_v3())\n' > run.py
RUN chmod +x run.py

# Install the package
RUN pip install -e .

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
ENV PYTHONPATH=/workspace/deployment/digitalocean/btc_live_feed_v3:/workspace/deployment/digitalocean/btc_live_feed_v3/src

# Run the web service using our entry point
CMD ["python", "run.py"] 