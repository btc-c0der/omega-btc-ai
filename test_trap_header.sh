#!/bin/bash

# OMEGA BTC AI - Trap Header Display Test
# A simple test script to verify the header display with simulated data

# Default settings
USE_COLORS=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-color)
      USE_COLORS=false
      shift
      ;;
    *)
      shift
      ;;
  esac
done

# Initialize simulated variables
REDIS_HOST="localhost"
REDIS_PORT="6379"
TRAP_METER_PID="12345"
TRADER_STATUS="INITIALIZING"
TRAP_PROBABILITY="0.0%"
DETECTED_TRAP="None"

# Function for colored or plain echo based on settings
colored_echo() {
  if $USE_COLORS; then
    printf "%b\n" "$1"
  else
    # Strip ANSI color codes
    echo "$1" | sed 's/\x1b\[[0-9;]*m//g'
  fi
}

# Function to clear screen and display header
display_header() {
  clear
  if $USE_COLORS; then
    colored_echo "\e[1;36m===========================================================\e[0m"
    colored_echo "\e[1;36m= OMEGA BTC AI - Trap-Aware Dual Position Traders Runner =\e[0m"
    colored_echo "\e[1;36m===========================================================\e[0m"
    colored_echo "\e[1;36mEnvironment:\e[0m"
    colored_echo "  \e[1;36mREDIS_HOST=\e[0m$REDIS_HOST"
    colored_echo "  \e[1;36mREDIS_PORT=\e[0m$REDIS_PORT"
    colored_echo ""
    colored_echo "\e[1;36mSystem Status:\e[0m"
    colored_echo "  \e[1;36mTrap Probability Meter: \e[1;32mRUNNING\e[0m (PID: $TRAP_METER_PID)"
    colored_echo "  \e[1;36mDual Position Traders: \e[1;33m$TRADER_STATUS\e[0m"
    colored_echo ""
    colored_echo "\e[1;36mMarket Condition:\e[0m"
    colored_echo "  \e[1;36mCurrent Trap Probability: \e[1;33m$TRAP_PROBABILITY\e[0m"
    colored_echo "  \e[1;36mDetected Trap: \e[1;33m$DETECTED_TRAP\e[0m"
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
    echo "System Status:"
    echo "  Trap Probability Meter: RUNNING (PID: $TRAP_METER_PID)"
    echo "  Dual Position Traders: $TRADER_STATUS"
    echo ""
    echo "Market Condition:"
    echo "  Current Trap Probability: $TRAP_PROBABILITY"
    echo "  Detected Trap: $DETECTED_TRAP"
    echo "==========================================================="
    echo ""
    echo "Log output appears below (press CTRL+C to stop):"
    echo "-----------------------------------------------------------"
  fi
}

# Hide cursor for cleaner display
tput civis

# Clean up function for exit
cleanup() {
  echo ""
  if $USE_COLORS; then
    colored_echo "\e[1;32mTest finished.\e[0m"
  else
    echo "Test finished."
  fi
  # Reset terminal
  tput cnorm # Show cursor
  exit 0
}

# Register cleanup function
trap cleanup EXIT
trap cleanup SIGINT
trap cleanup SIGTERM

# Display initial information
clear
if $USE_COLORS; then
  colored_echo "\e[1;36m===========================================================\e[0m"
  colored_echo "\e[1;36m=            OMEGA BTC AI - Header Display Test           =\e[0m"
  colored_echo "\e[1;36m===========================================================\e[0m"
  colored_echo "\e[1;33mStarting header simulation...\e[0m"
  colored_echo "COLORS: $(if $USE_COLORS; then echo "Enabled"; else echo "Disabled"; fi)"
  colored_echo "\e[1;36m===========================================================\e[0m"
else
  echo "==========================================================="
  echo "=            OMEGA BTC AI - Header Display Test           ="
  echo "==========================================================="
  echo "Starting header simulation..."
  echo "COLORS: Disabled"
  echo "==========================================================="
fi

sleep 2

# Simulate various states
STATES=(
  "INITIALIZING:0.0%:None"
  "RUNNING:0.23%:None"
  "RUNNING:0.42%:None"
  "RUNNING:0.67%:POTENTIAL_STOP_HUNT"
  "ALERT:0.82%:STOP_HUNT"
  "CAUTION:0.73%:STOP_HUNT"
  "TRADING:0.65%:STOP_HUNT"
  "TRADING:0.58%:FADING"
  "TRADING:0.31%:None"
  "TRADING:0.12%:None"
)

