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

# OMEGA BTC AI - Combined Persona Monitors Launcher
# ==================================================
#
# This script launches both the Persona-Based Entry Monitor and the Persona-Based Exit Monitor
# in a tmux session with split panes.
#
# Author: OMEGA BTC AI Team
# Version: 1.0.0

# Default values
SESSION_NAME="omega-monitors"
INTERVAL=60
MIN_CONFIDENCE=0.5
USE_MOCK=true
VERTICAL_SPLIT=false  # Horizontal split by default

# Function to display help message
function show_help {
  echo "OMEGA BTC AI - Combined Persona Monitors Launcher"
  echo "=================================================="
  echo
  echo "Usage: $0 [OPTIONS]"
  echo
  echo "Options:"
  echo "  -h, --help             Show this help message"
  echo "  -s, --session NAME     tmux session name (default: omega-monitors)"
  echo "  -i, --interval SEC     Refresh interval in seconds (default: 60)"
  echo "  -c, --confidence FLOAT Minimum confidence threshold (default: 0.5)"
  echo "  -m, --mock             Use mock data instead of real BitGet data (default: true)"
  echo "  -r, --real             Use real BitGet data (requires API credentials in .env)"
  echo "  -v, --vertical         Use vertical split instead of horizontal"
  echo
  echo "Examples:"
  echo "  $0 --interval 30 --session trading-view"
  echo "  $0 --real --confidence 0.6 --vertical"
  echo
  echo "Note: When using real data, BitGet API credentials must be set in your .env file."
  exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      ;;
    -s|--session)
      SESSION_NAME="$2"
      shift 2
      ;;
    -i|--interval)
      INTERVAL="$2"
      shift 2
      ;;
    -c|--confidence)
      MIN_CONFIDENCE="$2"
      shift 2
      ;;
    -m|--mock)
      USE_MOCK=true
      shift
      ;;
    -r|--real)
      USE_MOCK=false
      shift
      ;;
    -v|--vertical)
      VERTICAL_SPLIT=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      ;;
  esac
done

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
  echo "Error: tmux is not installed. Please install it to use this script."
  exit 1
fi

# Check if .env exists when using real data
if [ "$USE_MOCK" = false ]; then
  if [ ! -f ".env" ]; then
    echo "Error: .env file not found but required for real BitGet data."
    echo "Please create a .env file with your BitGet API credentials."
    exit 1
  fi
  
  # Check for BitGet credentials in .env
  if ! grep -q "BITGET_API_KEY" .env || ! grep -q "BITGET_SECRET_KEY" .env || ! grep -q "BITGET_PASSPHRASE" .env; then
    echo "Error: BitGet API credentials not found in .env file."
    echo "Please set BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE in your .env file."
    exit 1
  fi
fi

# Build command options
COMMON_OPTS="--interval $INTERVAL --min-confidence $MIN_CONFIDENCE"
if [ "$USE_MOCK" = true ]; then
  COMMON_OPTS="$COMMON_OPTS --mock"
fi

# Entry monitor command
ENTRY_CMD="python scripts/persona_entry_strategy.py --continuous $COMMON_OPTS"

# Exit monitor command
EXIT_CMD="python scripts/run_persona_exit_monitor.py $COMMON_OPTS"

# Check if session exists and kill it
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "Session $SESSION_NAME already exists. Killing it..."
  tmux kill-session -t "$SESSION_NAME"
fi

# Create new tmux session
echo "Creating new tmux session: $SESSION_NAME"
tmux new-session -d -s "$SESSION_NAME" -n "monitors"

# First pane: Entry monitor
tmux send-keys -t "$SESSION_NAME:monitors.0" "clear; echo 'Starting OMEGA BTC AI Persona Entry Monitor...'; sleep 1; $ENTRY_CMD" C-m

# Split pane based on orientation preference
if [ "$VERTICAL_SPLIT" = true ]; then
  tmux split-window -v -t "$SESSION_NAME:monitors.0"
else
  tmux split-window -h -t "$SESSION_NAME:monitors.0"
fi

# Second pane: Exit monitor
tmux send-keys -t "$SESSION_NAME:monitors.1" "clear; echo 'Starting OMEGA BTC AI Persona Exit Monitor...'; sleep 1; $EXIT_CMD" C-m

# Set status bar configuration
tmux set-option -t "$SESSION_NAME" status-style "bg=black,fg=green"
tmux set-option -t "$SESSION_NAME" status-left "#[fg=green,bold]OMEGA BTC AI #[fg=yellow][$SESSION_NAME] "
tmux set-option -t "$SESSION_NAME" status-right "#[fg=cyan]%H:%M:%S"
tmux set-option -t "$SESSION_NAME" window-status-current-style "bg=green,fg=black"

# Set window title
tmux rename-window -t "$SESSION_NAME:monitors" "OMEGA MONITORS"

# Display info about the session
echo "Starting combined monitors with:"
echo "  - Session name: $SESSION_NAME"
echo "  - Refresh interval: ${INTERVAL}s"
echo "  - Minimum confidence: $MIN_CONFIDENCE"
echo "  - Data source: $([ "$USE_MOCK" = true ] && echo "Mock data" || echo "Real BitGet data")"
echo "  - Split: $([ "$VERTICAL_SPLIT" = true ] && echo "Vertical" || echo "Horizontal")"
echo

# Attach to the session
echo "Attaching to tmux session..."
tmux attach-session -t "$SESSION_NAME" 