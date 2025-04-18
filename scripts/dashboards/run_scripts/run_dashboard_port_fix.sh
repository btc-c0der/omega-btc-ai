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

# Run OMEGA BTC AI with only dashboard components - Port Fix Version
# Starts only Fibonacci Dashboard Connector and Live API Server on alternate port

# Define Rasta colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'
BOLD='\033[1m'
BG_BLACK='\033[40m'

# Change to script directory
cd "$(dirname "$0")"
PROJECT_ROOT=$(pwd)

# Start with a nice banner
echo ""
echo -e "${BG_BLACK}${BOLD}${GREEN}🦁 🌿 🌈 ${YELLOW}======================================================${RED} 🔥 🌟 🦁${RESET}"
echo -e "${BG_BLACK}${BOLD}${RED}          ${GREEN}O${YELLOW}M${RED}E${GREEN}G${YELLOW}A ${RED}B${GREEN}T${YELLOW}C ${RED}A${GREEN}I ${YELLOW}- ${RED}D${GREEN}A${YELLOW}S${RED}H${GREEN}B${YELLOW}O${RED}A${GREEN}R${YELLOW}D ${RED}C${GREEN}O${YELLOW}M${RED}P${GREEN}O${YELLOW}N${RED}E${GREEN}N${YELLOW}T${RED}S ${GREEN}O${YELLOW}N${RED}L${GREEN}Y${YELLOW}          ${RESET}"
echo -e "${BG_BLACK}${BOLD}${GREEN}🦁 🌿 🌈 ${YELLOW}======================================================${RED} 🔥 🌟 🦁${RESET}"
echo ""

# Check if .env.local exists, create if not
if [ ! -f .env.local ]; then
    echo -e "${GREEN}🌿 Creating ${YELLOW}.env.local${GREEN} file for local development...${RESET}"
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
    echo -e "${YELLOW}🌟 ${GREEN}.env.local ${YELLOW}created successfully ${GREEN}🌟${RESET}"
fi

# Kill existing processes for clean restart
echo -e "${YELLOW}Checking for existing processes...${RESET}"
for proc in $(ps -ef | grep "fibonacci_dashboard_connector.py\|live-api-server.py" | grep -v grep | awk '{print $2}'); do
    echo -e "${YELLOW}Killing existing process ${proc}...${RESET}"
    kill $proc 2>/dev/null
done
# Wait for processes to end
sleep 2

# Display Rasta Lion ASCII Art
echo -e "${RED}                                 .;ldxkkkxd:.                             ${RESET}"
echo -e "${YELLOW}                              .;d0KXXXXXK0ko'                             ${RESET}"
echo -e "${GREEN}                            'ckKXNXK0KXXXNXKx;.                           ${RESET}"
echo -e "${RED}                           'dKXXX0o,...';oOXNXKo.                          ${RESET}"
echo -e "${YELLOW}                          ,kXXX0o.        .;xXXKo.                         ${RESET}"
echo -e "${GREEN}                         ;0XXKd.            'dXX0;                        ${RESET}"
echo -e "${RED}                        .xXXXO;               ,OXXx.                       ${RESET}"
echo -e "${YELLOW}                        ;KXXX0;                oXXXx.                      ${RESET}"
echo -e "${GREEN}                       .OXXXXk.                ;KXNk.                     ${RESET}"
echo -e "${RED}                       ,0XXXX0,                .kXXXx.                     ${RESET}"
echo -e "${YELLOW}                       :KXNXXX:                 ;KXXKc                      ${RESET}"
echo -e "${GREEN}                       ;KXXXXXo.                oXXXO'                     ${RESET}"
echo -e "${RED}                       ,0XXXXX0:.               cKXXKc                     ${RESET}"
echo -e "${YELLOW}                       :KXXXXNK:               ;0XXNk.                     ${RESET}"
echo -e "${GREEN}                       .OXXXXXNXo.            ;ONXXKc                      ${RESET}"
echo -e "${RED}                        :KXXXXXXXXOl;,,,,,:lxOKXXXKd.                      ${RESET}"
echo -e "${YELLOW}                         ;OXXXXXXXXXXXXXXXXXXXXX0:.                        ${RESET}"
echo -e "${GREEN}                          .:okKXXXXXXXXXXXXXKOo:.                          ${RESET}"
echo -e "${RED}                              .';:oxkkkxxo:,..                             ${RESET}"

