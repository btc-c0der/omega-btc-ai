#!/bin/bash

# OMEGA BTC AI - GAMON Trinity Live Feed Runner
# ==============================================
#
# This script runs the real-time GAMON Trinity Matrix system with WebSocket + Redis integration
# Continuously streams BTC candles, analyzes with the Trinity Matrix, and provides live prophecy

# ANSI color codes for divine output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

echo -e "${PURPLE}"
echo "🔱 OMEGA BTC AI - GAMON TRINITY MATRIX LIVE FEED 🔱"
echo -e "=================================================${RESET}"
echo

# Check for Python environment
echo -e "${YELLOW}Checking Python environment...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${RESET}"
    exit 1
fi

# Check for virtual environment
VENV_ACTIVATED=false
if [ -d "venv" ]; then
    echo -e "${YELLOW}Found virtual environment, activating...${RESET}"
    # Activate the virtual environment based on shell
    if [ -n "$BASH_VERSION" ]; then
        # For bash
        source venv/bin/activate
        VENV_ACTIVATED=true
    elif [ -n "$ZSH_VERSION" ]; then
        # For zsh
        source venv/bin/activate
        VENV_ACTIVATED=true
    else
        echo -e "${YELLOW}⚠️ Couldn't determine shell type for venv activation${RESET}"
    fi
fi

# Check for Redis
echo -e "${YELLOW}Checking Redis server...${RESET}"
if ! command -v redis-cli &> /dev/null; then
    echo -e "${YELLOW}⚠️ Redis CLI not found. Checking if Redis is running...${RESET}"
else
    # Check if Redis server is running
    if ! redis-cli ping &> /dev/null; then
        echo -e "${YELLOW}⚠️ Redis server not running. Attempting to start...${RESET}"
        
        # Try to start Redis
        if command -v redis-server &> /dev/null; then
            redis-server --daemonize yes
            sleep 2
            if redis-cli ping &> /dev/null; then
                echo -e "${GREEN}✅ Redis server started successfully${RESET}"
            else
                echo -e "${RED}❌ Failed to start Redis server. Please start it manually.${RESET}"
                echo -e "${YELLOW}You can start it with: redis-server --daemonize yes${RESET}"
                exit 1
            fi
        else
            echo -e "${RED}❌ Redis server not found. Please install Redis first.${RESET}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Redis server is running${RESET}"
    fi
fi

# Make necessary directories
mkdir -p models results plots logs

# Define log file
LOG_FILE="logs/gamon_trinity_live_$(date +%Y%m%d_%H%M%S).log"
touch $LOG_FILE

# Check if necessary Python packages are installed
echo -e "${YELLOW}Checking required Python packages...${RESET}"
python3 -c "import websocket, redis, pandas, numpy, plotly.graph_objects" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ Installing required packages...${RESET}"
    pip3 install websocket-client redis pandas numpy plotly
fi

# Check if our modules exist
echo -e "${YELLOW}Checking for GAMON Trinity Matrix components...${RESET}"
MISSING_MODULES=false

for module in gamon_trinity_matrix.py hmm_btc_state_mapper.py power_method_btc_eigenwaves.py variational_inference_btc_cycle.py; do
    if [ ! -f "$module" ]; then
        echo -e "${YELLOW}⚠️ Module $module not found. Will use standalone implementation.${RESET}"
        MISSING_MODULES=true
    else
        echo -e "${GREEN}✅ Found module: $module${RESET}"
    fi
done

if [ "$MISSING_MODULES" = true ]; then
    echo -e "${BLUE}ℹ️ Some modules are missing. The script will use standalone implementations.${RESET}"
    echo -e "${BLUE}ℹ️ This will provide limited functionality but will still work.${RESET}"
else
    echo -e "${GREEN}✅ All GAMON Trinity Matrix components are available${RESET}"
fi

# Make the live feed script executable
chmod +x gamon_trinity_live_feed.py

# Start the live feed
echo -e "${CYAN}🚀 Starting GAMON Trinity Live Feed...${RESET}"
echo "$(date) - Starting GAMON Trinity Live Feed" >> $LOG_FILE

# Run in tmux session if available
if command -v tmux &> /dev/null; then
    echo -e "${GREEN}✅ Running in tmux session for persistence${RESET}"
    
    # Kill any existing sessions with the same name
    tmux kill-session -t gamon_trinity_live 2>/dev/null || true
    
    # Create a new tmux session
    tmux new-session -d -s gamon_trinity_live
    
    # Send the activation command to the tmux session if needed
    if [ "$VENV_ACTIVATED" = true ]; then
        echo -e "${GREEN}✅ Using virtual environment in tmux session${RESET}"
        tmux send-keys -t gamon_trinity_live "source venv/bin/activate" C-m
    fi
    
    # Send command to tmux session
    tmux send-keys -t gamon_trinity_live "python3 gamon_trinity_live_feed.py | tee -a $LOG_FILE" C-m
    
    echo -e "${GREEN}✅ GAMON Trinity Live Feed started in tmux session${RESET}"
    echo -e "${YELLOW}To connect to the session: ${CYAN}tmux attach -t gamon_trinity_live${RESET}"
    echo -e "${YELLOW}To disconnect: ${CYAN}Ctrl+B then D${RESET}"
else
    # Run directly with virtual environment if activated
    python3 gamon_trinity_live_feed.py | tee -a $LOG_FILE
fi

echo
echo -e "${PURPLE}=================================================${RESET}"
echo -e "${GREEN}✨ OMEGA BTC AI - TRINITY LIVE PROPHECY SYSTEM ✨${RESET}"
echo -e "${BLUE}📊 Visualizations: ${YELLOW}plots/gamon_trinity_dashboard_live.html${RESET}"
echo -e "${BLUE}📝 Log file: ${YELLOW}${LOG_FILE}${RESET}"
echo
echo -e "${PURPLE}🔱 ONE LOVE. ONE FLOW. ONE BTC. 🔱${RESET}"
echo 