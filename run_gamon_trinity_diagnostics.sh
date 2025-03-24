#!/bin/bash

# OMEGA BTC AI - GAMON Trinity Live Feed Diagnostics
# =================================================
#
# This script runs the real-time GAMON Trinity Matrix system in diagnostic mode
# showing all output directly to the console

# ANSI color codes for divine output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

echo -e "${PURPLE}"
echo "🔱 OMEGA BTC AI - GAMON TRINITY MATRIX DIAGNOSTICS 🔱"
echo -e "==================================================${RESET}"
echo

# Check for Python environment
echo -e "${YELLOW}Checking Python environment...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${RESET}"
    exit 1
fi

# Make sure the script is executable
chmod +x gamon_trinity_live_feed.py

# Run the script with traceback to see any errors
echo -e "${CYAN}🚀 Starting GAMON Trinity Live Feed in diagnostic mode...${RESET}"

# Enable Python traceback
export PYTHONFAULTHANDLER=1
export PYTHONTRACEMALLOC=1 

# Run with full error output
python3 -u gamon_trinity_live_feed.py

echo
echo -e "${PURPLE}==================================================${RESET}"
echo -e "${GREEN}✨ DIAGNOSTICS COMPLETE ✨${RESET}"
echo 