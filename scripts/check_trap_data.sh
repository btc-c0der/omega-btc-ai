#!/bin/bash

# OMEGA BTC AI - Trap Probability Data Checker
# A utility script to inspect the current trap probability data in Redis

echo "🔍 Checking trap probability data in Redis..."
echo ""

# Check if current_trap_probability exists
echo "== CURRENT TRAP PROBABILITY =="
if redis-cli exists current_trap_probability > /dev/null; then
  echo "✅ Key exists in Redis"
  
  # Format and display the data
  echo ""
  echo "== TRAP DATA SUMMARY =="
  redis-cli get current_trap_probability | jq '{ 
    probability: .probability, 
    timestamp: .timestamp, 
    trend: .trend, 
    trap_type: .trap_type, 
    confidence: .confidence 
  }'
  
  echo ""
  echo "== TRAP COMPONENTS =="
  redis-cli get current_trap_probability | jq '.components'
  
  # Get history count
  HISTORY_COUNT=$(redis-cli llen trap_probability_history)
  echo ""
  echo "== TRAP HISTORY =="
  echo "📊 History entries: $HISTORY_COUNT"
  
  # Show last 3 history entries if available
  if [ "$HISTORY_COUNT" -gt 0 ]; then
    echo ""
    echo "Last 3 entries:"
    for i in {0..2}; do
      if [ "$i" -lt "$HISTORY_COUNT" ]; then
        ENTRY=$(redis-cli lindex trap_probability_history $i)
        if [ ! -z "$ENTRY" ]; then
          echo "$ENTRY" | jq '{ timestamp: .timestamp, probability: .probability, trend: .trend }'
        fi
      fi
    done
  fi
  
else
  echo "❌ No trap probability data found in Redis"
  echo ""
  echo "You can set test data with:"
  echo "cat scripts/set_trap.json | redis-cli -x set current_trap_probability"
fi

echo ""
echo "Done." 