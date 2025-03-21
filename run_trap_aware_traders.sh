#!/bin/bash

# OMEGA BTC AI - Trap-Aware Dual Position Traders Runner
# This script runs the trap-aware dual position traders with proper environment settings.

# Default settings
USE_COLORS=true
DEBUG=false
REDIS_HOST=localhost
REDIS_PORT=6379

# Initialize trading parameters with defaults
SYMBOL="BTCUSDT"
LONG_CAPITAL="150.0"
SHORT_CAPITAL="200.0"
LONG_LEVERAGE="5"
SHORT_LEVERAGE="5"
TRAP_PROB_THRESHOLD="0.6"
TRAP_ALERT_THRESHOLD="0.7"
MIN_FREE_BALANCE="750.0"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-color)
      USE_COLORS=false
      shift
      ;;
    --debug)
      DEBUG=true
      shift
      ;;
    --redis-host=*)
      REDIS_HOST="${1#*=}"
      shift
      ;;
    --redis-port=*)
      REDIS_PORT="${1#*=}"
      shift
      ;;
    *)
      # Save all other arguments to pass to the Python script
      EXTRA_ARGS="$EXTRA_ARGS $1"
      shift
      ;;
  esac
done

# Set environment variables
export REDIS_HOST=$REDIS_HOST
export REDIS_PORT=$REDIS_PORT
export FORCE_COLOR=1  # Force color output in Python

# Initialize status variables
TRAP_STATUS="INITIALIZING"
TRAP_PROBABILITY="0.0%"
DETECTED_TRAP="None"
TRADER_STATUS="INITIALIZING"

# Function for colored or plain echo based on settings
colored_echo() {
  if $USE_COLORS; then
    printf "%b\n" "$1"
  else
    # Strip ANSI color codes
    echo "$1" | sed 's/\x1b\[[0-9;]*m//g'
  fi
}

# Function to draw a progress bar
draw_progress_bar() {
  local value=$1
  local width=${2:-50}
  local char_filled=${3:-"█"}
  local char_empty=${4:-"░"}
  
  # Calculate filled part
  local filled=$(printf "%.0f" $(echo "$value * $width" | bc))
  
  # Ensure filled is within bounds
  if [ "$filled" -gt "$width" ]; then
    filled=$width
  fi
  if [ "$filled" -lt 0 ]; then
    filled=0
  fi
  
  # Calculate empty part
  local empty=$((width - filled))
  
  # Build progress bar
  local bar=""
  for ((i=0; i<filled; i++)); do
    bar="${bar}${char_filled}"
  done
  for ((i=0; i<empty; i++)); do
    bar="${bar}${char_empty}"
  done
  
  echo "$bar"
}

# Function to get probability color
get_probability_color() {
  local value=$1
  
  # Convert from string to numeric if needed
  value=$(echo "$value" | sed 's/%//')
  
  if (( $(echo "$value < 30" | bc -l) )); then
    echo "\e[1;32m"  # Green
  elif (( $(echo "$value < 60" | bc -l) )); then
    echo "\e[1;33m"  # Yellow
  elif (( $(echo "$value < 80" | bc -l) )); then
    echo "\e[1;35m"  # Magenta
  else
    echo "\e[1;31m"  # Red
  fi
}

# Function to get status color
get_status_color() {
  local status=$1
  
  case "$status" in
    *INITIALIZING*)
      echo "\e[1;36m"  # Cyan
      ;;
    *RUNNING*)
      echo "\e[1;32m"  # Green
      ;;
    *MONITORING*)
      echo "\e[1;32m"  # Green
      ;;
    *WAITING*)
      echo "\e[1;33m"  # Yellow
      ;;
    *TRADING*)
      echo "\e[1;32m"  # Green
      ;;
    *ALERT*)
      echo "\e[1;31m"  # Red
      ;;
    *CAUTION*)
      echo "\e[1;35m"  # Magenta
      ;;
    *WARNING*)
      echo "\e[1;33m"  # Yellow
      ;;
    *ERROR*)
      echo "\e[1;31m"  # Red
      ;;
    *)
      echo "\e[1;37m"  # White (default)
      ;;
  esac
}

