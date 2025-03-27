#!/bin/bash

# ANSI colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== REDIS MONITOR SERVER RESTART =====${NC}"

# Stop any existing processes
echo -e "${YELLOW}Stopping any existing Redis monitor server processes...${NC}"
pkill -f redis_monitor_server.py 2>/dev/null
pkill -f redis_monitor_server_optimized.py 2>/dev/null
pkill -f reggae_dashboard_server.py 2>/dev/null

sleep 1

# Check if processes were successfully terminated
if pgrep -f "redis_monitor_server.py" > /dev/null || pgrep -f "redis_monitor_server_optimized.py" > /dev/null || pgrep -f "reggae_dashboard_server.py" > /dev/null; then
    echo -e "${RED}Failed to stop all monitor processes. Forcing termination...${NC}"
    pkill -9 -f redis_monitor_server.py 2>/dev/null
    pkill -9 -f redis_monitor_server_optimized.py 2>/dev/null
    pkill -9 -f reggae_dashboard_server.py 2>/dev/null
    sleep 1
fi

# Start Redis monitor server in background
echo -e "${GREEN}Starting optimized Redis monitor server...${NC}"
./redis_monitor_server_optimized.py &
REDIS_MONITOR_PID=$!

# Wait for it to initialize
sleep 2

# Check if it's running
if ps -p $REDIS_MONITOR_PID > /dev/null; then
    echo -e "${GREEN}Redis monitor server started successfully (PID: $REDIS_MONITOR_PID)${NC}"
else
    echo -e "${RED}Failed to start Redis monitor server${NC}"
    exit 1
fi

# Test connection
echo -e "${YELLOW}Testing monitor API...${NC}"
curl -s --max-time 5 http://localhost:5002/ | head -20 || echo -e "${RED}Failed to connect to monitor API${NC}"
echo -e "..."

# Check health endpoint
echo -e "${YELLOW}Checking health endpoint...${NC}"
curl -s --max-time 5 http://localhost:5002/api/health | jq . || echo -e "${RED}Failed to check health endpoint${NC}"

echo -e "${BLUE}Monitor restart complete!${NC}"
echo -e "${YELLOW}Redis monitor is running in the background (PID: $REDIS_MONITOR_PID)${NC}"
echo -e "Use the following URL to access the monitor: http://localhost:5002/"
echo -e "Available endpoints:"
echo -e "  - http://localhost:5002/api/health"
echo -e "  - http://localhost:5002/api/redis-info"
echo -e "  - http://localhost:5002/api/redis-keys" 