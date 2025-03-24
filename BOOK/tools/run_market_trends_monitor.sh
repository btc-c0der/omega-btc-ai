#!/bin/bash

# OMEGA BTC AI - Market Trends Monitor Runner
# This script runs the market trends monitor in a tmux session with fixed display mode

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "Error: tmux is not installed. Please install tmux first."
    exit 1
fi

# Set script variables
SESSION_NAME="omega-market-monitor"
WINDOW_NAME="market-trends"
PROJECT_ROOT=$(cd "$(dirname "$0")/../.." && pwd)
PYTHON_CMD="cd $PROJECT_ROOT && FIXED_DISPLAY=true python -m omega_ai.monitor.monitor_market_trends_fixed"

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create a new tmux session
tmux new-session -d -s $SESSION_NAME -n $WINDOW_NAME

# Set status bar colors and formatting
tmux set -g status-bg black
tmux set -g status-fg green
tmux set -g status-left "#[fg=green,bold][OMEGA BTC AI] #[fg=cyan]Market Monitor #[fg=yellow]| "
tmux set -g status-right "#[fg=cyan]%H:%M:%S #[fg=yellow]| #[fg=green,bold]FIXED DISPLAY MODE #[fg=default]"
tmux set -g status-left-length 50
tmux set -g status-right-length 50

# Configure window
tmux send-keys -t $SESSION_NAME:$WINDOW_NAME "$PYTHON_CMD" C-m

# Display information about the session
echo "====================================================="
echo "  OMEGA BTC AI - Market Trends Monitor"
echo "====================================================="
echo ""
echo "Started tmux session: $SESSION_NAME"
echo ""
echo "Commands:"
echo "  - Attach to session:     tmux attach -t $SESSION_NAME"
echo "  - Detach from session:   Ctrl+b, d"
echo "  - Kill session:          tmux kill-session -t $SESSION_NAME"
echo ""
echo "The monitor is now running in fixed display mode!"
echo "====================================================="

# Attach to the session
tmux attach -t $SESSION_NAME

# If we get here, the session has been detached
echo "Session detached. The monitor continues to run in the background."
echo "To reattach: tmux attach -t $SESSION_NAME" 