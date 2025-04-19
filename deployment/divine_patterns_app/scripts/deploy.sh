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

"""
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""


# Divine Pattern Analyzer - Digital Ocean Deployment Script
# ========================================================
#
# This script deploys the Divine Pattern Analyzer to DigitalOcean
# Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Welcome message
echo -e "${CYAN}======================================================${NC}"
echo -e "${CYAN}      Divine Pattern Analyzer Deployment Script      ${NC}"
echo -e "${CYAN}======================================================${NC}"
echo ""

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}Error: doctl command is not installed.${NC}"
    echo -e "${YELLOW}Please install the DigitalOcean CLI tool:${NC}"
    echo "Visit: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if user is authenticated with DigitalOcean
echo -e "${BLUE}Checking DigitalOcean authentication...${NC}"
if ! doctl account get &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with DigitalOcean.${NC}"
    echo -e "${YELLOW}Please run:${NC} doctl auth init"
    exit 1
fi
echo -e "${GREEN}✅ Authenticated with DigitalOcean${NC}"

# Validate app.yaml exists
if [ ! -f "deployment/divine_patterns_app/app.yaml" ]; then
    echo -e "${RED}❌ Error: app.yaml not found at deployment/divine_patterns_app/app.yaml${NC}"
    exit 1
fi
echo -e "${GREEN}✅ app.yaml found${NC}"

# Deploy to DigitalOcean
echo -e "${GREEN}Deploying to DigitalOcean...${NC}"
echo -e "${YELLOW}This may take a few minutes.${NC}"

# Create the app using the app spec
APP_ID=$(doctl apps create --spec deployment/divine_patterns_app/app.yaml --format ID --no-header)

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Deployment failed.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Deployment started successfully!${NC}"
echo -e "${CYAN}You can monitor the deployment at: https://cloud.digitalocean.com/apps/$APP_ID${NC}"

# Get deployment URL
echo -e "${BLUE}Fetching deployment URL...${NC}"
sleep 10 # Give DO a moment to create the app

# Try to get the app URL
APP_URL=$(doctl apps get $APP_ID --format DefaultIngress --no-header)

if [ -n "$APP_URL" ] && [ "$APP_URL" != "null" ]; then
    echo -e "${GREEN}✅ Your Divine Pattern Analyzer will be available at:${NC}"
    echo -e "${CYAN}https://$APP_URL${NC}"
    
    echo -e "${YELLOW}API Endpoints:${NC}"
    echo -e "  * Health Check: ${CYAN}https://$APP_URL/health${NC}"
    echo -e "  * Sample Data: ${CYAN}https://$APP_URL/sample${NC}"
    echo -e "  * Analyze: ${CYAN}https://$APP_URL/analyze${NC} (POST)"
else
    echo -e "${YELLOW}App is being provisioned. Check the status later with:${NC}"
    echo -e "${CYAN}doctl apps get $APP_ID${NC}"
fi

echo -e "${GREEN}Deployment complete! 🚀${NC}" 