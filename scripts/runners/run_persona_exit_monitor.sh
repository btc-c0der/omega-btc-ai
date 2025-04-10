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

# OMEGA BTC AI - Persona Exit Monitor Launcher
# This script launches the persona-based exit strategy monitor in a tmux session

# Default values
INTERVAL=60  # Refresh interval in seconds
SESSION_NAME="persona-monitor"
MIN_CONFIDENCE=0.5
USE_REAL_POSITIONS=true
LOG_FILE="persona_exit_monitor.log"
USE_TMUX=false  # Default to running without tmux

# Help text
show_help() {
  echo "OMEGA BTC AI - Persona Exit Monitor Launcher"
  echo ""
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -i, --interval SEC       Refresh interval in seconds (default: 60)"
  echo "  -s, --session NAME       tmux session name (default: persona-monitor)"
  echo "  -c, --confidence FLOAT   Minimum confidence threshold (default: 0.5)"
  echo "  -m, --mock               Use mock positions instead of real BitGet positions"
  echo "  -l, --log FILE           Log file path (default: persona_exit_monitor.log)"
  echo "  -t, --tmux               Run in a tmux session (default: run directly)"
  echo "  -h, --help               Show this help message"
  echo ""
  echo "Examples:"
  echo "  $0 --interval 30 --confidence 0.6            # Run directly without tmux"
  echo "  $0 --interval 30 --confidence 0.6 --tmux     # Run in a tmux session"
  exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -i|--interval)
      INTERVAL="$2"
      shift 2
      ;;
    -s|--session)
      SESSION_NAME="$2"
      shift 2
      ;;
    -c|--confidence)
      MIN_CONFIDENCE="$2"
      shift 2
      ;;
    -m|--mock)
      USE_REAL_POSITIONS=false
      shift
      ;;
    -l|--log)
      LOG_FILE="$2"
      shift 2
      ;;
    -t|--tmux)
      USE_TMUX=true
      shift
      ;;
    -h|--help)
      show_help
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      ;;
  esac
done

# Check if script exists
SCRIPT_PATH="$(dirname "$0")/simple_persona_exit_demo.py"
if [ ! -f "$SCRIPT_PATH" ]; then
  echo "Error: Could not find $SCRIPT_PATH"
  exit 1
fi

# Build command with options
CMD="python3 $SCRIPT_PATH"

if [ "$USE_REAL_POSITIONS" = true ]; then
  CMD="$CMD --use-real-positions"
fi

CMD="$CMD --min-confidence $MIN_CONFIDENCE --continuous"

# Function to run the monitor script directly
run_direct() {
  echo "Starting Persona Exit Monitor with refresh interval of $INTERVAL seconds"
  echo "Press Ctrl+C to stop"
  
  while true; do
    clear
    echo "OMEGA BTC AI - Persona Exit Monitor"
    echo "Running continuously. Press Ctrl+C to stop."
    echo "Refreshing every $INTERVAL seconds"
    echo "========================================"
    echo ""
    
    $CMD
    
    echo ""
    echo "Next update in $INTERVAL seconds..."
    sleep $INTERVAL
  done
}

# Function to run in tmux
run_tmux() {
  # Check if tmux is installed
  if ! command -v tmux &> /dev/null; then
    echo "Error: tmux is not installed. Please install it or run without --tmux."
    exit 1
  fi
  
  # Create continuous monitor script
  MONITOR_SCRIPT=$(cat << EOF
#!/bin/bash
while true; do
  clear
  echo "OMEGA BTC AI - Persona Exit Monitor"
  echo "Running continuously. Press Ctrl+C to stop."
  echo "Refreshing every $INTERVAL seconds"
  echo "========================================"
  echo ""
  
  $CMD
  
  echo ""
  echo "Next update in $INTERVAL seconds..."
  sleep $INTERVAL
done
EOF
)

  # Check if session exists
  if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session $SESSION_NAME already exists. Attaching..."
    tmux attach-session -t "$SESSION_NAME"
    exit 0
  fi

  # Create new tmux session
  echo "Creating new tmux session: $SESSION_NAME"
  tmux new-session -d -s "$SESSION_NAME"

  # Send command to tmux session
  tmux send-keys -t "$SESSION_NAME" "$MONITOR_SCRIPT" C-m

  # Attach to the session
  echo "Starting Persona Exit Monitor with refresh interval of $INTERVAL seconds"
  echo "Attaching to tmux session..."
  tmux attach-session -t "$SESSION_NAME"
}

# Run either in tmux or directly based on option
if [ "$USE_TMUX" = true ]; then
  run_tmux
else
  run_direct
fi 