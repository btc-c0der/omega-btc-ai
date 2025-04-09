#!/bin/bash
# OMEGA BTC AI - Dashboard Monitor
# Starts dashboard components in tmux panes for real-time monitoring

# Define Rasta colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
RESET='\033[0m'
BOLD='\033[1m'
BG_BLACK='\033[40m'

# Change to script directory
cd "$(dirname "$0")"
PROJECT_ROOT=$(pwd)

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}❌ tmux is required but not installed.${RESET}"
    echo -e "${YELLOW}Please install tmux:${RESET}"
    echo -e "  macOS: ${GREEN}brew install tmux${RESET}"
    echo -e "  Ubuntu/Debian: ${GREEN}sudo apt install tmux${RESET}"
    exit 1
fi

# Start with a nice banner
echo ""
echo -e "${BG_BLACK}${BOLD}${GREEN}🦁 🌿 🌈 ${YELLOW}======================================================${RED} 🔥 🌟 🦁${RESET}"
echo -e "${BG_BLACK}${BOLD}${RED}          ${GREEN}O${YELLOW}M${RED}E${GREEN}G${YELLOW}A ${RED}B${GREEN}T${YELLOW}C ${RED}A${GREEN}I ${YELLOW}- ${RED}D${GREEN}A${YELLOW}S${RED}H${GREEN}B${YELLOW}O${RED}A${GREEN}R${YELLOW}D ${RED}M${GREEN}O${YELLOW}N${RED}I${GREEN}T${YELLOW}O${RED}R ${GREEN}P${YELLOW}A${RED}N${GREEN}E${YELLOW}L          ${RESET}"
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
echo -e "${RED}🔥 ${YELLOW}LAUNCHING ${GREEN}OMEGA BTC AI ${YELLOW}DASHBOARD MONITOR ${RED}🔥${RESET}"
echo -e "${GREEN}🦁 ${YELLOW}JAH BLESS ${GREEN}THE CODE! ${YELLOW}ONE LOVE! ${RED}ONE HEART! ${GREEN}ONE CODE! ${YELLOW}🦁${RESET}"
echo ""

# Create logs directory
mkdir -p logs

# Find path to fibonacci dashboard connector and live-api-server
FIB_DASHBOARD_PATH=$(find ./omega_ai -name "fibonacci_dashboard_connector.py" | head -1)
LIVE_API_PATH=$(find ./omega_ai -name "live-api-server.py" | head -1)

# Also try to find the Redis monitor if available
REDIS_MONITOR_PATH=$(find . -name "redis_monitor_server.py" -o -name "redis_monitor_server_optimized.py" | head -1)

# Prepare tmux session
SESSION_NAME="omega-monitor"

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION_NAME -n "OMEGA BTC AI Monitor"

# Configure tmux panes and run commands
if [ -n "$FIB_DASHBOARD_PATH" ] && [ -n "$LIVE_API_PATH" ]; then
    # Two components - split screen horizontally
    tmux split-window -h -t $SESSION_NAME
    
    # If we have Redis monitor, split one pane vertically
    if [ -n "$REDIS_MONITOR_PATH" ]; then
        tmux split-window -v -t $SESSION_NAME:0.1
    fi
    
    # Set titles and colors
    tmux send-keys -t $SESSION_NAME:0.0 "echo -e '${GREEN}🌿 Fibonacci Dashboard Connector ${YELLOW}🌿'" C-m
    tmux send-keys -t $SESSION_NAME:0.1 "echo -e '${YELLOW}🔥 Live API Server ${RED}🔥'" C-m
    
    if [ -n "$REDIS_MONITOR_PATH" ]; then
        tmux send-keys -t $SESSION_NAME:0.2 "echo -e '${BLUE}⚡ Redis Monitor ${CYAN}⚡'" C-m
    fi
    
    # Start components in their panes
    tmux send-keys -t $SESSION_NAME:0.0 "cd \"$(dirname \"$FIB_DASHBOARD_PATH\")\" && python fibonacci_dashboard_connector.py" C-m
    tmux send-keys -t $SESSION_NAME:0.1 "cd \"$(dirname \"$LIVE_API_PATH\")\" && python live-api-server.py" C-m
    
    if [ -n "$REDIS_MONITOR_PATH" ]; then
        tmux send-keys -t $SESSION_NAME:0.2 "cd \"$(dirname \"$REDIS_MONITOR_PATH\")\" && python \"$(basename \"$REDIS_MONITOR_PATH\")\"" C-m
    fi
    
    echo -e "${GREEN}✅ Started dashboard components in tmux session '${YELLOW}$SESSION_NAME${GREEN}'${RESET}"
else
    echo -e "${RED}❌ Cannot find required dashboard components!${RESET}"
    tmux kill-session -t $SESSION_NAME
    exit 1
fi

# Add helpful instructions
echo -e "${YELLOW}📊 MONITOR ATTACHED!${RESET}"
echo -e "${GREEN}➡️ Press ${YELLOW}Ctrl+B, then arrow keys${GREEN} to navigate between panes${RESET}"
echo -e "${GREEN}➡️ Press ${YELLOW}Ctrl+B, then d${GREEN} to detach from the session (components will keep running)${RESET}"
echo -e "${GREEN}➡️ Type ${YELLOW}tmux attach -t $SESSION_NAME${GREEN} to reattach to the session later${RESET}"
echo -e "${GREEN}➡️ Type ${YELLOW}tmux kill-session -t $SESSION_NAME${GREEN} to terminate all components${RESET}"

echo -e "\n${GREEN}🦁 ${YELLOW}JAH LOVE ${GREEN}GUIDE YOUR ${YELLOW}ANALYSIS! ${GREEN}🦁${RESET}"

# Attach to the tmux session
tmux attach-session -t $SESSION_NAME 