# Generate simulated log lines
LOG_LINES=(
  "2025-03-21 01:48:10,475 - omega_ai.trading - INFO - Initializing dual position traders"
  "2025-03-21 01:48:11,235 - omega_ai.trading - INFO - Connected to BitGet exchange API"
  "2025-03-21 01:48:12,115 - omega_ai.trading - DEBUG - Market data received for BTCUSDT"
  "2025-03-21 01:48:13,336 - omega_ai.trading - INFO - BTC current price: 85,432.50 USDT"
  "2025-03-21 01:48:14,518 - omega_ai.trap - INFO - Trap Probability: 0.23%"
  "2025-03-21 01:48:15,780 - omega_ai.trading - INFO - Account balance: 423.50 USDT"
  "2025-03-21 01:48:16,921 - omega_ai.trap - WARNING - Trap probability increasing: 0.42%"
  "2025-03-21 01:48:17,134 - omega_ai.trading - INFO - Monitoring market conditions"
  "2025-03-21 01:48:18,273 - omega_ai.trap - WARNING - Trap probability rising rapidly: 0.67%"
  "2025-03-21 01:48:19,425 - omega_ai.trap - WARNING - Potential STOP_HUNT pattern detected"
  "2025-03-21 01:48:20,587 - omega_ai.trap - ALERT - Trap probability critical: 0.82%"
  "2025-03-21 01:48:21,736 - omega_ai.trap - WARNING - Likely STOP_HUNT forming at 85,432.50"
  "2025-03-21 01:48:22,902 - omega_ai.trading - INFO - Adjusting position sizing based on trap"
  "2025-03-21 01:48:23,047 - omega_ai.trading - INFO - Trap probability decreasing: 0.73%"
  "2025-03-21 01:48:24,159 - omega_ai.trading - INFO - Trap probability decreasing: 0.65%"
  "2025-03-21 01:48:25,267 - omega_ai.trading - INFO - STOP_HUNT pattern fading"
  "2025-03-21 01:48:26,380 - omega_ai.trading - INFO - Trap probability decreasing: 0.58%"
  "2025-03-21 01:48:27,491 - omega_ai.trading - INFO - Trap probability decreasing: 0.31%"
  "2025-03-21 01:48:28,602 - omega_ai.trading - INFO - No traps currently detected"
  "2025-03-21 01:48:29,714 - omega_ai.trading - INFO - Trap probability low: 0.12%"
)

# Display each state with appropriate log data
for i in "${!STATES[@]}"; do
  # Parse state
  IFS=':' read -r -a state_parts <<< "${STATES[$i]}"
  TRADER_STATUS="${state_parts[0]}"
  TRAP_PROBABILITY="${state_parts[1]}"
  DETECTED_TRAP="${state_parts[2]}"
  
  # Update and display header
  display_header
  
  # Display log lines up to current state
  log_count=$((i+1))
  for j in $(seq 0 $log_count); do
    if [ $j -lt ${#LOG_LINES[@]} ]; then
      if $USE_COLORS; then
        # Add color based on log level
        line="${LOG_LINES[$j]}"
        if [[ $line == *" - DEBUG "* ]]; then
          printf "\e[0;37m%s\e[0m\n" "$line"
        elif [[ $line == *" - INFO "* ]]; then
          printf "\e[0;32m%s\e[0m\n" "$line"
        elif [[ $line == *" - WARNING "* ]]; then
          printf "\e[0;33m%s\e[0m\n" "$line"
        elif [[ $line == *" - ALERT "* ]] || [[ $line == *" - ERROR "* ]]; then
          printf "\e[0;31m%s\e[0m\n" "$line"
        else
          echo "$line"
        fi
      else
        echo "${LOG_LINES[$j]}"
      fi
    fi
  done
  
  # Sleep to simulate time passing
  sleep 3
done

echo ""
if $USE_COLORS; then
  colored_echo "\e[1;32mTest completed successfully!\e[0m"
else
  echo "Test completed successfully!"
fi

# Wait for user to press a key
read -n 1 -s -r -p "Press any key to exit..."
cleanup 