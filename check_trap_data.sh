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


# OMEGA BTC AI - Check Trap Probability Data
# This script displays current trap probability data stored in Redis

# Default settings
REDIS_HOST=localhost
REDIS_PORT=6379

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
    *)
      shift
      ;;
  esac
done

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

# Function to get and format current trap probability
get_current_trap_probability() {
  # Get data from Redis
  local data=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" GET "current_trap_probability")
  
  if [ -z "$data" ]; then
    echo "No current trap probability data found in Redis."
    return 1
  fi
  
  # Extract and display probability
  local probability=$(echo "$data" | grep -o '"probability":[0-9.]*' | cut -d':' -f2)
  local timestamp=$(echo "$data" | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4)
  
  echo "Current Trap Probability: $probability%"
  echo "Timestamp: $timestamp"
  
  # Check if trap type exists
  if echo "$data" | grep -q '"trap_type"'; then
    local trap_type=$(echo "$data" | grep -o '"trap_type":"[^"]*"' | cut -d'"' -f4)
    local confidence=$(echo "$data" | grep -o '"confidence":[0-9.]*' | cut -d':' -f2)
    echo "Detected Trap: $trap_type (confidence: $confidence)"
  else
    echo "No trap detected"
  fi
  
  # Extract components
  echo "Component Values:"
  echo "$data" | grep -o '"components":{[^}]*}' | sed 's/"components":{//g' | sed 's/}//g' | tr ',' '\n' | sed 's/"//g'
}

# Function to get trap probability history count
get_history_count() {
  local count=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" LLEN "trap_probability_history")
  echo "History entries: $count"
}

# Print script header
echo "OMEGA BTC AI - Check Trap Probability Data"
echo "=========================================="
echo

# Check Redis connection
if ! check_redis; then
  echo "Exiting due to Redis connection error."
  exit 1
fi

echo
echo "Current Trap Probability Data:"
echo "-----------------------------"
get_current_trap_probability

echo
get_history_count

echo
echo "BTC Price Data:"
echo "--------------"
redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" GET "btc_price"

echo
echo "To view the full history (last 5 entries):"
echo "-----------------------------------------"
redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" LRANGE "trap_probability_history" 0 4 