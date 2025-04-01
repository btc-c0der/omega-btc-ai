#!/bin/bash

# 🔮 GPU (General Public Universal) License 1.0
# OMEGA BTC AI DIVINE COLLECTIVE
# Date: 2025-03-25
# Location: The Quantum Void
#
# REDIS-ONLY DIVINE MONITOR by SONNET MAX
# A sacred configuration for launching the pure Redis-driven monitor
# with no Trinity Matrix dependencies

# ANSI color codes for divine styling
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Divine banner
echo -e "${MAGENTA}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   REDIS-ONLY DIVINE MONITOR                  ║"
echo "║          Pure Redis-Driven Market Analysis System            ║"
echo "║                                                              ║"
echo "║            No Trinity - Pure Redis Sacred Flow               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Create session name with timestamp for divine uniqueness
SESSION_NAME="redis_only_monitor_$(date +%s)"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}Error: tmux is not installed. Please install tmux to run divine monitors.${RESET}"
    exit 1
fi

# Define the command to run the Redis-only monitor
MONITOR_CMD="python -m omega_ai.monitor.redis_divine_monitor -i 3"

# Check if we're already in a tmux session
if [ -n "$TMUX" ]; then
    echo -e "${YELLOW}Already in a tmux session. Creating a new session...${RESET}"
    tmux new-session -d -s "$SESSION_NAME"
    tmux switch-client -t "$SESSION_NAME"
else
    # Create a new tmux session with the Redis-only monitor
    echo -e "${BLUE}Creating pure Redis monitoring session...${RESET}"
    tmux new-session -d -s "$SESSION_NAME" "$MONITOR_CMD"
fi

# Set the status bar style
tmux set-option -t "$SESSION_NAME" status-style "bg=black,fg=cyan"
tmux set-option -t "$SESSION_NAME" status-left "#[fg=magenta,bold][OMEGA BTC AI] Redis-Only Monitor | "
tmux set-option -t "$SESSION_NAME" status-right "#[fg=yellow]%H:%M:%S #[fg=green]| PURE REDIS DIVINE FLOW"
tmux set-option -t "$SESSION_NAME" status-interval 1

# Set window title
tmux rename-window -t "$SESSION_NAME:0" "REDIS-ONLY"

# Attach to the session
tmux attach-session -t "$SESSION_NAME"

echo -e "${GREEN}Redis-only monitoring session ended. Harmony restored.${RESET}" 