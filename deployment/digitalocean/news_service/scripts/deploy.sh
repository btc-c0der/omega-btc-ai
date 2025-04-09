#!/bin/bash
"""
✨ GBU License Notice ✨
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


# OMEGA BTC AI - Deploy BTC Live Feed v3
# ======================================
# This script deploys BTC Live Feed v3 to DigitalOcean

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# App ID
APP_ID="fbf696ef-8240-4fc8-a1cb-9d03b00197b9"

# Logo display
echo -e "${MAGENTA}"
echo "🔱 OMEGA BTC AI - Deploy BTC Live Feed v3 🔱"
echo -e "${RESET}"

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}Error: doctl is not installed. Please install it first.${RESET}"
    echo "Visit: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if doctl is authenticated
if ! doctl account get &> /dev/null; then
    echo -e "${RED}Error: doctl is not authenticated. Please authenticate first.${RESET}"
    echo "Run: doctl auth init"
    exit 1
fi

# Check if app.yaml exists
if [ ! -f "config/app.yaml" ]; then
    echo -e "${RED}Error: config/app.yaml not found.${RESET}"
    exit 1
fi

# Load environment variables
echo -e "${YELLOW}Loading environment variables...${RESET}"
if [ -f ".env" ]; then
    source .env
else
    echo -e "${RED}Error: .env file not found.${RESET}"
    exit 1
fi

# Check required environment variables
required_vars=(
    "REDIS_HOST"
    "REDIS_PORT"
    "REDIS_PASSWORD"
    "REDIS_USERNAME"
    "FAILOVER_REDIS_HOST"
    "FAILOVER_REDIS_PORT"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}Error: $var is not set in .env file${RESET}"
        exit 1
    fi
done

# Deploy to DigitalOcean
echo -e "${GREEN}Deploying to DigitalOcean...${RESET}"
echo -e "${YELLOW}Updating app with ID: $APP_ID${RESET}"
doctl apps update $APP_ID --spec config/app.yaml

echo -e "${GREEN}Deployment update initiated!${RESET}"
echo -e "${CYAN}App ID: $APP_ID${RESET}"
echo -e "${CYAN}You can monitor the deployment at: https://cloud.digitalocean.com/apps/$APP_ID${RESET}"

# Start monitoring
echo -e "${YELLOW}Starting monitoring...${RESET}"
python ../../scripts/monitor_btc_feed_v3.py --host localhost --port 8080 --refresh 5 