FROM python:3.11.8-slim

WORKDIR /workspace/deployment/digitalocean/btc_live_feed_v3

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and configuration files
COPY omega_ai/ ./omega_ai/
COPY .env .
COPY Procfile .
COPY setup.py .

# Create a direct script to run the application
RUN cat > run.py << 'EOL'
#!/usr/bin/env python3
import os
import sys
import asyncio

# Add workspace to path
sys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3")

try:
# Import directly from the omega_ai package
from omega_ai.data_feed.btc_live_feed_v3 import run_btc_live_feed_v3
except ImportError as e:
print(f"ERROR: Could not import the BTC Live Feed module: {e}")
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print("Directory contents:")
os.system("ls -la")
print("omega_ai directory contents:")
os.system("ls -la omega_ai")
if os.path.exists("omega_ai/data_feed"):
print("data_feed directory contents:")
os.system("ls -la omega_ai/data_feed")
sys.exit(1)

if __name__ == "__main__":
print("Starting BTC Live Feed v3...")
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
try:
asyncio.run(run_btc_live_feed_v3())
except Exception as e:
import traceback
print(f"Error running BTC Live Feed v3: {e}")
traceback.print_exc()
sys.exit(1)
EOL
RUN chmod +x run.py

# Create a health check script
RUN cat > health.py << 'EOL'
#!/usr/bin/env python3
import os
import sys
import uvicorn

# Add workspace to path
sys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3")

try:
# Import directly from the omega_ai package
from omega_ai.data_feed.health_check import app
except ImportError as e:
print(f"ERROR: Could not import the Health Check module: {e}")
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print("Directory contents:")
os.system("ls -la")
print("omega_ai directory contents:")
os.system("ls -la omega_ai")
if os.path.exists("omega_ai/data_feed"):
print("data_feed directory contents:")
os.system("ls -la omega_ai/data_feed")
sys.exit(1)

if __name__ == "__main__":
print("Starting Health Check Server...")
host = os.getenv("HEALTH_CHECK_HOST", "0.0.0.0")
port = int(os.getenv("HEALTH_CHECK_PORT", "8080"))
uvicorn.run(app, host=host, port=port, log_level="info")
EOL
RUN chmod +x health.py

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
ENV PYTHONPATH=/workspace/deployment/digitalocean/btc_live_feed_v3

# Run the web service using our entry point
CMD ["python", "run.py"] 