#!/bin/bash
# OMEGA BTC AI - Grid Surveillance System
# Creates a divine monitoring grid using tmux for real-time market surveillance
# Layout:
#  ___________________________
# |      |         |         |
# | Fib  |  Trap   | Live   |
# | Dash | Probab. | API    |
# |      |  Meter  |        |
# |------|---------|---------|
# | Div. |         |        |
# | Dash |         |        |
# |______|_________|_________|
# |      Redis Monitor       |
# |_________________________|

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
REGGAE_DASHBOARD_URL=http://localhost:$FRONTEND_PORT_1
API_BASE_URL=http://localhost:$BACKEND_PORT_1
WS_URL=ws://localhost:8765

# Development Mode
NODE_ENV=development
LOG_LEVEL=DEBUG

# Local Storage Paths
LOG_DIR=./logs
DATA_DIR=./data

# Dynamic Ports
FRONTEND_PORT=$FRONTEND_PORT_1
BACKEND_PORT=$BACKEND_PORT_1
DASHBOARD_PORT=$FRONTEND_PORT_1
API_PORT=$BACKEND_PORT_1
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

# Function to find an available port
find_available_port() {
    local start_port=$1
    local max_attempts=100
    local port=$start_port

    while [ $port -lt $((start_port + max_attempts)) ]; do
        if ! lsof -i :$port > /dev/null 2>&1; then
            echo $port
            return 0
        fi
        port=$((port + 1))
    done
    
    echo -e "${RED}❌ No available ports found in range $start_port-$((start_port + max_attempts))${RESET}" >&2
    return 1
}

# Find available ports for each component
echo -e "${YELLOW}🔍 Finding available ports...${RESET}"

FRONTEND_PORT_1=$(find_available_port 7000)
BACKEND_PORT_1=$(find_available_port 8400)
FRONTEND_PORT_2=$(find_available_port 7100)
BACKEND_PORT_2=$(find_available_port 8500)
REDIS_MONITOR_PORT=$(find_available_port 6380)
DIVINE_DASHBOARD_PORT=$(find_available_port 5051)
TRAP_METER_PORT=$(find_available_port 5052)

echo -e "${GREEN}✨ Using ports:${RESET}"
echo -e "${YELLOW}Live Traders Dashboard:${RESET}"
echo -e "  Frontend: ${GREEN}$FRONTEND_PORT_1${RESET}"
echo -e "  Backend:  ${GREEN}$BACKEND_PORT_1${RESET}"
echo -e "${YELLOW}Orders Dashboard:${RESET}"
echo -e "  Frontend: ${GREEN}$FRONTEND_PORT_2${RESET}"
echo -e "  Backend:  ${GREEN}$BACKEND_PORT_2${RESET}"
echo -e "${YELLOW}Redis Monitor:${RESET}"
echo -e "  Port:     ${GREEN}$REDIS_MONITOR_PORT${RESET}"
echo -e "${YELLOW}Divine Dashboard:${RESET}"
echo -e "  Port:     ${GREEN}$DIVINE_DASHBOARD_PORT${RESET}"
echo -e "${YELLOW}Trap Probability Meter:${RESET}"
echo -e "  Port:     ${GREEN}$TRAP_METER_PORT${RESET}"
echo ""

# Find absolute paths to components
FIB_DASHBOARD_PATH="$PROJECT_ROOT/omega_ai/visualizer/start_with_live_traders.py"
LIVE_API_PATH="$PROJECT_ROOT/omega_ai/visualizer/start_orders_dashboard.py"
REDIS_MONITOR_PATH="$PROJECT_ROOT/omega_ai/tools/redis_monitor.py"
DIVINE_DASHBOARD_PATH="$PROJECT_ROOT/sandbox/divine/start_divine_dashboard.py"
TRAP_METER_PATH="$PROJECT_ROOT/omega_ai/tools/trap_probability_meter.py"

# Verify paths exist
if [ ! -f "$FIB_DASHBOARD_PATH" ]; then
    echo -e "${RED}❌ Cannot find Fibonacci Dashboard at: $FIB_DASHBOARD_PATH${RESET}"
    exit 1
fi

if [ ! -f "$LIVE_API_PATH" ]; then
    echo -e "${RED}❌ Cannot find Live API Server at: $LIVE_API_PATH${RESET}"
    exit 1
fi

if [ ! -f "$REDIS_MONITOR_PATH" ]; then
    echo -e "${YELLOW}⚠️  Redis Monitor not found at: $REDIS_MONITOR_PATH${RESET}"
fi

if [ ! -f "$DIVINE_DASHBOARD_PATH" ]; then
    echo -e "${YELLOW}⚠️  Divine Dashboard not found at: $DIVINE_DASHBOARD_PATH${RESET}"
fi

if [ ! -f "$TRAP_METER_PATH" ]; then
    echo -e "${YELLOW}⚠️  Trap Probability Meter not found at: $TRAP_METER_PATH${RESET}"
fi

# Prepare tmux session
SESSION_NAME="omega-monitor"

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION_NAME -n "OMEGA BTC AI Monitor"

# Configure tmux panes
# First split horizontally for the footer (Redis Monitor)
tmux split-window -v -t $SESSION_NAME:0.0 -p 20

# Split the top section into three columns (30-40-30 split)
tmux split-window -h -t $SESSION_NAME:0.0 -p 70  # Split for center and right
tmux split-window -h -t $SESSION_NAME:0.0 -p 43  # Split left and center

# Split the bottom-left for Divine Dashboard
tmux split-window -v -t $SESSION_NAME:0.0 -p 50

