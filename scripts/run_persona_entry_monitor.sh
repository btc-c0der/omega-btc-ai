#!/bin/bash
# OMEGA BTC AI - Persona-Based Entry Strategy Monitor
# =================================================
#
# This script runs the Persona-Based Entry Strategy Monitor with specified parameters.
# It can run in continuous mode, with mock data, or with real BitGet market data.
#
# Author: OMEGA BTC AI Team
# Version: 1.0.1 - Mainnet Integration

# Default values
INTERVAL=60
USE_TMUX=false
SESSION_NAME="entry-monitor"
LOG_FILE="persona_entry_monitor.log"
USE_MOCK=false
USE_COLOR=true
MIN_CONFIDENCE=0.5
# BitGet API credentials (default to empty)
BITGET_API_KEY=""
BITGET_SECRET_KEY=""
BITGET_PASSPHRASE=""

# Function to display help message
function show_help {
  echo "Usage: $0 [OPTIONS]"
  echo
  echo "Options:"
  echo "  -h, --help             Show this help message"
  echo "  -i, --interval SECONDS Interval between checks in seconds (default: 60)"
  echo "  -t, --tmux             Run in tmux session"
  echo "  -s, --session NAME     tmux session name (default: entry-monitor)"
  echo "  -n, --no-color         Disable colored output"
  echo "  -l, --log FILE         Log file path (default: persona_entry_monitor.log)"
  echo "  -m, --mock             Use mock market data instead of real BitGet data"
  echo "  -c, --confidence FLOAT Minimum confidence threshold (default: 0.5)"
  echo "  -k, --api-key KEY      BitGet API key"
  echo "  -a, --api-secret SEC   BitGet API secret"
  echo "  -p, --passphrase PASS  BitGet API passphrase"
  echo
  echo "Example:"
  echo "  $0 --interval 30 --tmux --session my-monitor"
  echo "  $0 --mock --interval 120"
  echo "  $0 --api-key YOUR_KEY --api-secret YOUR_SECRET --passphrase YOUR_PASS"
  echo
  echo "IMPORTANT: Without the --mock option, the script connects to the BITGET MAINNET"
  echo "using either the provided credentials or those in your .env file."
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      exit 0
      ;;
    -i|--interval)
      INTERVAL="$2"
      shift 2
      ;;
    -t|--tmux)
      USE_TMUX=true
      shift
      ;;
    -s|--session)
      SESSION_NAME="$2"
      shift 2
      ;;
    -n|--no-color)
      USE_COLOR=false
      shift
      ;;
    -l|--log)
      LOG_FILE="$2"
      shift 2
      ;;
    -m|--mock)
      USE_MOCK=true
      shift
      ;;
    -c|--confidence)
      MIN_CONFIDENCE="$2"
      shift 2
      ;;
    -k|--api-key)
      BITGET_API_KEY="$2"
      shift 2
      ;;
    -a|--api-secret)
      BITGET_SECRET_KEY="$2"
      shift 2
      ;;
    -p|--passphrase)
      BITGET_PASSPHRASE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Check if .env file exists and load credentials if not provided via CLI
if [ -f ".env" ] && [ -z "$BITGET_API_KEY" ] && [ -z "$BITGET_SECRET_KEY" ] && [ -z "$BITGET_PASSPHRASE" ]; then
  echo "Loading BitGet credentials from .env file..."
  # Extract values from .env file using grep and cut
  BITGET_API_KEY=$(grep "BITGET_API_KEY" .env | cut -d '=' -f2)
  BITGET_SECRET_KEY=$(grep "BITGET_SECRET_KEY" .env | cut -d '=' -f2)
  BITGET_PASSPHRASE=$(grep "BITGET_PASSPHRASE" .env | cut -d '=' -f2)
fi

# Build command
CMD="python scripts/persona_entry_strategy.py --continuous"

if [ "$USE_COLOR" = false ]; then
  CMD="$CMD --no-color"
fi

if [ "$USE_MOCK" = true ]; then
  CMD="$CMD --mock"
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

CMD="$CMD --interval $INTERVAL --min-confidence $MIN_CONFIDENCE"

# Set BitGet API environment variables if provided
if [ -n "$BITGET_API_KEY" ]; then
  export BITGET_API_KEY="$BITGET_API_KEY"
  echo "Using BitGet API key: ${BITGET_API_KEY:0:5}..."
fi

if [ -n "$BITGET_SECRET_KEY" ]; then
  export BITGET_SECRET_KEY="$BITGET_SECRET_KEY"
  echo "Using BitGet API secret: ${BITGET_SECRET_KEY:0:5}..."
fi

if [ -n "$BITGET_PASSPHRASE" ]; then
  export BITGET_PASSPHRASE="$BITGET_PASSPHRASE"
  echo "Using BitGet API passphrase: ${BITGET_PASSPHRASE:0:3}..."
fi

# Function to run in tmux
function run_in_tmux {
  if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session $SESSION_NAME already exists. Attaching..."
    tmux attach-session -t "$SESSION_NAME"
  else
    echo "Creating new tmux session: $SESSION_NAME"
    tmux new-session -d -s "$SESSION_NAME" "$CMD | tee $LOG_FILE"
    tmux attach-session -t "$SESSION_NAME"
  fi
}

# Run command
if [ "$USE_TMUX" = true ]; then
  run_in_tmux
else
  echo "Running persona entry monitor with interval: ${INTERVAL}s"
  if [ "$USE_MOCK" = true ]; then
    echo "Using mock market data"
  else
    echo "Using REAL BitGet MAINNET market data"
  fi
  
  if [ "$USE_COLOR" = false ]; then
    echo "Color output disabled"
  fi
  
  echo "Minimum confidence threshold: $MIN_CONFIDENCE"
  echo "Log file: $LOG_FILE"
  echo
  
  # Run in background and log to file
  nohup $CMD > "$LOG_FILE" 2>&1 &
  PID=$!
  echo "Entry monitor running in background with PID: $PID"
  echo "To view logs: tail -f $LOG_FILE"
  echo "To stop: kill $PID"
fi 