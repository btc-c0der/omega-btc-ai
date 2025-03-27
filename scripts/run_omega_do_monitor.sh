#!/bin/bash

# 🔱 OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor 🔱
# =============================================
#
# A sacred shell wrapper for the OMEGA BTC AI Digital Ocean Monitor

# ANSI color codes for divine styling
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}${BOLD}Error: Python 3 is not installed.${RESET}"
    echo -e "${YELLOW}Please install Python 3 to use the OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor.${RESET}"
    exit 1
fi

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}${BOLD}Error: doctl is not installed.${RESET}"
    echo -e "${YELLOW}Please install the Digital Ocean CLI (doctl) to use this monitor.${RESET}"
    echo -e "${CYAN}Visit: https://docs.digitalocean.com/reference/doctl/how-to/install/${RESET}"
    exit 1
fi

# Check doctl authentication
if ! doctl account get &> /dev/null; then
    echo -e "${RED}${BOLD}Error: doctl is not authenticated.${RESET}"
    echo -e "${YELLOW}Please authenticate with Digital Ocean first:${RESET}"
    echo -e "${CYAN}doctl auth init${RESET}"
    exit 1
fi

# Configuration
export OMEGA_DO_APP_ID=${OMEGA_DO_APP_ID:-"f129574c-0fcd-4a97-93bb-32618cbccae2"}
export OMEGA_DO_APP_URL=${OMEGA_DO_APP_URL:-"https://omega-btc-live-feed-v2-f129574c-0fcd-4a97-93bb-32618cbccae2.ondigitalocean.app"}

# Install required packages if needed
echo -e "${CYAN}Checking required Python packages...${RESET}"
python3 -c "import sys; r = [__import__(p) for p in ['argparse', 'urllib', 'json']]" 2>/dev/null || {
    echo -e "${YELLOW}Installing required packages...${RESET}"
    pip install argparse urllib3 requests
}

# Announce the divine monitoring
echo -e "\n${MAGENTA}${BOLD}🔱 OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor 🔱${RESET}"
echo -e "${MAGENTA}==============================================${RESET}"
echo -e "${CYAN}Monitoring Digital Ocean App: ${YELLOW}${OMEGA_DO_APP_ID}${RESET}"
echo -e "${CYAN}App URL: ${YELLOW}${OMEGA_DO_APP_URL}${RESET}"
echo -e "${MAGENTA}==============================================${RESET}\n"

# Run the monitor script with the provided command
MONITOR_SCRIPT="$SCRIPT_DIR/omega_do_monitor.py"

# Check if the monitor script exists
if [ ! -f "$MONITOR_SCRIPT" ]; then
    echo -e "${RED}Error: Monitor script not found at $MONITOR_SCRIPT${RESET}"
    exit 1
fi

# Make the monitor script executable
chmod +x "$MONITOR_SCRIPT"

# Run the monitor with the provided command
python3 "$MONITOR_SCRIPT" "$@"

# Exit with the script's exit code
exit $? 