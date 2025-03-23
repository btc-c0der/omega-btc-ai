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
    echo -e "${YELLOW}Error: tmux is not installed. Please install tmux to run this script.${NC}"
    exit 1
fi

# Create a new tmux session named "omega-monitors"
echo -e "${CYAN}Starting tmux session...${NC}"

# Kill any existing session with the same name
tmux kill-session -t omega-monitors 2>/dev/null

# Create a new session with RastaBitgetMonitor
tmux new-session -d -s omega-monitors -n "monitors" "python simple_bitget_positions.py --interval 3; bash"

# Split the window horizontally and run Trap Probability Meter in the bottom pane
# Add a more compact version with minimal output
tmux split-window -v -t omega-monitors "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"

# Adjust pane sizes to give maximum space to RastaBitgetMonitor (85%) 
# and just enough for the trap meter (15%)
tmux resize-pane -t omega-monitors:monitors.0 -y 85%

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