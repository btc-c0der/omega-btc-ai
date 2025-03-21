#!/bin/bash
# Run BTC Monitoring System with explicit Redis configuration
# This script ensures the correct Redis host is used

# Set environment variables
export REDIS_HOST=localhost
export REDIS_PORT=6379

# Display startup message
echo "Starting BTC Monitoring System with Redis host: $REDIS_HOST"

# Run the monitoring script
python start_btc_monitoring.py 