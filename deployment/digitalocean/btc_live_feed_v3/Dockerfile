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

# Create a direct script to run the application
RUN echo '#!/usr/bin/env python3\n\
    import os\n\
    import sys\n\
    import asyncio\n\
    \n\
    # Add src to path\n\
    sys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3")\n\
    sys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3/src")\n\
    \n\
    # Import the feed directly from the file\n\
    from src.omega_ai.data_feed.btc_live_feed_v3 import run_btc_live_feed_v3\n\
    \n\
    if __name__ == "__main__":\n\
    print("Starting BTC Live Feed v3...")\n\
    print(f"Python path: {sys.path}")\n\
    print(f"Current directory: {os.getcwd()}")\n\
    try:\n\
    asyncio.run(run_btc_live_feed_v3())\n\
    except Exception as e:\n\
    import traceback\n\
    print(f"Error running BTC Live Feed v3: {e}")\n\
    traceback.print_exc()\n\
    sys.exit(1)\n\
    ' > run.py && chmod +x run.py

# Create a health check script
RUN echo '#!/usr/bin/env python3\n\
    import os\n\
    import sys\n\
    import uvicorn\n\
    \n\
    # Add src to path\n\
    sys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3")\n\
    sys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3/src")\n\
    \n\
    from src.omega_ai.data_feed.health_check import app\n\
    \n\
    if __name__ == "__main__":\n\
    print("Starting Health Check Server...")\n\
    host = os.getenv("HEALTH_CHECK_HOST", "0.0.0.0")\n\
    port = int(os.getenv("HEALTH_CHECK_PORT", "8080"))\n\
    uvicorn.run(app, host=host, port=port, log_level="info")\n\
    ' > health.py && chmod +x health.py

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