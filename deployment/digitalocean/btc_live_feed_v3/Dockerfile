FROM python:3.11.8-slim

WORKDIR /workspace

# Copy everything needed for the application
COPY . /workspace/

# Install dependencies
RUN pip install --no-cache-dir -r deployment/digitalocean/btc_live_feed_v3/requirements.txt

# Debug: Check if omega_ai directory exists
RUN echo "Verifying structure..." && \
    ls -la && \
    ls -la deployment/digitalocean/btc_live_feed_v3 && \
    if [ -d "omega_ai" ]; then ls -la omega_ai; fi && \
    if [ -d "deployment/digitalocean/btc_live_feed_v3/omega_ai" ]; then ls -la deployment/digitalocean/btc_live_feed_v3/omega_ai; fi

# Create a direct script to run the application
RUN cat > /workspace/deployment/digitalocean/btc_live_feed_v3/run.py << 'EOL'
#!/usr/bin/env python3
import os
import sys
import asyncio

# Add workspace to path
sys.path.insert(0, "/workspace")
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
print("Deployment directory contents:")
os.system("ls -la /workspace/deployment/digitalocean/btc_live_feed_v3")
if os.path.exists("/workspace/omega_ai"):
print("omega_ai directory contents (workspace):")
os.system("ls -la /workspace/omega_ai")
if os.path.exists("/workspace/deployment/digitalocean/btc_live_feed_v3/omega_ai"):
print("omega_ai directory contents (deployment):")
os.system("ls -la /workspace/deployment/digitalocean/btc_live_feed_v3/omega_ai")
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
RUN chmod +x /workspace/deployment/digitalocean/btc_live_feed_v3/run.py

# Create a health check script that also runs the BTC feed
RUN cat > /workspace/deployment/digitalocean/btc_live_feed_v3/health.py << 'EOL'
#!/usr/bin/env python3
import os
import sys
import asyncio
import uvicorn
from fastapi import FastAPI, BackgroundTasks

# Add workspace to path
sys.path.insert(0, "/workspace")
sys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3")

try:
# Import the required modules
from omega_ai.data_feed.health_check import app as health_app
from omega_ai.data_feed.btc_live_feed_v3 import run_btc_live_feed_v3
except ImportError as e:
print(f"ERROR: Could not import required modules: {e}")
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print("Directory contents:")
os.system("ls -la")
if os.path.exists("/workspace/omega_ai"):
print("omega_ai directory contents (workspace):")
os.system("ls -la /workspace/omega_ai")
if os.path.exists("/workspace/deployment/digitalocean/btc_live_feed_v3/omega_ai"):
print("omega_ai directory contents (deployment):")
os.system("ls -la /workspace/deployment/digitalocean/btc_live_feed_v3/omega_ai")
sys.exit(1)

# Create a background task for running the BTC feed
async def run_btc_feed_in_background():
try:
print("Starting BTC Live Feed in background...")
await run_btc_live_feed_v3()
except Exception as e:
import traceback
print(f"Error running BTC Live Feed: {e}")
traceback.print_exc()

# Add startup event to health app to run the BTC feed
@health_app.on_event("startup")
async def startup_event():
import asyncio
from fastapi import BackgroundTasks

# Create a background task for the BTC feed
background_tasks = BackgroundTasks()
background_tasks.add_task(run_btc_feed_in_background)

# Start the background task
asyncio.create_task(run_btc_feed_in_background())
print("BTC Live Feed started in background")

if __name__ == "__main__":
print("Starting Health Check Server with BTC Live Feed...")
host = os.getenv("HEALTH_CHECK_HOST", "0.0.0.0")
port = int(os.getenv("HEALTH_CHECK_PORT", "8080"))
uvicorn.run(health_app, host=host, port=port, log_level="info")
EOL
RUN chmod +x /workspace/deployment/digitalocean/btc_live_feed_v3/health.py

# Install the package
RUN cd /workspace/deployment/digitalocean/btc_live_feed_v3 && pip install -e .

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

# Run the health check server as the main process
WORKDIR /workspace/deployment/digitalocean/btc_live_feed_v3
CMD ["python", "health.py"] 