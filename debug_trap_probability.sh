#!/bin/bash

# OMEGA BTC AI - Trap Probability Debug Script
# This script helps debug the trap probability display by setting simulated values in Redis

# Default settings
USE_COLORS=true
REDIS_HOST=localhost
REDIS_PORT=6379
DEBUG=true

# Set trap probability sequence (percent values)
PROBABILITY_VALUES=(
  "0.1" "5.0" "12.0" "25.0" "37.0" "52.0" "68.0" "75.0" "82.0" "90.0" "75.0" "60.0" "45.0" "30.0" "15.0" "5.0"
)

# Set trap types sequence
TRAP_TYPES=(
  "none" "none" "none" "none" "potential_stop_hunt" "potential_stop_hunt" "stop_hunt" "stop_hunt" 
  "stop_hunt" "liquidity_grab" "liquidity_grab" "fading" "fading" "none" "none" "none"
)

# Function to generate JSON for trap probability data
generate_probability_json() {
  local prob="$1"
  local trap_type="$2"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
  
  # Generate component probabilities with some variation
  local price_pattern=$(echo "scale=2; $RANDOM/32768 * 0.5 + 0.2" | bc)
  local volume_spike=$(echo "scale=2; $RANDOM/32768 * 0.5 + 0.3" | bc)
  local fib_level=$(echo "scale=2; $RANDOM/32768 * 0.5 + 0.2" | bc)
  local historical_match=$(echo "scale=2; $RANDOM/32768 * 0.4 + 0.3" | bc)
  local order_book=$(echo "scale=2; $RANDOM/32768 * 0.5 + 0.2" | bc)
  local market_regime=$(echo "scale=2; $RANDOM/32768 * 0.4 + 0.3" | bc)
  
  # Generate confidence for trap detection
  local confidence=0.0
  if [ "$trap_type" != "none" ]; then
    confidence=$(echo "scale=2; $RANDOM/32768 * 0.3 + 0.6" | bc)
  fi
  
  # Create the base JSON
  local json='{"timestamp":"'$timestamp'","probability":'$prob',"components":{'
  json+='"price_pattern":'$price_pattern','
  json+='"volume_spike":'$volume_spike','
  json+='"fib_level":'$fib_level','
  json+='"historical_match":'$historical_match','
  json+='"order_book":'$order_book','
  json+='"market_regime":'$market_regime
  json+='}}'
  
  # Add trap type and confidence if needed
  if [ "$trap_type" != "none" ]; then
    # Remove the closing brace to add more properties
    json=${json%?}
    json+=',"trap_type":"'$trap_type'","confidence":'$confidence'}'
  fi
  
  echo "$json"
}

# Function to store trap probability data in Redis
store_probability_in_redis() {
  local prob="$1"
  local trap_type="$2"
  
  if [ "$DEBUG" = true ]; then
    echo "Storing probability $prob with trap type $trap_type in Redis"
  fi
  
  # Generate JSON
  local json=$(generate_probability_json "$prob" "$trap_type")
  
  if [ "$DEBUG" = true ]; then
    echo "JSON: $json"
  fi
  
  # Store in Redis
  redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" SET "current_trap_probability" "$json"
  redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" LPUSH "trap_probability_history" "$json"
  redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" LTRIM "trap_probability_history" 0 99
  
  # Store current BTC price (simulated)
  local price=$(echo "scale=2; 85000 + $RANDOM/32768 * 1000 - 500" | bc)
  redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" SET "btc_price" "{\"price\":$price}"
  
  if [ "$DEBUG" = true ]; then
    echo "Stored data in Redis successfully"
    echo "------------------------------------------"
  fi
}

# Function to check Redis connection
check_redis() {
  if ! redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" PING > /dev/null; then
    echo "Error: Cannot connect to Redis at $REDIS_HOST:$REDIS_PORT"
    echo "Please make sure Redis is running."
    return 1
  fi
  
  echo "Redis connection successful at $REDIS_HOST:$REDIS_PORT"
  return 0
}

# Print script header
echo "OMEGA BTC AI - Trap Probability Debug Script"
echo "============================================="
echo "This script will simulate trap probability values in Redis"
echo "for testing the trap-aware traders script display."
echo

# Check Redis connection
if ! check_redis; then
  echo "Exiting due to Redis connection error."
  exit 1
fi

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --redis-host=*)
      REDIS_HOST="${1#*=}"
      shift
      ;;
    --redis-port=*)
      REDIS_PORT="${1#*=}"
      shift
      ;;
    --no-debug)
      DEBUG=false
      shift
      ;;
    *)
      shift
      ;;
  esac
done

echo "Starting trap probability simulation..."
echo "Values will be written to Redis at $REDIS_HOST:$REDIS_PORT"
echo

# Simulate the trap probability values in Redis
for i in "${!PROBABILITY_VALUES[@]}"; do
  # Get probability and trap type
  prob="${PROBABILITY_VALUES[$i]}"
  trap_type="${TRAP_TYPES[$i]}"
  
  # Store in Redis
  store_probability_in_redis "$prob" "$trap_type"
  
  echo "Set trap probability to $prob% (trap type: $trap_type)"
  
  # Pause between updates
  sleep 3
done

echo
echo "Simulation complete! The trap probability values have been"
echo "set in Redis. You can now run the trap-aware traders script"
echo "to see the display updating with these values." 