echo -e ""
echo -e "${RED}🔥 ${YELLOW}STARTING ${GREEN}RASTA DASHBOARD ${YELLOW}COMPONENTS ${RED}🔥${RESET}"
echo -e "${GREEN}🦁 ${YELLOW}JAH BLESS ${GREEN}THE CODE! ${YELLOW}ONE LOVE! ${RED}ONE HEART! ${GREEN}ONE CODE! ${YELLOW}🦁${RESET}"
echo ""

# Create logs directory
mkdir -p logs

# Find path to fibonacci dashboard connector and live-api-server
FIB_DASHBOARD_PATH=$(find ./omega_ai -name "fibonacci_dashboard_connector.py" | head -1)
LIVE_API_PATH=$(find ./omega_ai -name "live-api-server.py" | head -1)

# Start components individually
# Start Fibonacci Dashboard Connector
if [ -n "$FIB_DASHBOARD_PATH" ]; then
    echo -e "${GREEN}🌿 Starting Fibonacci Dashboard Connector...${RESET}"
    FIB_DASHBOARD_DIR=$(dirname "$FIB_DASHBOARD_PATH")
    cd "$FIB_DASHBOARD_DIR"
    python fibonacci_dashboard_connector.py > "$PROJECT_ROOT/logs/fibonacci_dashboard.log" 2>&1 &
    FIB_PID=$!
    cd "$PROJECT_ROOT"
    echo -e "${GREEN}✅ Started Fibonacci Dashboard Connector (PID: $FIB_PID)${RESET}"
else
    echo -e "${RED}❌ Cannot find Fibonacci Dashboard Connector!${RESET}"
    exit 1
fi

# Start Live API Server with custom port
if [ -n "$LIVE_API_PATH" ]; then
    echo -e "${GREEN}🌿 Starting Live API Server on port 5050...${RESET}"
    LIVE_API_DIR=$(dirname "$LIVE_API_PATH")
    cd "$LIVE_API_DIR"
    
    # Create a temporary copy of the live-api-server with modified port
    cp live-api-server.py live-api-server-temp.py
    
    # Change port from 5000 to 5050
    sed -i '' 's/port=5000/port=5050/g' live-api-server-temp.py
    
    # Run the modified version
    python live-api-server-temp.py > "$PROJECT_ROOT/logs/live_api_server.log" 2>&1 &
    LIVE_API_PID=$!
    
    cd "$PROJECT_ROOT"
    echo -e "${GREEN}✅ Started Live API Server on port 5050 (PID: $LIVE_API_PID)${RESET}"
else
    echo -e "${YELLOW}⚠️ Live API Server not found, skipping${RESET}"
fi

# Print running components
echo -e "${GREEN}🌿 ${YELLOW}Dashboard components started ${GREEN}successfully ${RED}🔥${RESET}"
echo -e ""
echo -e "${YELLOW}📊 RUNNING COMPONENTS:${RESET}"
echo -e "${GREEN}➡️ Fibonacci Dashboard Connector (PID: $FIB_PID)${RESET}"
if [ -n "$LIVE_API_PID" ]; then
    echo -e "${GREEN}➡️ Live API Server (PID: $LIVE_API_PID)${RESET}"
fi

echo -e "\n${YELLOW}📝 LOGS:${RESET}"
echo -e "${GREEN}➡️ Fibonacci Dashboard: ${RESET}$PROJECT_ROOT/logs/fibonacci_dashboard.log"
if [ -n "$LIVE_API_PID" ]; then
    echo -e "${GREEN}➡️ Live API Server: ${RESET}$PROJECT_ROOT/logs/live_api_server.log"
fi

echo -e "\n${YELLOW}🌐 ACCESS POINTS:${RESET}"
echo -e "${GREEN}➡️ Live API Dashboard: ${RESET}http://localhost:5050/"

echo -e "\n${YELLOW}⚠️ TO STOP COMPONENTS:${RESET}"
echo -e "${GREEN}kill $FIB_PID${RESET}"
if [ -n "$LIVE_API_PID" ]; then
    echo -e "${GREEN}kill $LIVE_API_PID${RESET}"
fi

echo -e "\n${GREEN}🦁 ${YELLOW}JAH LOVE ${GREEN}GUIDE YOUR ${YELLOW}ANALYSIS! ${GREEN}🦁${RESET}" 