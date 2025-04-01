#!/bin/bash

# OMEGA BTC AI - Run BTC Live Feed v3 Locally
# ===========================================
# This script runs BTC Live Feed v3 using local Redis instance

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Logo display
echo -e "${MAGENTA}"
echo "🔱 OMEGA BTC AI - BTC Live Feed v3 Local Mode 🔱"
echo -e "${RESET}"

# Check if Redis is running locally
echo -e "${YELLOW}Checking if Redis is running locally...${RESET}"
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${RED}Error: Redis is not running locally. Please start Redis first.${RESET}"
    echo "You can start Redis with: brew services start redis (macOS) or redis-server (Linux)"
    exit 1
fi

echo -e "${GREEN}Redis is running locally.${RESET}"

# Check if port 8080 is available for the health check server
echo -e "${YELLOW}Checking if port 8080 is available...${RESET}"
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}Error: Port 8080 is already in use. The health check server needs this port.${RESET}"
    echo "Please stop the process using port 8080 or modify the HEALTH_CHECK_PORT in this script."
    exit 1
fi

echo -e "${GREEN}Port 8080 is available.${RESET}"

# Kill any existing btc_live_feed_v3.py processes
echo -e "${YELLOW}Stopping any existing BTC Live Feed v3 processes...${RESET}"
pkill -f "python.*btc_live_feed_v3.py" || true
pkill -f "python -m omega_ai.data_feed.btc_live_feed_v3" || true

# Environment variables for the feed
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_USERNAME=""  # Usually empty for local Redis
export REDIS_PASSWORD=""  # Usually empty for local Redis
export REDIS_USE_SSL="false"
export FAILOVER_REDIS_HOST="localhost"
export FAILOVER_REDIS_PORT="6379"
export HEALTH_CHECK_PORT="8080"
export HEALTH_CHECK_HOST="0.0.0.0"
export USE_FAILOVER="true"  # Enable failover mode even though we're using the same Redis

# Start BTC Live Feed v3 in a terminal
echo -e "${GREEN}Starting BTC Live Feed v3...${RESET}"
echo -e "${YELLOW}Environment variables:${RESET}"
echo "REDIS_HOST=$REDIS_HOST"
echo "REDIS_PORT=$REDIS_PORT"
echo "REDIS_USE_SSL=$REDIS_USE_SSL"
echo "FAILOVER_REDIS_HOST=$FAILOVER_REDIS_HOST"
echo "FAILOVER_REDIS_PORT=$FAILOVER_REDIS_PORT"
echo "HEALTH_CHECK_PORT=$HEALTH_CHECK_PORT"

# Start the BTC Live Feed v3 in the background
python -m omega_ai.data_feed.btc_live_feed_v3 &
FEED_PID=$!

# Start the Health Check server in the background
echo -e "${GREEN}Starting Health Check server...${RESET}"
python -m omega_ai.data_feed.health_check &
HEALTH_PID=$!

# Start the monitoring dashboard
echo -e "${GREEN}Starting Monitoring Dashboard...${RESET}"
echo -e "${CYAN}Press Ctrl+C to stop all processes${RESET}"
sleep 2  # Give the services a moment to start

python scripts/monitor_btc_feed_v3.py --host localhost --port 8080 --refresh 5

# Cleanup on exit
echo -e "${YELLOW}Stopping all processes...${RESET}"
kill $FEED_PID $HEALTH_PID 2>/dev/null
pkill -f "python.*btc_live_feed_v3.py" 2>/dev/null || true
pkill -f "python -m omega_ai.data_feed.btc_live_feed_v3" 2>/dev/null || true
pkill -f "python -m omega_ai.data_feed.health_check" 2>/dev/null || true

echo -e "${GREEN}All processes stopped.${RESET}" 