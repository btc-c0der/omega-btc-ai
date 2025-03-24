#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Print banner
echo -e "${MAGENTA}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                 OMEGA BTC AI - MONITOR SUITE                    ║" 
echo "║                  RastaBitget + Trap Monitor                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if tmux is available
if ! command -v tmux &> /dev/null; then
    echo -e "${YELLOW}Error: tmux is not installed. Please install tmux to use this script.${NC}"
    exit 1
fi

# Default split mode (will be overridden by .env if available)
SPLIT_MODE="vertical"

# Source settings from .env file if it exists
if [ -f ".env" ]; then
    echo -e "${CYAN}Loading configuration from .env file...${NC}"
    # Extract SPLIT_MODE value from .env file
    ENV_SPLIT_MODE=$(grep "^SPLIT_MODE=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'")
    if [ -n "$ENV_SPLIT_MODE" ]; then
        SPLIT_MODE="$ENV_SPLIT_MODE"
        echo -e "${CYAN}Using SPLIT_MODE=$SPLIT_MODE from .env${NC}"
    else
        echo -e "${CYAN}SPLIT_MODE not found in .env, using default: $SPLIT_MODE${NC}"
    fi
else
    echo -e "${YELLOW}No .env file found, using default configuration${NC}"
fi

# Create a new tmux session named "omega-monitors"
echo -e "${CYAN}Starting tmux session...${NC}"

# Kill any existing session with the same name
tmux kill-session -t omega-monitors 2>/dev/null

# Create a new session with RastaBitgetMonitor
tmux new-session -d -s omega-monitors -n "monitors" "python simple_bitget_positions.py --interval 3; bash"

# Use SPLIT_MODE to determine the split type
if [ "$SPLIT_MODE" = "vertical" ]; then
    echo -e "${CYAN}Using vertical split layout${NC}"
    tmux split-window -v -t omega-monitors "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
    # Adjust pane sizes for vertical split (top/bottom)
    tmux resize-pane -t omega-monitors:monitors.0 -y 65%
else
    echo -e "${CYAN}Using horizontal split layout${NC}"
    tmux split-window -h -t omega-monitors "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
    # Adjust pane sizes for horizontal split (side by side)
    tmux resize-pane -t omega-monitors:monitors.0 -x 55%
fi

# Set tmux styling options for clear separation
tmux set-option -t omega-monitors pane-border-style "fg=magenta"
tmux set-option -t omega-monitors pane-active-border-style "fg=cyan,bold"
tmux set-option -t omega-monitors status-style "bg=black,fg=green"
tmux set-option -t omega-monitors status-right "#[fg=cyan]#(date '+%H:%M') #[fg=yellow]OMEGA BTC AI"

# Add a message to instruct on how to exit
tmux send-keys -t omega-monitors:monitors.0 "echo -e '\n${GREEN}Press Ctrl+B then & to exit the tmux session${NC}'" C-m

# Attach to the session
echo -e "${GREEN}Starting monitors. To detach from tmux: press Ctrl+B, then D${NC}"
echo -e "${YELLOW}To exit completely: press Ctrl+B, then &${NC}"
sleep 2
tmux attach -t omega-monitors 