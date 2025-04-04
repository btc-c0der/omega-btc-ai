#!/bin/bash
# Simple shell script to run CyBer1t4L QA Bot locally

# Default values
MODE="full"
NO_DISCORD=""
THRESHOLD=80
MODULES=""

# Display help
show_help() {
  echo "CyBer1t4L QA Bot Runner"
  echo ""
  echo "Usage: ./run_cyber1t4l.sh [options]"
  echo ""
  echo "Options:"
  echo "  -m, --mode MODE      Operation mode: full, coverage, generate, monitor (default: full)"
  echo "  -n, --no-discord     Run without Discord integration"
  echo "  -t, --threshold NUM  Coverage threshold percentage (default: 80)"
  echo "  -s, --modules MODS   Comma-separated list of modules for test generation"
  echo "  -h, --help           Display this help message"
  echo ""
  echo "Examples:"
  echo "  ./run_cyber1t4l.sh --mode coverage --no-discord"
  echo "  ./run_cyber1t4l.sh --mode generate --modules src/omega_bot_farm/trading/bitget_positions_info.py"
  echo ""
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -m|--mode)
      MODE="$2"
      shift 2
      ;;
    -n|--no-discord)
      NO_DISCORD="--no-discord"
      shift
      ;;
    -t|--threshold)
      THRESHOLD="$2"
      shift 2
      ;;
    -s|--modules)
      MODULES="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Verify the mode is valid
if [[ ! "$MODE" =~ ^(full|coverage|generate|monitor)$ ]]; then
  echo "Error: Invalid mode '$MODE'"
  show_help
  exit 1
fi

# Convert comma-separated modules to space-separated for command line
if [ -n "$MODULES" ]; then
  MODULES_ARG="--modules ${MODULES//,/ }"
else
  MODULES_ARG=""
fi

# Make sure we're in the project root directory
cd "$(dirname "$0")/../../.." || { echo "Error: Could not navigate to project root"; exit 1; }

# Make sure the runner script is executable
chmod +x src/omega_bot_farm/qa/run_cyber1t4l_locally.py

# Run the bot
echo "Starting CyBer1t4L QA Bot in $MODE mode..."
echo ""

python -m src.omega_bot_farm.qa.run_cyber1t4l_locally \
  --mode "$MODE" \
  --threshold "$THRESHOLD" \
  $NO_DISCORD \
  $MODULES_ARG

exit_code=$?

if [ $exit_code -eq 0 ]; then
  echo ""
  echo "CyBer1t4L QA Bot completed successfully"
else
  echo ""
  echo "CyBer1t4L QA Bot exited with error code $exit_code"
fi

exit $exit_code 