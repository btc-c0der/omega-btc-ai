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

# Run BTC Monitoring System with explicit Redis configuration
# This script ensures the correct Redis host is used

# Set environment variables
export REDIS_HOST=localhost
export REDIS_PORT=6379

# Display startup message
echo "Starting BTC Monitoring System with Redis host: $REDIS_HOST"

# Run the monitoring script
python start_btc_monitoring.py 