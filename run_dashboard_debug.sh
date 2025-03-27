#!/bin/bash
# OMEGA BTC AI - Dashboard Debug Script
# Starts only the essential components with fixed paths

# Define Rasta colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
RESET='\033[0m'
BOLD='\033[1m'
BG_BLACK='\033[40m'

# Change to script directory
cd "$(dirname "$0")"
PROJECT_ROOT=$(pwd)

# Debug banner
echo -e "${BLUE}${BOLD}=====================================================================${RESET}"
echo -e "${BLUE}${BOLD}          OMEGA BTC AI - DASHBOARD DEBUG MODE                       ${RESET}"
echo -e "${BLUE}${BOLD}=====================================================================${RESET}"
echo ""

# Display system information
echo -e "${YELLOW}${BOLD}SYSTEM INFORMATION:${RESET}"
echo -e "${GREEN}Working Directory:${RESET} $(pwd)"
echo -e "${GREEN}Python Version:${RESET} $(python --version 2>&1)"
echo -e "${GREEN}Node Version:${RESET} $(node --version 2>&1 || echo 'Not installed')"
echo -e "${GREEN}NPM Version:${RESET} $(npm --version 2>&1 || echo 'Not installed')"
echo ""

# Check for essential directories
echo -e "${YELLOW}${BOLD}CHECKING DIRECTORIES:${RESET}"
if [ -d "./omega_ai" ]; then
    echo -e "${GREEN}✓ omega_ai directory found${RESET}"
else
    echo -e "${RED}✗ omega_ai directory not found!${RESET}"
fi

if [ -d "./omega_ai/visualizer" ]; then
    echo -e "${GREEN}✓ visualizer directory found${RESET}"
else
    echo -e "${RED}✗ visualizer directory not found!${RESET}"
fi

if [ -d "./omega_ai/visualizer/backend" ]; then
    echo -e "${GREEN}✓ backend directory found${RESET}"
else
    echo -e "${RED}✗ backend directory not found!${RESET}"
fi

if [ -d "./omega_ai/visualizer/frontend" ]; then
    echo -e "${GREEN}✓ frontend directory found${RESET}"
else
    echo -e "${RED}✗ frontend directory not found!${RESET}"
fi

echo ""

# Check for essential files
echo -e "${YELLOW}${BOLD}CHECKING ESSENTIAL FILES:${RESET}"
LIVE_API_PATH=$(find ./omega_ai -name "live-api-server.py" | head -1)
if [ -n "$LIVE_API_PATH" ]; then
    echo -e "${GREEN}✓ live-api-server.py found at:${RESET} $LIVE_API_PATH"
else
    echo -e "${RED}✗ live-api-server.py not found!${RESET}"
fi

FIB_DASHBOARD_PATH=$(find ./omega_ai -name "fibonacci_dashboard_connector.py" | head -1)
if [ -n "$FIB_DASHBOARD_PATH" ]; then
    echo -e "${GREEN}✓ fibonacci_dashboard_connector.py found at:${RESET} $FIB_DASHBOARD_PATH"
else
    echo -e "${RED}✗ fibonacci_dashboard_connector.py not found!${RESET}"
fi

# Create .env.local with Redis configuration
echo -e "\n${YELLOW}${BOLD}SETTING UP ENVIRONMENT:${RESET}"
if [ ! -f .env.local ]; then
    echo -e "${GREEN}Creating .env.local file...${RESET}"
    cat > .env.local << EOF
# OMEGA BTC AI - Local Development Environment
# This file overrides settings in the main .env file

# Redis Configuration - No password for local development
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Local Development URLs
REGGAE_DASHBOARD_URL=http://localhost:5001
API_BASE_URL=http://localhost:8000
WS_URL=ws://localhost:8765

# Development Mode
NODE_ENV=development
LOG_LEVEL=DEBUG

# Local Storage Paths
LOG_DIR=./logs
DATA_DIR=./data
EOF
    echo -e "${GREEN}✓ .env.local created successfully${RESET}"
else
    echo -e "${GREEN}✓ .env.local already exists${RESET}"
fi

# Create logs directory
mkdir -p logs
echo -e "${GREEN}✓ Created logs directory${RESET}"

# Start specific components directly (not using run_omega_system.py)
echo -e "\n${YELLOW}${BOLD}STARTING COMPONENTS DIRECTLY:${RESET}"

# Start Fibonacci Dashboard Connector in background
echo -e "${GREEN}Starting Fibonacci Dashboard Connector...${RESET}"
FIB_DASHBOARD_DIR=$(dirname "$FIB_DASHBOARD_PATH")
cd "$FIB_DASHBOARD_DIR"
python fibonacci_dashboard_connector.py > "$PROJECT_ROOT/logs/fibonacci_dashboard.log" 2>&1 &
FIB_PID=$!
cd "$PROJECT_ROOT"
echo -e "${GREEN}✓ Started Fibonacci Dashboard Connector (PID: $FIB_PID)${RESET}"

# Start Live API Server in background
if [ -n "$LIVE_API_PATH" ]; then
    echo -e "${GREEN}Starting Live API Server...${RESET}"
    LIVE_API_DIR=$(dirname "$LIVE_API_PATH")
    cd "$LIVE_API_DIR"
    python live-api-server.py > "$PROJECT_ROOT/logs/live_api_server.log" 2>&1 &
    LIVE_API_PID=$!
    cd "$PROJECT_ROOT"
    echo -e "${GREEN}✓ Started Live API Server (PID: $LIVE_API_PID)${RESET}"
else
    echo -e "${RED}✗ Cannot start Live API Server - file not found${RESET}"
fi

# Print instructions
echo -e "\n${YELLOW}${BOLD}DASHBOARD COMPONENTS STARTED:${RESET}"
echo -e "${GREEN}Fibonacci Dashboard Connector running with PID:${RESET} $FIB_PID"
if [ -n "$LIVE_API_PID" ]; then
    echo -e "${GREEN}Live API Server running with PID:${RESET} $LIVE_API_PID"
fi

echo -e "\n${YELLOW}${BOLD}ACCESS POINTS:${RESET}"
echo -e "${GREEN}Fibonacci Dashboard:${RESET} View logs/fibonacci_dashboard.log"
if [ -n "$LIVE_API_PID" ]; then
    echo -e "${GREEN}Live API Server:${RESET} View logs/live_api_server.log"
fi

echo -e "\n${YELLOW}${BOLD}TO STOP COMPONENTS:${RESET}"
echo -e "${GREEN}Run:${RESET} kill $FIB_PID"
if [ -n "$LIVE_API_PID" ]; then
    echo -e "${GREEN}Run:${RESET} kill $LIVE_API_PID"
fi

echo -e "\n${BLUE}${BOLD}DEBUG MODE COMPLETE - COMPONENTS RUNNING IN BACKGROUND${RESET}" 