# Function to get trap type icon
get_trap_icon() {
  local trap_type=$1
  
  case "$trap_type" in
    *LIQUIDITY_GRAB*)
      echo "💰"
      ;;
    *STOP_HUNT*)
      echo "🎯"
      ;;
    *BULL_TRAP*)
      echo "🐂"
      ;;
    *BEAR_TRAP*)
      echo "🐻"
      ;;
    *FAKE_PUMP*)
      echo "🚀"
      ;;
    *FAKE_DUMP*)
      echo "📉"
      ;;
    *POTENTIAL*)
      echo "⚠️"
      ;;
    *FADING*)
      echo "🔅"
      ;;
    *None*)
      echo "✅"
      ;;
    *)
      echo "❓"
      ;;
  esac
}

# Parse command line arguments to extract trading parameters
parse_trading_parameters() {
  local args="$EXTRA_ARGS"
  
  # Extract symbol
  if [[ "$args" =~ --symbol[[:space:]]+([A-Z0-9]+) ]]; then
    SYMBOL="${BASH_REMATCH[1]}"
  fi
  
  # Extract long capital
  if [[ "$args" =~ --long-capital[[:space:]]+([0-9.]+) ]]; then
    LONG_CAPITAL="${BASH_REMATCH[1]}"
  fi
  
  # Extract short capital
  if [[ "$args" =~ --short-capital[[:space:]]+([0-9.]+) ]]; then
    SHORT_CAPITAL="${BASH_REMATCH[1]}"
  fi
  
  # Extract long leverage
  if [[ "$args" =~ --long-leverage[[:space:]]+([0-9]+) ]]; then
    LONG_LEVERAGE="${BASH_REMATCH[1]}"
  fi
  
  # Extract short leverage
  if [[ "$args" =~ --short-leverage[[:space:]]+([0-9]+) ]]; then
    SHORT_LEVERAGE="${BASH_REMATCH[1]}"
  fi
  
  # Extract trap probability threshold
  if [[ "$args" =~ --trap-probability-threshold[[:space:]]+([0-9.]+) ]]; then
    TRAP_PROB_THRESHOLD="${BASH_REMATCH[1]}"
  fi
  
  # Extract trap alert threshold
  if [[ "$args" =~ --trap-alert-threshold[[:space:]]+([0-9.]+) ]]; then
    TRAP_ALERT_THRESHOLD="${BASH_REMATCH[1]}"
  fi
  
  # Extract min free balance
  if [[ "$args" =~ --min-free-balance[[:space:]]+([0-9.]+) ]]; then
    MIN_FREE_BALANCE="${BASH_REMATCH[1]}"
  fi
  
  # Output the args for debugging if in debug mode
  if $DEBUG; then
    echo "Parsed trading parameters:"
    echo "  SYMBOL = $SYMBOL"
    echo "  LONG_CAPITAL = $LONG_CAPITAL"
    echo "  SHORT_CAPITAL = $SHORT_CAPITAL"
    echo "  LONG_LEVERAGE = $LONG_LEVERAGE"
    echo "  SHORT_LEVERAGE = $SHORT_LEVERAGE"
    echo "  TRAP_PROB_THRESHOLD = $TRAP_PROB_THRESHOLD"
    echo "  TRAP_ALERT_THRESHOLD = $TRAP_ALERT_THRESHOLD"
    echo "  MIN_FREE_BALANCE = $MIN_FREE_BALANCE"
  fi
}

# Parse any command-line arguments that affect trader parameters
parse_trading_parameters

