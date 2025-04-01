#!/bin/bash
# OMEGA BTC AI - Dual Monitor (Entry & Exit Strategy)
# This script launches both the entry and exit monitors in a tmux session with split panes
# Author: OMEGA BTC AI Team
# Version: 1.0.0

# Default values
SESSION_NAME="omega-monitors"
INTERVAL=30                  # Refresh interval in seconds
MIN_CONFIDENCE=0.5           # Minimum confidence threshold
USE_MOCK=true                # Default to mock data
LAYOUT="horizontal"          # Default to horizontal split (can be "horizontal" or "vertical")

# Help text
show_help() {
  echo "OMEGA BTC AI - Dual Monitor Launcher (Entry & Exit Strategy)"
  echo ""
  echo "This script launches both the entry and exit strategy monitors in a tmux session."
  echo ""
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -h, --help               Show this help message"
  echo "  -s, --session NAME       tmux session name (default: omega-monitors)"
  echo "  -i, --interval SEC       Refresh interval in seconds (default: 30)"
  echo "  -c, --confidence FLOAT   Minimum confidence threshold (default: 0.5)"
  echo "  -m, --mock               Use mock data (default: true)"
  echo "  -r, --real               Use real BitGet market data instead of mock data"
  echo "  -v, --vertical           Use vertical split layout (default: horizontal)"
  echo ""
  echo "Examples:"
  echo "  $0 --interval 15 --confidence 0.6         # Run with mock data, 15s interval"
  echo "  $0 --real --session trading-live          # Run with real data, custom session name"
  echo "  $0 --vertical --interval 10              # Run with vertical split layout"
  echo ""
  echo "IMPORTANT: Without the --mock option (or with --real), both monitors connect to the"
  echo "BITGET MAINNET using credentials from your .env file."
  exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
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
      LAYOUT="vertical"
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
  echo "Error: tmux is not installed. Please install tmux to use this script."
  exit 1
fi

# Build commands for entry and exit monitors
ENTRY_CMD="./scripts/run_persona_entry_monitor.sh --interval $INTERVAL --min-confidence $MIN_CONFIDENCE"
EXIT_CMD="python scripts/run_persona_exit_monitor.py --interval $INTERVAL --min-persona-confidence $MIN_CONFIDENCE"

if [ "$USE_MOCK" = true ]; then
  ENTRY_CMD="$ENTRY_CMD --mock"
  EXIT_CMD="$EXIT_CMD --mock"
else
  # If not using mock data, warn user about connecting to MAINNET
  echo -e "\033[33m⚠️  WARNING: You are connecting to BITGET MAINNET! This is not a simulation. ⚠️\033[0m"
  echo -e "\033[33m   Use --mock if you want to run with simulated data.\033[0m"
  echo
  read -p "Do you want to continue connecting to MAINNET? (y/N): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled. Use --mock for simulation mode."
    exit 0
  fi
  echo "Proceeding with MAINNET connection..."
fi

# Function to start the dual monitor
run_dual_monitor() {
  # Check if session already exists
  if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session $SESSION_NAME already exists. Attaching..."
    tmux attach-session -t "$SESSION_NAME"
    exit 0
  fi

  # Create new tmux session with entry monitor
  echo "Creating new tmux session ($SESSION_NAME) with entry monitor..."
  tmux new-session -d -s "$SESSION_NAME" -n "Entry" "$ENTRY_CMD"
  
  # Wait briefly for first pane to initialize
  sleep 1
  
  # Create second window for exit monitor
  echo "Adding exit monitor..."
  
  if [ "$LAYOUT" = "vertical" ]; then
    # Create vertical split (side by side)
    tmux split-window -h -t "$SESSION_NAME:0" "$EXIT_CMD"
  else
    # Create horizontal split (one above the other)
    tmux split-window -v -t "$SESSION_NAME:0" "$EXIT_CMD" 
  fi
  
  # Set synchronize-panes off (so commands don't affect both panes)
  tmux set-option -t "$SESSION_NAME" synchronize-panes off
  
  # Add a third window with a shell for convenience
  tmux new-window -t "$SESSION_NAME:1" -n "Console" 
  
  # Return to first window with monitors
  tmux select-window -t "$SESSION_NAME:0"
  
  # Set up a message
  tmux display-message "OMEGA BTC AI - Entry & Exit Monitors Running"
  
  # Attach to the session
  echo "Starting dual monitors with refresh interval of $INTERVAL seconds"
  echo "Attaching to tmux session..."
  tmux attach-session -t "$SESSION_NAME"
}

# Run the dual monitor
run_dual_monitor 