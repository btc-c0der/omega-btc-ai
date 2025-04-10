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


# Utility script to run the OMEGA BTC AI React Dashboard

# Navigate to the React dashboard directory
cd "$(dirname "$0")/deployment/digitalocean/news_service/omega-react"

# Execute the dashboard runner script
./run.sh

# If the script doesn't exist or isn't executable, provide fallback
if [ $? -ne 0 ]; then
  echo "Couldn't run the dashboard script, trying fallback method..."
  
  # Check if http-server is installed
  if ! command -v http-server &> /dev/null; then
    echo "Installing http-server..."
    npm install -g http-server
  fi
  
  # Run http-server
  echo "Starting http-server..."
  http-server -p 3000 .
fi 