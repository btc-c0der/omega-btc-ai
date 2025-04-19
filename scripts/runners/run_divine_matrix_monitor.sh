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


# OMEGA BTC AI - Divine Matrix Monitor
# This script runs the divine Matrix monitor with test integration in a tmux session

# Terminal colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${MAGENTA}${BOLD}
╔════════════════════════════════════════════════════════════╗
║        OMEGA BTC AI - DIVINE MATRIX FUNKO MONITOR         ║
║           🧠 TEST INTEGRATION & MONITORING 🧠             ║
╚════════════════════════════════════════════════════════════╝${NC}"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}Error: tmux is not installed. Please install tmux to run monitors.${NC}"
    exit 1
fi

# Kill existing session if it exists
SESSION_NAME="divine-matrix"
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create new session
echo -e "${BLUE}Creating tmux session for divine Matrix monitor...${NC}"
tmux new-session -d -s $SESSION_NAME

# Set window names and split panes
tmux rename-window -t $SESSION_NAME:0 "MATRIX_MONITOR"

# Split window into 4 panes
tmux split-window -h -t $SESSION_NAME:0
tmux split-window -v -t $SESSION_NAME:0.0
tmux split-window -v -t $SESSION_NAME:0.1

# Set status bar colors and formatting
tmux set -g status-bg black
tmux set -g status-fg green
tmux set -g status-left "#[fg=green,bold][OMEGA BTC AI] #[fg=cyan]Divine Matrix #[fg=yellow]| "
tmux set -g status-right "#[fg=cyan]%H:%M:%S #[fg=yellow]| #[fg=green,bold]JAH BLESS! #[fg=default]"
tmux set -g status-left-length 50
tmux set -g status-right-length 50

# Configure each pane
# Pane 0: Test Runner
tmux send-keys -t $SESSION_NAME:0.0 "echo -e '${GREEN}Starting Divine Test Runner...${NC}'" C-m
tmux send-keys -t $SESSION_NAME:0.0 "python scripts/run_automated_tests.sh --all" C-m

# Pane 1: Test Results
tmux send-keys -t $SESSION_NAME:0.1 "echo -e '${YELLOW}Monitoring Test Results...${NC}'" C-m
tmux send-keys -t $SESSION_NAME:0.1 "tail -f divine_test_listener.log" C-m

# Pane 2: Service Health
tmux send-keys -t $SESSION_NAME:0.2 "echo -e '${BLUE}Monitoring Service Health...${NC}'" C-m
tmux send-keys -t $SESSION_NAME:0.2 "docker-compose -f orchestrator/docker-compose.monitoring.yml logs -f" C-m

# Pane 3: Redis Monitor
tmux send-keys -t $SESSION_NAME:0.3 "echo -e '${CYAN}Monitoring Redis...${NC}'" C-m
tmux send-keys -t $SESSION_NAME:0.3 "python scripts/redis_health_check.py" C-m

# Create a control panel window
tmux new-window -t $SESSION_NAME:1 -n "CONTROL"
tmux send-keys -t $SESSION_NAME:1 "echo -e '${MAGENTA}OMEGA BTC AI - Divine Control Panel${NC}'" C-m
tmux send-keys -t $SESSION_NAME:1 "echo -e '${CYAN}Press Ctrl+B 0 to return to monitors${NC}'" C-m
tmux send-keys -t $SESSION_NAME:1 "echo -e '${CYAN}Press Ctrl+B & to exit session${NC}'" C-m

# Return to the monitors window
tmux select-window -t $SESSION_NAME:0

# Display information about the session
echo -e "${GREEN}${BOLD}Divine Matrix Monitor started successfully!${NC}"
echo -e "${YELLOW}To detach from tmux: press Ctrl+B, then D${NC}"
echo -e "${CYAN}To navigate between panes: Ctrl+B, then arrow keys${NC}"
echo -e "${CYAN}To zoom/unzoom a pane: Ctrl+B, then Z${NC}"
echo -e "${MAGENTA}To access control panel: Ctrl+B, then 1${NC}"
echo -e "${BLUE}To return to monitors: Ctrl+B, then 0${NC}"
echo -e "${RED}To exit completely: Ctrl+B, then &${NC}"

# Attach to the session
sleep 2
tmux attach-session -t $SESSION_NAME 