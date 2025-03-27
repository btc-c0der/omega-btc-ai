#!/bin/bash

# OMEGA BTC AI - Trap Probability Simulator
# A debug tool to simulate trap probability changes for testing the display

echo "🔄 Starting trap probability simulation..."
echo "Press Ctrl+C to stop"
echo ""

# Create temp file for JSON
TEMP_FILE=$(mktemp)

# Trap types with emoji
TRAP_TYPES=(
  "liquidity_grab:💰"
  "stop_hunt:🎯"
  "bull_trap:🐂"
  "bear_trap:🐻"
  "fake_pump:🚀"
  "fake_dump:📉"
)

# Make sure temp file is deleted on exit
trap "rm -f $TEMP_FILE" EXIT

# Function to generate timestamp
get_timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%S.000Z"
}

# Starting probability
PROBABILITY=35.0
TREND="increasing"
CHANGE=0.05
TRAP_TYPE="none"
CONFIDENCE=0.0

# Components and their base values - using regular arrays
COMPONENT_NAMES=(
  "price_pattern"
  "volume_spike"
  "fib_level"
  "historical_match"
  "order_book"
  "market_regime"
)

COMPONENT_VALUES=(
  0.3
  0.4
  0.3
  0.2
  0.3
  0.4
)

# Component descriptions - using regular arrays
DESCRIPTION_VALUES=(
  "Normal price action"
  "Average volume"
  "Not near key levels"
  "No significant pattern match"
  "Balanced order book"
  "Neutral market conditions"
)

# Get component value by name
get_component_value() {
  local component_name=$1
  local index=0
  
  for name in "${COMPONENT_NAMES[@]}"; do
    if [[ "$name" == "$component_name" ]]; then
      echo "${COMPONENT_VALUES[$index]}"
      return
    fi
    ((index++))
  done
  
  echo "0.0"
}

# Set component value by name
set_component_value() {
  local component_name=$1
  local new_value=$2
  local index=0
  
  for name in "${COMPONENT_NAMES[@]}"; do
    if [[ "$name" == "$component_name" ]]; then
      COMPONENT_VALUES[$index]=$new_value
      return
    fi
    ((index++))
  done
}

# Get component description by name
get_description() {
  local component_name=$1
  local index=0
  
  for name in "${COMPONENT_NAMES[@]}"; do
    if [[ "$name" == "$component_name" ]]; then
      echo "${DESCRIPTION_VALUES[$index]}"
      return
    fi
    ((index++))
  done
  
  echo "Unknown"
}

# Set component description by name
set_description() {
  local component_name=$1
  local new_description=$2
  local index=0
  
  for name in "${COMPONENT_NAMES[@]}"; do
    if [[ "$name" == "$component_name" ]]; then
      DESCRIPTION_VALUES[$index]="$new_description"
      return
    fi
    ((index++))
  done
}

