#!/bin/bash

# OMEGA BTC AI Runner Script
# This script starts the OMEGA BTC AI system with the specified mode

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Display banner
echo -e "${GREEN}"
echo "  ___  __  __ _____ ____    _      ____ _____ ____      _    ___ "
echo " / _ \|  \/  | ____/ ___|  / \    | __ )_   _/ ___|    / \  |_ _|"
echo "| | | | |\/| |  _|| |  _  / _ \   |  _ \ | || |       / _ \  | | "
echo "| |_| | |  | | |__| |_| |/ ___ \  | |_) || || |___   / ___ \ | | "
echo " \___/|_|  |_|_____\____/_/   \_\ |____/ |_| \____| /_/   \_\___|"
echo -e "${NC}"

# Function to display usage
display_usage() {
    echo "Usage: $0 [mode] [options]"
    echo "Modes:"
    echo "  full       - Start all services (default)"
    echo "  trading    - Start only trading services"
    echo "  monitoring - Start only monitoring services"
    echo "  dashboard  - Start only dashboard"
    echo "Options:"
    echo "  --testnet  - Use testnet instead of mainnet"
    echo "  --help     - Display this help message"
}

# Default mode
MODE="full"
TESTNET=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        full|trading|monitoring|dashboard)
            MODE="$1"
            shift
            ;;
        --testnet)
            TESTNET="--testnet"
            shift
            ;;
        --help)
            display_usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            display_usage
            exit 1
            ;;
    esac
done

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${RED}Redis is not running. Starting Redis...${NC}"
    redis-server --daemonize yes
    sleep 2
fi

# Run the OMEGA BTC AI system
echo -e "${GREEN}Starting OMEGA BTC AI in $MODE mode...${NC}"
python -m omega_ai.omega_runner --mode $MODE $TESTNET

# Deactivate virtual environment if it was activated
if [ -d "venv" ]; then
    deactivate
fi

# If the script exits with an error, show the logs
if [ $? -ne 0 ]; then
    echo "Error: OMEGA BTC AI failed to start properly"
    echo "Checking logs..."
    tail -n 50 omega_runner.log
    tail -n 50 omega_service.log
fi