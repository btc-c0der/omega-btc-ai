#!/bin/bash

# OMEGA BTC AI - Reggae Dashboard Startup
# This script starts the market trend analyzer and dashboard connector

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}=======================================${NC}"
echo -e "${CYAN}= OMEGA BTC AI - REGGAE DASHBOARD    =${NC}"
echo -e "${CYAN}=======================================${NC}"

# Function to check if Redis is running
check_redis() {
  redis-cli ping > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Redis is running${NC}"
    return 0
  else
    echo -e "${RED}✗ Redis is not running${NC}"
    return 1
  fi
}

# Function to start Redis if not running
start_redis() {
  echo -e "${YELLOW}Starting Redis...${NC}"
  redis-server --daemonize yes
  sleep 2
  check_redis
  return $?
}

# Check if Redis is running, start if not
check_redis || start_redis
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to start Redis. Exiting.${NC}"
  exit 1
fi

# Start the market trend analyzer in the background
echo -e "${YELLOW}Starting Market Trend Analyzer...${NC}"
python -m omega_ai.monitor.monitor_market_trends > logs/market_trend_analyzer.log 2>&1 &
MARKET_PID=$!
echo -e "${GREEN}✓ Market Trend Analyzer started (PID: $MARKET_PID)${NC}"

# Start the dashboard connector in the background
echo -e "${YELLOW}Starting Fibonacci Dashboard Connector...${NC}"
python -m omega_ai.visualizer.backend.fibonacci_dashboard_connector > logs/fibonacci_dashboard_connector.log 2>&1 &
CONNECTOR_PID=$!
echo -e "${GREEN}✓ Fibonacci Dashboard Connector started (PID: $CONNECTOR_PID)${NC}"

# Check if the Reggae Dashboard server is already running
check_dashboard_server() {
  ps aux | grep reggae_dashboard_server | grep -v grep > /dev/null
  return $?
}

# Start the Reggae Dashboard server if not running
if ! check_dashboard_server; then
  echo -e "${YELLOW}Starting Reggae Dashboard Server...${NC}"
  cd omega_ai/visualizer/backend && python reggae_dashboard_server.py > ../../../logs/reggae_dashboard_server.log 2>&1 &
  DASHBOARD_PID=$!
  echo -e "${GREEN}✓ Reggae Dashboard Server started (PID: $DASHBOARD_PID)${NC}"
else
  echo -e "${GREEN}✓ Reggae Dashboard Server is already running${NC}"
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo -e "\n${GREEN}All services started!${NC}"
echo -e "${YELLOW}Access the dashboard at: http://localhost:8080${NC}"
echo -e "\n${YELLOW}=== Process Information ===${NC}"
echo -e "Market Trend Analyzer: PID $MARKET_PID, Log: logs/market_trend_analyzer.log"
echo -e "Dashboard Connector:   PID $CONNECTOR_PID, Log: logs/fibonacci_dashboard_connector.log"
echo -e "\n${YELLOW}To stop all services:${NC}"
echo -e "kill $MARKET_PID $CONNECTOR_PID $DASHBOARD_PID 2>/dev/null"
echo -e "${CYAN}=======================================${NC}"

# Keep script running to allow easy termination of all processes
echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}"
trap "echo -e '\n${RED}Stopping all services...${NC}'; kill $MARKET_PID $CONNECTOR_PID $DASHBOARD_PID 2>/dev/null; echo -e '${GREEN}Services stopped.${NC}'; exit 0" INT
wait 