# Function to clear screen and display header
display_header() {
  # Get color for probability
  local prob_color=$(get_probability_color "$TRAP_PROBABILITY")
  
  # Convert probability to numeric value for progress bar
  local prob_value=$(echo "$TRAP_PROBABILITY" | sed 's/%//' | awk '{print $1/100}')
  
  # Generate progress bar
  local progress_bar=$(draw_progress_bar "$prob_value" 50)
  
  # Get status color
  local status_color=$(get_status_color "$TRADER_STATUS")
  
  # Get trap icon
  local trap_icon=$(get_trap_icon "$DETECTED_TRAP")
  
  clear
  if $USE_COLORS; then
    colored_echo "\e[1;36m===========================================================\e[0m"
    colored_echo "\e[1;36m= OMEGA BTC AI - Trap-Aware Dual Position Traders Runner =\e[0m"
    colored_echo "\e[1;36m===========================================================\e[0m"
    colored_echo "\e[1;36mEnvironment:\e[0m"
    colored_echo "  \e[1;36mREDIS_HOST=\e[0m$REDIS_HOST"
    colored_echo "  \e[1;36mREDIS_PORT=\e[0m$REDIS_PORT"
    colored_echo ""
    colored_echo "\e[1;36mTrading Parameters:\e[0m"
    colored_echo "  \e[1;36mSymbol: \e[0m$SYMBOL"
    colored_echo "  \e[1;36mCapital: \e[0mLong=$LONG_CAPITAL USDT, Short=$SHORT_CAPITAL USDT"
    colored_echo "  \e[1;36mLeverage: \e[0mLong=${LONG_LEVERAGE}x, Short=${SHORT_LEVERAGE}x"
    colored_echo "  \e[1;36mTrap Thresholds: \e[0mProb=${TRAP_PROB_THRESHOLD}, Alert=${TRAP_ALERT_THRESHOLD}"
    colored_echo "  \e[1;36mMin Free Balance: \e[0m$MIN_FREE_BALANCE USDT"
    colored_echo ""
    colored_echo "\e[1;36mSystem Status:\e[0m"
    colored_echo "  \e[1;36mTrap Probability Meter: \e[1;32mRUNNING\e[0m (PID: $TRAP_METER_PID)"
    colored_echo "  \e[1;36mDual Position Traders: ${status_color}$TRADER_STATUS\e[0m"
    colored_echo ""
    colored_echo "\e[1;36mMarket Condition:\e[0m"
    colored_echo "  \e[1;36mTrap Probability: ${prob_color}${progress_bar}\e[0m ${prob_color}${TRAP_PROBABILITY}\e[0m"
    colored_echo "  \e[1;36mDetected Trap: \e[1;33m$trap_icon $DETECTED_TRAP\e[0m"
    colored_echo "\e[1;36m===========================================================\e[0m"
    colored_echo ""
    colored_echo "\e[1;36mLog output appears below (press CTRL+C to stop):\e[0m"
    colored_echo "\e[1;36m-----------------------------------------------------------\e[0m"
  else
    echo "==========================================================="
    echo "= OMEGA BTC AI - Trap-Aware Dual Position Traders Runner ="
    echo "==========================================================="
    echo "Environment:"
    echo "  REDIS_HOST=$REDIS_HOST"
    echo "  REDIS_PORT=$REDIS_PORT"
    echo ""
    echo "Trading Parameters:"
    echo "  Symbol: $SYMBOL"
    echo "  Capital: Long=$LONG_CAPITAL USDT, Short=$SHORT_CAPITAL USDT"
    echo "  Leverage: Long=${LONG_LEVERAGE}x, Short=${SHORT_LEVERAGE}x"
    echo "  Trap Thresholds: Prob=${TRAP_PROB_THRESHOLD}, Alert=${TRAP_ALERT_THRESHOLD}"
    echo "  Min Free Balance: $MIN_FREE_BALANCE USDT"
    echo ""
    echo "System Status:"
    echo "  Trap Probability Meter: RUNNING (PID: $TRAP_METER_PID)"
    echo "  Dual Position Traders: $TRADER_STATUS"
    echo ""
    echo "Market Condition:"
    # In non-color mode, create a text-based progress bar
    local text_bar=$(draw_progress_bar "$prob_value" 50 "#" "-")
    echo "  Trap Probability: [$text_bar] ${TRAP_PROBABILITY}"
    echo "  Detected Trap: $DETECTED_TRAP"
    echo "==========================================================="
    echo ""
    echo "Log output appears below (press CTRL+C to stop):"
    echo "-----------------------------------------------------------"
  fi
}