# Set working directory for all panes
tmux send-keys -t $SESSION_NAME:0.0 "cd \"$PROJECT_ROOT\"" C-m  # Top-left: Fibonacci Dashboard
tmux send-keys -t $SESSION_NAME:0.1 "cd \"$PROJECT_ROOT\"" C-m  # Top-center: Trap Probability
tmux send-keys -t $SESSION_NAME:0.2 "cd \"$PROJECT_ROOT\"" C-m  # Top-right: Live API Server
tmux send-keys -t $SESSION_NAME:0.3 "cd \"$PROJECT_ROOT\"" C-m  # Bottom-left: Divine Dashboard
tmux send-keys -t $SESSION_NAME:0.4 "cd \"$PROJECT_ROOT\"" C-m  # Footer: Redis Monitor

# Set environment variables for dynamically assigned ports
tmux send-keys -t $SESSION_NAME:0.0 "export FRONTEND_PORT=$FRONTEND_PORT_1 && export BACKEND_PORT=$BACKEND_PORT_1 && export DASHBOARD_PORT=$FRONTEND_PORT_1 && export API_PORT=$BACKEND_PORT_1" C-m
tmux send-keys -t $SESSION_NAME:0.1 "export TRAP_METER_PORT=$TRAP_METER_PORT" C-m
tmux send-keys -t $SESSION_NAME:0.2 "export FRONTEND_PORT=$FRONTEND_PORT_2 && export BACKEND_PORT=$BACKEND_PORT_2 && export DASHBOARD_PORT=$FRONTEND_PORT_2 && export API_PORT=$BACKEND_PORT_2" C-m
tmux send-keys -t $SESSION_NAME:0.3 "export DIVINE_PORT=$DIVINE_DASHBOARD_PORT" C-m
tmux send-keys -t $SESSION_NAME:0.4 "export REDIS_MONITOR_PORT=$REDIS_MONITOR_PORT" C-m

# Set titles with colors and port info
tmux send-keys -t $SESSION_NAME:0.0 "echo -e '${GREEN}🌿 Fibonacci Dashboard ${YELLOW}(Frontend: $FRONTEND_PORT_1) ${GREEN}🌿'" C-m
tmux send-keys -t $SESSION_NAME:0.1 "echo -e '${RED}🎯 Trap Probability Meter ${CYAN}(Port: $TRAP_METER_PORT) ${RED}🎯'" C-m
tmux send-keys -t $SESSION_NAME:0.2 "echo -e '${YELLOW}🔥 Live API ${RED}(Backend: $BACKEND_PORT_2) ${YELLOW}🔥'" C-m
tmux send-keys -t $SESSION_NAME:0.3 "echo -e '${MAGENTA}🎭 Divine Dashboard ${CYAN}(Port: $DIVINE_DASHBOARD_PORT) ${MAGENTA}🎭'" C-m
tmux send-keys -t $SESSION_NAME:0.4 "echo -e '${BLUE}⚡ Redis Monitor ${CYAN}(Port: $REDIS_MONITOR_PORT) ${BLUE}⚡'" C-m

# Start components with proper paths
tmux send-keys -t $SESSION_NAME:0.0 "python \"$FIB_DASHBOARD_PATH\"" C-m

if [ -f "$TRAP_METER_PATH" ]; then
    tmux send-keys -t $SESSION_NAME:0.1 "python \"$TRAP_METER_PATH\" --interval 3 --verbose" C-m
else
    tmux send-keys -t $SESSION_NAME:0.1 "echo -e '${RED}Trap Probability Meter not available${RESET}'" C-m
fi

tmux send-keys -t $SESSION_NAME:0.2 "python \"$LIVE_API_PATH\"" C-m

if [ -f "$DIVINE_DASHBOARD_PATH" ]; then
    tmux send-keys -t $SESSION_NAME:0.3 "python \"$DIVINE_DASHBOARD_PATH\" --port $DIVINE_DASHBOARD_PORT" C-m
else
    tmux send-keys -t $SESSION_NAME:0.3 "echo -e '${RED}Divine Dashboard not available${RESET}'" C-m
fi

if [ -f "$REDIS_MONITOR_PATH" ]; then
    tmux send-keys -t $SESSION_NAME:0.4 "python \"$REDIS_MONITOR_PATH\"" C-m
else
    tmux send-keys -t $SESSION_NAME:0.4 "echo -e '${RED}Redis Monitor not available${RESET}'" C-m
fi

echo -e "${GREEN}✅ Started dashboard components in tmux session '${YELLOW}$SESSION_NAME${GREEN}'${RESET}"

# Add helpful instructions
echo -e "${YELLOW}📊 MONITOR ATTACHED!${RESET}"
echo -e "${GREEN}➡️ Press ${YELLOW}Ctrl+B, then arrow keys${GREEN} to navigate between panes${RESET}"
echo -e "${GREEN}➡️ Press ${YELLOW}Ctrl+B, then d${GREEN} to detach from the session (components will keep running)${RESET}"
echo -e "${GREEN}➡️ Type ${YELLOW}tmux attach -t $SESSION_NAME${GREEN} to reattach to the session later${RESET}"
echo -e "${GREEN}➡️ Type ${YELLOW}tmux kill-session -t $SESSION_NAME${GREEN} to terminate all components${RESET}"

echo -e "\n${GREEN}🦁 ${YELLOW}JAH LOVE ${GREEN}GUIDE YOUR ${YELLOW}ANALYSIS! ${GREEN}🦁${RESET}"

# Attach to the tmux session
tmux attach-session -t $SESSION_NAME 