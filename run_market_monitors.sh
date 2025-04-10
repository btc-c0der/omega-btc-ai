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


# OMEGA BTC AI - Market Trend Monitors Runner
# This script runs both the original and AI-enhanced market trend monitors in tmux sessions

# Terminal colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${MAGENTA}${BOLD}
╔════════════════════════════════════════════════════════════╗
║        OMEGA BTC AI - DIVINE MARKET TREND MONITORS         ║
║           🧠 FIBONACCI PATTERN RECOGNITION 🧠             ║
╚════════════════════════════════════════════════════════════╝${NC}"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}Error: tmux is not installed. Please install tmux to run monitors.${NC}"
    exit 1
fi

# Kill existing tmux sessions if they exist
tmux kill-session -t "market_monitors" &> /dev/null

# Create new tmux session
echo -e "${BLUE}Creating tmux session for market monitors...${NC}"
tmux new-session -d -s "market_monitors"

# Split window horizontally 50/50
tmux split-window -h -t "market_monitors"

# Set window names
tmux rename-window -t "market_monitors" "MARKET_TREND_MONITORS"

# Start original market trend monitor in the left pane
echo -e "${YELLOW}Starting original market trend monitor...${NC}"
tmux send-keys -t "market_monitors:0.0" "cd $(pwd) && python -m omega_ai.monitor.monitor_market_trends_fixed" C-m

# Start AI-enhanced market trend monitor in the right pane
echo -e "${CYAN}Starting AI-enhanced market trend monitor...${NC}"
tmux send-keys -t "market_monitors:0.1" "cd $(pwd) && python -m omega_ai.monitor.market_trends_monitor_ai" C-m

# Attach to the tmux session
echo -e "${GREEN}${BOLD}Monitors started successfully! Attaching to tmux session...${NC}"
echo -e "${YELLOW}Press Ctrl+B then D to detach from the session${NC}"
sleep 2
tmux attach-session -t "market_monitors" 