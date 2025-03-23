#!/bin/bash

# OMEGA BTC AI - Divine Dashboard Launcher
# Starts both the Golden Ratio API and Divine Dashboard

# Colors for output
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
RED="\033[0;31m"
RESET="\033[0m"

# Default port
PORT=5051

# Function to check if Redis is running
check_redis() {
    if ! redis-cli ping > /dev/null 2>&1; then
        echo -e "${RED}Error: Redis is not running${RESET}"
        echo -e "${YELLOW}Please start Redis first with: brew services start redis${RESET}"
        exit 1
    fi
}

# Function to check if port is in use
check_port() {
    if lsof -i :$PORT > /dev/null; then
        echo -e "${RED}Error: Port $PORT is already in use${RESET}"
        echo -e "${YELLOW}Please free up port $PORT or use a different port${RESET}"
        exit 1
    fi
}

# Print header
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║             OMEGA BTC AI - Divine Dashboard Launcher             ║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${RESET}"
echo

# Check Redis
echo -e "${YELLOW}Checking Redis...${RESET}"
check_redis
echo -e "${GREEN}✓ Redis is running${RESET}"

# Check port
echo -e "${YELLOW}Checking port $PORT...${RESET}"
check_port
echo -e "${GREEN}✓ Port $PORT is available${RESET}"

# Start the Golden Ratio API
echo -e "\n${CYAN}Starting Golden Ratio API...${RESET}"
python golden_ratio_api.py --port $PORT &
API_PID=$!

# Wait for API to start
echo -e "${YELLOW}Waiting for API to initialize...${RESET}"
sleep 3

# Check if API is running
if ! kill -0 $API_PID 2>/dev/null; then
    echo -e "${RED}Error: Failed to start Golden Ratio API${RESET}"
    exit 1
fi

echo -e "${GREEN}✓ Golden Ratio API is running${RESET}"
echo -e "${CYAN}Dashboard is accessible at: http://localhost:$PORT/divine${RESET}"

# Keep running until interrupted
echo -e "\n${YELLOW}Press Ctrl+C to stop the dashboard${RESET}"
wait $API_PID 