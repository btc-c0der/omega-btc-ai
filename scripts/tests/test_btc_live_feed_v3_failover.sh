#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸


# OMEGA BTC AI - Test BTC Live Feed v3 Failover
# ============================================
# This script tests BTC Live Feed v3's Redis failover capability

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
echo "🔱 OMEGA BTC AI - BTC Live Feed v3 Failover Test 🔱"
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

# Setup "Primary" Redis on a different port
echo -e "${YELLOW}Starting another Redis instance on port 6380 for testing...${RESET}"
redis-server --port 6380 --daemonize yes
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to start Redis on port 6380. Continuing with just localhost:6379.${RESET}"
    # Set both to use the same Redis for testing
    PRIMARY_PORT=6379
else
    PRIMARY_PORT=6380
fi

# Environment variables for the feed
export REDIS_HOST="localhost"
export REDIS_PORT="${PRIMARY_PORT}"  # "Primary" Redis
export REDIS_USERNAME=""
export REDIS_PASSWORD=""
export REDIS_USE_SSL="false"
export FAILOVER_REDIS_HOST="localhost"
export FAILOVER_REDIS_PORT="6379"    # "Failover" Redis
export HEALTH_CHECK_PORT="8080"
export HEALTH_CHECK_HOST="0.0.0.0"
export USE_FAILOVER="true"

# Start BTC Live Feed v3 in a terminal
echo -e "${GREEN}Starting BTC Live Feed v3...${RESET}"
echo -e "${YELLOW}Environment variables:${RESET}"
echo "REDIS_HOST=$REDIS_HOST"
echo "REDIS_PORT=$REDIS_PORT (Primary Redis)"
echo "FAILOVER_REDIS_HOST=$FAILOVER_REDIS_HOST"
echo "FAILOVER_REDIS_PORT=$FAILOVER_REDIS_PORT (Failover Redis)"

# Start the BTC Live Feed v3 in the background
python -m omega_ai.data_feed.btc_live_feed_v3 &
FEED_PID=$!

# Start the Health Check server in the background
echo -e "${GREEN}Starting Health Check server...${RESET}"
python -m omega_ai.data_feed.health_check &
HEALTH_PID=$!

# Start the monitoring dashboard in the background
echo -e "${GREEN}Starting Monitoring Dashboard...${RESET}"
python scripts/monitor_btc_feed_v3.py --host localhost --port 8080 --refresh 3 &
MONITOR_PID=$!

# Give processes time to start
sleep 5

# Let it run for a bit
echo -e "${CYAN}BTC Live Feed v3 is running with primary Redis on port ${PRIMARY_PORT} and failover Redis on port 6379...${RESET}"
echo -e "${CYAN}Letting it run for 15 seconds...${RESET}"
sleep 15

# Simulate failure of the primary Redis
echo -e "${YELLOW}Simulating failure of the primary Redis...${RESET}"
if [ "$PRIMARY_PORT" == "6380" ]; then
    # Only try to stop if we created a separate Redis
    redis-cli -p 6380 shutdown
    echo -e "${RED}Primary Redis (port 6380) has been shut down. Failover should activate.${RESET}"
else
    # If we're using the same Redis, we just demonstrate the concept
    echo -e "${YELLOW}Using same Redis for primary and failover. This is just a demonstration.${RESET}"
    echo -e "${YELLOW}In a real scenario, the primary Redis would fail and failover would activate.${RESET}"
fi

echo -e "${CYAN}Waiting 15 seconds to observe failover behavior...${RESET}"
sleep 15

# Restart the primary Redis (if we're using different Redis instances)
if [ "$PRIMARY_PORT" == "6380" ]; then
    echo -e "${GREEN}Restarting the primary Redis...${RESET}"
    redis-server --port 6380 --daemonize yes
    echo -e "${GREEN}Primary Redis (port 6380) has been restarted. Feed should reconnect and sync data.${RESET}"
    echo -e "${CYAN}Waiting 15 seconds to observe reconnection behavior...${RESET}"
    sleep 15
fi

# Cleanup
echo -e "${YELLOW}Stopping all processes...${RESET}"
kill $FEED_PID $HEALTH_PID $MONITOR_PID 2>/dev/null
pkill -f "python.*btc_live_feed_v3.py" 2>/dev/null || true
pkill -f "python -m omega_ai.data_feed.btc_live_feed_v3" 2>/dev/null || true
pkill -f "python -m omega_ai.data_feed.health_check" 2>/dev/null || true
pkill -f "python scripts/monitor_btc_feed_v3.py" 2>/dev/null || true

# Stop the additional Redis instance if it's still running
if [ "$PRIMARY_PORT" == "6380" ]; then
    redis-cli -p 6380 shutdown 2>/dev/null || true
fi

echo -e "${GREEN}Test completed. All processes stopped.${RESET}" 