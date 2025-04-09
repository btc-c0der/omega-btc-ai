#!/bin/bash

# OMEGA BTC AI - Trap Trader Process Terminator
# Automatically finds and kills any running trap aware trader processes

echo "🔍 Searching for trap aware trader processes..."

# Find process IDs
trap_pids=$(ps aux | grep -i "trap.*trader\|run_trap\|trap_aware" | grep -v grep | grep -v "kill_trap_traders" | awk '{print $2}')

# Count processes
process_count=$(echo "$trap_pids" | grep -v "^$" | wc -l | tr -d ' ')

if [ "$process_count" -eq 0 ]; then
  echo "✅ No trap aware trader processes found."
  exit 0
fi

# Display found processes
echo "🚨 Found $process_count trap aware trader processes:"
for pid in $trap_pids; do
  process_info=$(ps -p "$pid" -o command | grep -v COMMAND)
  echo "   PID $pid: ${process_info:0:80}..."
done

# Kill processes
echo "🛑 Terminating $process_count processes..."
for pid in $trap_pids; do
  kill -9 "$pid" 2>/dev/null
  if [ $? -eq 0 ]; then
    echo "   ✓ Killed process $pid"
  else
    echo "   ✗ Failed to kill process $pid"
  fi
done

# Verify all processes are terminated
remaining=$(ps aux | grep -i "trap.*trader\|run_trap\|trap_aware" | grep -v grep | grep -v "kill_trap_traders" | wc -l | tr -d ' ')
if [ "$remaining" -eq 0 ]; then
  echo "✅ All trap aware trader processes successfully terminated."
else
  echo "⚠️ Warning: $remaining processes could not be terminated."
fi 