# Clean up function for exit
cleanup() {
  echo ""
  if $USE_COLORS; then
    colored_echo "\e[1;33mShutting down processes...\e[0m"
  else
    echo "Shutting down processes..."
  fi
  kill $TRAP_METER_PID 2>/dev/null
  kill $TRADERS_PID 2>/dev/null
  if $USE_COLORS; then
    colored_echo "\e[1;32mDone.\e[0m"
  else
    echo "Done."
  fi
  # Reset terminal
  tput cnorm # Show cursor
  exit 0
}

# Register cleanup function
trap cleanup EXIT
trap cleanup SIGINT
trap cleanup SIGTERM

# Hide cursor for cleaner display
tput civis

# Clear screen and show initial message
clear
if $USE_COLORS; then
  colored_echo "\e[1;36m===========================================================\e[0m"
  colored_echo "\e[1;36m= OMEGA BTC AI - Trap-Aware Dual Position Traders Runner =\e[0m"
  colored_echo "\e[1;36m===========================================================\e[0m"
  colored_echo "\e[1;33mSetting up environment...\e[0m"
  colored_echo "REDIS_HOST=$REDIS_HOST"
  colored_echo "REDIS_PORT=$REDIS_PORT"
  colored_echo "COLORS: $(if $USE_COLORS; then echo "Enabled"; else echo "Disabled"; fi)"
  colored_echo "\e[1;36m===========================================================\e[0m"
else
  echo "==========================================================="
  echo "= OMEGA BTC AI - Trap-Aware Dual Position Traders Runner ="
  echo "==========================================================="
  echo "Setting up environment..."
  echo "REDIS_HOST=$REDIS_HOST"
  echo "REDIS_PORT=$REDIS_PORT"
  echo "COLORS: Disabled"
  echo "==========================================================="
fi

# Make sure we have the probability meter running in the background
if $USE_COLORS; then
  colored_echo "\e[1;33mStarting Trap Probability Meter in the background...\e[0m"
else
  echo "Starting Trap Probability Meter in the background..."
fi

# Configure color settings for subprocess
if ! $USE_COLORS; then
  export FORCE_COLOR=0
fi

python -m omega_ai.tools.trap_probability_meter --interval 5 --verbose > trap_meter.log 2>&1 &
TRAP_METER_PID=$!

if $USE_COLORS; then
  colored_echo "\e[1;32mTrap Probability Meter started with PID: $TRAP_METER_PID\e[0m"
  colored_echo "\e[1;33mWaiting 5 seconds for the meter to initialize...\e[0m"
else
  echo "Trap Probability Meter started with PID: $TRAP_METER_PID"
  echo "Waiting 5 seconds for the meter to initialize..."
fi

sleep 5

# Display the header
display_header

# Create a temporary file for output
TEMPFILE=$(mktemp)

# Run the trap-aware dual position traders with output redirected
if $USE_COLORS; then
  colored_echo "\e[1;33mStarting Trap-Aware Dual Position Traders...\e[0m"
else
  echo "Starting Trap-Aware Dual Position Traders..."
fi

python -m omega_ai.trading.strategies.trap_aware_dual_traders \
  --symbol $SYMBOL \
  --long-capital $LONG_CAPITAL \
  --short-capital $SHORT_CAPITAL \
  --long-leverage $LONG_LEVERAGE \
  --short-leverage $SHORT_LEVERAGE \
  --trap-probability-threshold $TRAP_PROB_THRESHOLD \
  --trap-alert-threshold $TRAP_ALERT_THRESHOLD \
  --min-free-balance $MIN_FREE_BALANCE \
  $EXTRA_ARGS > "$TEMPFILE" 2>&1 &

TRADERS_PID=$!

# Store the probability data in Redis
_store_trap_prediction() {
  if $USE_COLORS; then
    printf "\e[1;33mStoring trap prediction...\e[0m\n"
  else
    echo "Storing trap prediction..."
  fi
  
  # Store prediction code here
}

