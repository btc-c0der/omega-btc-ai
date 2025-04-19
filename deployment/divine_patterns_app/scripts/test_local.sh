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

"""
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""


# Divine Pattern Analyzer - Local Test Script
# ==========================================
#
# This script tests the Divine Pattern Analyzer locally
# Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================================${NC}"
echo -e "${CYAN}      Divine Pattern Analyzer Local Test Script       ${NC}"
echo -e "${CYAN}======================================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    exit 1
fi

# Navigate to the app directory
cd "$(dirname "$0")/.." || exit 1

# Check if required files exist
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found.${NC}"
    exit 1
fi

if [ ! -f "scripts/run.py" ]; then
    echo -e "${RED}Error: run.py not found.${NC}"
    exit 1
fi

# Install dependencies in development mode
echo -e "${BLUE}Installing application in development mode...${NC}"
pip install -e . > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install application.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Application installed${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    source venv/bin/activate
fi

# Run health check in background
echo -e "${BLUE}Starting API server in background...${NC}"
python3 scripts/run.py &
SERVER_PID=$!

# Give server time to start
echo -e "${YELLOW}Waiting for server to start...${NC}"
sleep 5

# Test health endpoint
echo -e "${BLUE}Testing health endpoint...${NC}"
HEALTH_RESPONSE=$(curl -s http://localhost:8080/health)
if [ $? -ne 0 ] || [ -z "$HEALTH_RESPONSE" ]; then
    echo -e "${RED}❌ Health check failed.${NC}"
    kill $SERVER_PID
    exit 1
fi
echo -e "${GREEN}✅ Health check passed${NC}"
echo "$HEALTH_RESPONSE" | python3 -m json.tool

# Test sample data endpoint
echo -e "${BLUE}Testing sample data endpoint...${NC}"
SAMPLE_RESPONSE=$(curl -s "http://localhost:8080/sample?days=1&sample_rate=12")
if [ $? -ne 0 ] || [ -z "$SAMPLE_RESPONSE" ]; then
    echo -e "${RED}❌ Sample data endpoint failed.${NC}"
    kill $SERVER_PID
    exit 1
fi
echo -e "${GREEN}✅ Sample data endpoint passed${NC}"

# Extract sample data for analysis test
SAMPLE_VALUES=$(echo "$SAMPLE_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data['values']))")
SAMPLE_TIMESTAMPS=$(echo "$SAMPLE_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data['timestamps']))")

# Test analyze endpoint
echo -e "${BLUE}Testing analyze endpoint...${NC}"
ANALYZE_RESPONSE=$(curl -s -X POST \
  "http://localhost:8080/analyze?sample_rate=12" \
  -H "Content-Type: application/json" \
  -d "{\"values\": $SAMPLE_VALUES, \"timestamps\": $SAMPLE_TIMESTAMPS}")
if [ $? -ne 0 ] || [ -z "$ANALYZE_RESPONSE" ]; then
    echo -e "${RED}❌ Analyze endpoint failed.${NC}"
    kill $SERVER_PID
    exit 1
fi
echo -e "${GREEN}✅ Analyze endpoint passed${NC}"
echo -e "${YELLOW}Analysis results:${NC}"
echo "$ANALYZE_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"  Divine Patterns: {len(data['divine_patterns'])} found\")"

# Stop the server
echo -e "${BLUE}Stopping API server...${NC}"
kill $SERVER_PID

echo -e "${GREEN}✅ All tests passed successfully!${NC}"
echo -e "${CYAN}The application is ready for deployment.${NC}" 