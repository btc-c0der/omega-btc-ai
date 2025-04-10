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

# Run Tesla Dashboard v3
# This script runs the Divine Dashboard v3 with Tesla Cybertruck QA Integration

# Set color variables
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡"
echo "⚡                                      ⚡"
echo "⚡   Tesla Divine Dashboard v3          ⚡"
echo "⚡   with Cybertruck QA Integration     ⚡"
echo "⚡                                      ⚡"
echo "⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡ ⚡"
echo -e "${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 to run this dashboard."
    exit 1
fi

# Check if required packages are installed
echo -e "${PURPLE}Checking dependencies...${NC}"
if ! pip list | grep -q "fastapi"; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo -e "${GREEN}Starting Divine Dashboard v3 Server...${NC}"
echo "Main Dashboard will be available at: http://localhost:8889"
echo "Cybertruck QA Dashboard will be available at: http://localhost:7860"
echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"

# Change to script directory
cd "$(dirname "$0")"

# Run the server
python3 divine_server.py

# Exit message if server stops
echo -e "${PURPLE}Divine Dashboard v3 Server stopped${NC}" 