# Keep updating the display
while kill -0 $TRADERS_PID 2>/dev/null; do
  # Update status from log file
  if grep -q "STATUS:" "$TEMPFILE"; then
    if $USE_COLORS; then
      TRADER_STATUS=$(grep "STATUS:" "$TEMPFILE" | tail -n 1 | cut -d ":" -f 2-)
    else
      TRADER_STATUS=$(grep "STATUS:" "$TEMPFILE" | tail -n 1 | cut -d ":" -f 2- | sed 's/\x1b\[[0-9;]*m//g')
    fi
  fi
  
  # Update trap probability from log file
  if grep -q "Trap Probability:" "$TEMPFILE"; then
    if $USE_COLORS; then
      TRAP_PROBABILITY=$(grep "Trap Probability:" "$TEMPFILE" | tail -n 1 | sed 's/.*Trap Probability: \([0-9.]*%\).*/\1/')
    else
      TRAP_PROBABILITY=$(grep "Trap Probability:" "$TEMPFILE" | tail -n 1 | sed 's/.*Trap Probability: \([0-9.]*%\).*/\1/' | sed 's/\x1b\[[0-9;]*m//g')
    fi
  fi
  
  # Check for detected traps
  if grep -q "WARNING: Likely" "$TEMPFILE"; then
    if $USE_COLORS; then
      DETECTED_TRAP=$(grep "WARNING: Likely" "$TEMPFILE" | tail -n 1 | sed 's/.*Likely \([A-Z_]*\).*/\1/')
    else
      DETECTED_TRAP=$(grep "WARNING: Likely" "$TEMPFILE" | tail -n 1 | sed 's/.*Likely \([A-Z_]*\).*/\1/' | sed 's/\x1b\[[0-9;]*m//g')
    fi
  elif grep -q "No traps currently detected" "$TEMPFILE"; then
    DETECTED_TRAP="None detected"
  fi
  
  # Update display
  display_header
  
  # Show last 15 lines from the log file
  if $USE_COLORS; then
    tail -n 15 "$TEMPFILE" | grep -v "STATUS:" | while read -r line; do
      # Add color based on log level
      if [[ $line == *" - DEBUG "* ]]; then
        printf "\e[0;37m%s\e[0m\n" "$line"  # Light gray for debug
      elif [[ $line == *" - INFO "* ]]; then
        printf "\e[0;32m%s\e[0m\n" "$line"  # Green for info
      elif [[ $line == *" - WARNING "* ]]; then
        printf "\e[0;33m%s\e[0m\n" "$line"  # Yellow for warning
      elif [[ $line == *" - ALERT "* ]]; then
        printf "\e[0;35m%s\e[0m\n" "$line"  # Magenta for alerts
      elif [[ $line == *" - ERROR "* ]] || [[ $line == *" - CRITICAL "* ]]; then
        printf "\e[0;31m%s\e[0m\n" "$line"  # Red for errors
      elif [[ $line == *"Trap Probability:"* ]]; then
        # Extract probability value for coloring
        local prob=$(echo "$line" | sed 's/.*Trap Probability: \([0-9.]*%\).*/\1/' | sed 's/%//')
        local color=$(get_probability_color "$prob")
        printf "${color}%s\e[0m\n" "$line"
      elif [[ $line == *"Likely "* ]] && [[ $line == *"_TRAP"* || $line == *"_HUNT"* ]]; then
        printf "\e[0;31m%s\e[0m\n" "$line"  # Red for trap detections
      else
        echo "$line"
      fi
    done
  else
    tail -n 15 "$TEMPFILE" | grep -v "STATUS:" | sed 's/\x1b\[[0-9;]*m//g'
  fi
  
  # Update interval
  sleep 1
done

# Clean up temp file
rm -f "$TEMPFILE"

if $USE_COLORS; then
  colored_echo "\e[1;36m===========================================================\e[0m"
  colored_echo "\e[1;32mTrap-Aware Dual Position Traders finished\e[0m"
  colored_echo "\e[1;36m===========================================================\e[0m"
else
  echo "==========================================================="
  echo "Trap-Aware Dual Position Traders finished"
  echo "==========================================================="
fi 