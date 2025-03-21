#!/bin/bash

# OMEGA BTC AI - Trap-Aware Dual Position Traders Runner
# This script runs the trap-aware dual position traders with proper environment settings.

# Set environment variables
export REDIS_HOST=localhost
export REDIS_PORT=6379

# Display startup message
echo "==========================================================="
echo "= OMEGA BTC AI - Trap-Aware Dual Position Traders Runner ="
echo "==========================================================="
echo "Setting up environment..."
echo "REDIS_HOST=$REDIS_HOST"
echo "REDIS_PORT=$REDIS_PORT"
echo "==========================================================="

# Make sure we have the probability meter running in the background
echo "Starting Trap Probability Meter in the background..."
python -m omega_ai.tools.trap_probability_meter --interval 5 --verbose &
TRAP_METER_PID=$!
echo "Trap Probability Meter started with PID: $TRAP_METER_PID"
echo "Waiting 5 seconds for the meter to initialize..."
sleep 5

# Run the trap-aware dual position traders
echo "Starting Trap-Aware Dual Position Traders..."
python -m omega_ai.trading.strategies.trap_aware_dual_traders \
  --symbol BTCUSDT \
  --long-capital 150.0 \
  --short-capital 200.0 \
  --long-leverage 11 \
  --short-leverage 11 \
  --trap-probability-threshold 0.6 \
  --trap-alert-threshold 0.7 \
  --min-free-balance 50.0 \
  "$@"

# Clean up background process when this script exits
trap "kill $TRAP_METER_PID 2>/dev/null" EXIT

echo "==========================================================="
echo "Trap-Aware Dual Position Traders finished"
echo "===========================================================" 