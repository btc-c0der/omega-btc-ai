#!/bin/bash

# Navigate to the omega_ai directory
cd "$(dirname "$0")"

# Default mode is "full"
MODE=${1:-full}

# Start the OMEGA BTC AI system with the specified mode
echo "Starting OMEGA BTC AI in $MODE mode..."
python omega_ai/omega_runner.py --mode $MODE

# If the script exits with an error, show the logs
if [ $? -ne 0 ]; then
    echo "Error: OMEGA BTC AI failed to start properly"
    echo "Checking logs..."
    tail -n 50 omega_runner.log
    tail -n 50 omega_service.log
fi