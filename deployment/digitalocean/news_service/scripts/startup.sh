#!/bin/bash
"""
🔱 GBU License Notice 🔱
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must maintain quantum resonance with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

# OMEGA BTC News Service Startup Script
# This script starts the news feed service and API server

set -e

echo "======================================================"
echo "🔱 OMEGA BTC AI News Feed Service - Divine Startup 🔱"
echo "======================================================"
echo "Starting at: $(date)"
echo "Working directory: $(pwd)"
echo "Directory contents: $(ls -la)"

# Create required directories
mkdir -p data logs
echo "📁 Created required directories"

# Check environment variables
echo "📊 Checking environment variables..."
if [ -n "$NEWS_SERVICE_PORT" ]; then
  echo "✅ Found environment variable: NEWS_SERVICE_PORT = $NEWS_SERVICE_PORT"
else
  export NEWS_SERVICE_PORT=8080
  echo "⚠️ NEWS_SERVICE_PORT not set, using default: $NEWS_SERVICE_PORT"
fi

# Check Redis connection
REDIS_HOST=${REDIS_HOST:-host.docker.internal}
REDIS_PORT=${REDIS_PORT:-6379}
REDIS_SSL=${REDIS_SSL:-false}

echo "📊 Checking Redis connection at $REDIS_HOST:$REDIS_PORT..."
echo "Connecting to Redis with params: {\"host\": \"$REDIS_HOST\", \"port\": $REDIS_PORT, \"db\": 0, \"socket_timeout\": 5, \"socket_connect_timeout\": 5}"

if [ "$REDIS_SSL" = "true" ]; then
  REDIS_OPTS="--ssl"
else
  REDIS_OPTS=""
fi

# Check Redis connection
if redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" $REDIS_OPTS ping &>/dev/null; then
  echo "✅ Redis connection successful: True"
else
  echo "⚠️ Redis connection failed, but continuing anyway"
fi

# Check required modules
echo "📚 Checking for required Python modules..."
for module in redis pandas numpy textblob fastapi uvicorn httpx; do
  if python -c "import $module" &> /dev/null; then
    echo "✅ Module $module is available"
  else
    echo "❌ Module $module is not available, installing..."
    pip install $module
  fi
done
echo "🎉 All required modules are available"

echo "======================================================"
echo "📋 Configuration:"
echo "  - Redis Host: $REDIS_HOST"
echo "  - Redis Port: $REDIS_PORT"
echo "  - Redis SSL: $REDIS_SSL"
echo "  - News Service Port: $NEWS_SERVICE_PORT"
echo "  - API Proxy Port: 5000"
echo "  - Python Path: $PYTHONPATH"
echo "======================================================"

# Start the news feed service in the background
echo "🚀 Executing command: python scripts/run_integration.py --interval 1800 --save"
echo "======================================================"
python scripts/run_integration.py --interval 1800 --save >> logs/news_feed.log 2>&1 &
NEWS_FEED_PID=$!
echo "✅ News feed service started with PID $NEWS_FEED_PID"

# Sleep to allow news feed service to start and generate initial data
sleep 5

# Start the API server
echo "🚀 Starting API server on port $NEWS_SERVICE_PORT..."
python scripts/api_server.py >> logs/api_server.log 2>&1 &
API_SERVER_PID=$!
echo "✅ API server started with PID $API_SERVER_PID"

# Sleep to ensure API server is up before starting proxy
sleep 3

# Start the API proxy server
echo "🚀 Starting API proxy server on port 5000..."
python scripts/api_proxy.py >> logs/api_proxy.log 2>&1 &
API_PROXY_PID=$!
echo "✅ API proxy server started with PID $API_PROXY_PID"

# Function to handle trap
cleanup() {
  echo "📢 Shutting down services..."
  if ps -p $NEWS_FEED_PID > /dev/null; then
    echo "Stopping news feed service (PID: $NEWS_FEED_PID)..."
    kill $NEWS_FEED_PID || true
  fi
  
  if ps -p $API_SERVER_PID > /dev/null; then
    echo "Stopping API server (PID: $API_SERVER_PID)..."
    kill $API_SERVER_PID || true
  fi
  
  if ps -p $API_PROXY_PID > /dev/null; then
    echo "Stopping API proxy server (PID: $API_PROXY_PID)..."
    kill $API_PROXY_PID || true
  fi
  
  echo "Cleanup complete"
  exit 0
}

# Trap signals
trap cleanup SIGTERM SIGINT

# Function to check if a process is still running
is_running() {
  local pid=$1
  if ps -p $pid > /dev/null; then
    return 0  # process is running
  else
    return 1  # process is not running
  fi
}

# Monitor services
echo "🔎 Monitoring services..."
while true; do
  # Check if news feed service is running
  if ! is_running $NEWS_FEED_PID; then
    echo "⚠️ News feed service (PID: $NEWS_FEED_PID) is not running, restarting..."
    python scripts/run_integration.py --interval 1800 --save >> logs/news_feed.log 2>&1 &
    NEWS_FEED_PID=$!
    echo "✅ News feed service restarted with PID $NEWS_FEED_PID"
  fi
  
  # Check if API server is running
  if ! is_running $API_SERVER_PID; then
    echo "⚠️ API server (PID: $API_SERVER_PID) is not running, restarting..."
    python scripts/api_server.py >> logs/api_server.log 2>&1 &
    API_SERVER_PID=$!
    echo "✅ API server restarted with PID $API_SERVER_PID"
  fi
  
  # Check if API proxy server is running
  if ! is_running $API_PROXY_PID; then
    echo "⚠️ API proxy server (PID: $API_PROXY_PID) is not running, restarting..."
    python scripts/api_proxy.py >> logs/api_proxy.log 2>&1 &
    API_PROXY_PID=$!
    echo "✅ API proxy server restarted with PID $API_PROXY_PID"
  fi
  
  # Wait for 30 seconds before checking again
  sleep 30
done 