# Simulate a trap formation scenario
simulate_trap_formation() {
  # Random selection of trap type when probability crosses 60
  if (( $(echo "$PROBABILITY > 60.0" | bc -l) )) && [ "$TRAP_TYPE" == "none" ]; then
    RANDOM_INDEX=$((RANDOM % ${#TRAP_TYPES[@]}))
    TRAP_TYPE_WITH_EMOJI=${TRAP_TYPES[$RANDOM_INDEX]}
    TRAP_TYPE=${TRAP_TYPE_WITH_EMOJI%%:*}
    CONFIDENCE=0.65
    echo "🚨 Trap forming: $TRAP_TYPE (${TRAP_TYPE_WITH_EMOJI#*:})"
  fi
  
  # Increase confidence as probability increases
  if [ "$TRAP_TYPE" != "none" ]; then
    CONFIDENCE=$(echo "$CONFIDENCE + 0.02" | bc)
    if (( $(echo "$CONFIDENCE > 0.95" | bc -l) )); then
      CONFIDENCE=0.95
    fi
  fi
  
  # Update probability based on scenario phase
  case $1 in
    "rising")
      PROBABILITY=$(echo "$PROBABILITY + (($RANDOM % 10) / 10)" | bc)
      TREND="increasing"
      CHANGE=$(echo "($RANDOM % 15) / 100" | bc)
      
      # Increase component values
      for i in "${!COMPONENT_NAMES[@]}"; do
        component=${COMPONENT_NAMES[$i]}
        current_value=${COMPONENT_VALUES[$i]}
        new_value=$(echo "$current_value + (($RANDOM % 10) / 100)" | bc)
        
        if (( $(echo "$new_value > 0.95" | bc -l) )); then
          new_value=0.95
        fi
        
        COMPONENT_VALUES[$i]=$new_value
      done
      
      # Update descriptions as values increase
      price_pattern_value=${COMPONENT_VALUES[0]}
      volume_spike_value=${COMPONENT_VALUES[1]}
      
      if (( $(echo "$price_pattern_value > 0.7" | bc -l) )); then
        DESCRIPTION_VALUES[0]="Wyckoff distribution pattern"
      elif (( $(echo "$price_pattern_value > 0.5" | bc -l) )); then
        DESCRIPTION_VALUES[0]="Suspicious price pattern forming"
      fi
      
      if (( $(echo "$volume_spike_value > 0.7" | bc -l) )); then
        DESCRIPTION_VALUES[1]="Volume 3x above average"
      elif (( $(echo "$volume_spike_value > 0.5" | bc -l) )); then
        DESCRIPTION_VALUES[1]="Volume increasing abnormally"
      fi
      ;;
      
    "peaking")
      PROBABILITY=$(echo "$PROBABILITY + (($RANDOM % 8) / 10) - 0.2" | bc)
      
      if (( $(echo "$PROBABILITY > 85.0" | bc -l) )); then
        PROBABILITY=85.0
      fi
      
      TREND="stable"
      CHANGE=$(echo "(($RANDOM % 8) / 100) - 0.02" | bc)
      ;;
      
    "fading")
      PROBABILITY=$(echo "$PROBABILITY - (($RANDOM % 12) / 10)" | bc)
      TREND="decreasing"
      CHANGE=$(echo "-($RANDOM % 20) / 100" | bc)
      
      # Decrease component values
      for i in "${!COMPONENT_NAMES[@]}"; do
        component=${COMPONENT_NAMES[$i]}
        current_value=${COMPONENT_VALUES[$i]}
        new_value=$(echo "$current_value - (($RANDOM % 10) / 100)" | bc)
        
        if (( $(echo "$new_value < 0.15" | bc -l) )); then
          new_value=0.15
        fi
        
        COMPONENT_VALUES[$i]=$new_value
      done
      
      # Reset trap type when probability drops below 30
      if (( $(echo "$PROBABILITY < 30.0" | bc -l) )) && [ "$TRAP_TYPE" != "none" ]; then
        echo "✓ Trap resolved: $TRAP_TYPE"
        TRAP_TYPE="none"
        CONFIDENCE=0.0
      fi
      ;;
  esac
  
  # Ensure probability stays in valid range
  if (( $(echo "$PROBABILITY > 100.0" | bc -l) )); then
    PROBABILITY=100.0
  elif (( $(echo "$PROBABILITY < 5.0" | bc -l) )); then
    PROBABILITY=5.0
  fi
}

# Create JSON and store to Redis
store_trap_data() {
  # Create components section
  COMP_JSON=""
  for i in "${!COMPONENT_NAMES[@]}"; do
    component=${COMPONENT_NAMES[$i]}
    value=${COMPONENT_VALUES[$i]}
    description=${DESCRIPTION_VALUES[$i]}
    
    if [ -n "$COMP_JSON" ]; then
      COMP_JSON+=","
    fi
    COMP_JSON+="\"$component\": {\"value\": $value, \"description\": \"$description\"}"
  done
  
  # Create full JSON
  cat > $TEMP_FILE << EOF
{
  "probability": $PROBABILITY,
  "timestamp": "$(get_timestamp)",
  "trend": "$TREND",
  "change": $CHANGE,
  "components": {
    $COMP_JSON
  },
  "trap_type": "$TRAP_TYPE",
  "confidence": $CONFIDENCE
}
EOF
  
  # Store in Redis
  cat $TEMP_FILE | redis-cli -x set current_trap_probability > /dev/null
  
  # Store in history list
  cat $TEMP_FILE | redis-cli -x lpush trap_probability_history > /dev/null
  redis-cli ltrim trap_probability_history 0 99 > /dev/null
  
  # Display current status
  printf "\rProbability: %5.1f%%  Trend: %-12s  Trap: %-15s  Phase: %-8s" $PROBABILITY "$TREND" "$TRAP_TYPE" "$1"
}

# Simulate trap formation and fading cycle
echo "Phase 1: Initial trap formation..."
for i in {1..15}; do
  simulate_trap_formation "rising"
  store_trap_data "rising"
  sleep 2
done

echo -e "\nPhase 2: Trap peaking..."
for i in {1..10}; do
  simulate_trap_formation "peaking"
  store_trap_data "peaking"
  sleep 2
done

echo -e "\nPhase 3: Trap fading..."
for i in {1..20}; do
  simulate_trap_formation "fading"
  store_trap_data "fading"
  sleep 2
done

echo -e "\n\n✅ Simulation completed!" 