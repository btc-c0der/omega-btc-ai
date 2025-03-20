#!/bin/bash
# OMEGA BTC AI - BitGet API Environment Test Runner
# ================================================
# This script runs the BitGet environment test to check API credentials from .env

# Set color codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print header
echo -e "${CYAN}==============================${NC}"
echo -e "${CYAN}BitGet API Env Test Runner${NC}"
echo -e "${CYAN}==============================${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}No .env file found in current directory.${NC}"
    echo -e "${YELLOW}Looking for .env in parent directories...${NC}"
    
    # Try to find .env in parent directories
    parent_dir=$(dirname "$(pwd)")
    if [ -f "$parent_dir/.env" ]; then
        echo -e "${GREEN}Found .env in parent directory.${NC}"
        cp "$parent_dir/.env" .
        echo -e "${GREEN}Copied .env to current directory.${NC}"
    else
        echo -e "${RED}ERROR: No .env file found.${NC}"
        echo -e "${YELLOW}Please create a .env file with BitGet API credentials.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Found .env file in current directory.${NC}"
fi

# Make the test script executable if it isn't already
if [ ! -x "test_bitget_env.py" ]; then
    echo -e "${YELLOW}Making test script executable...${NC}"
    chmod +x test_bitget_env.py
fi

# Run the test script
echo -e "${BLUE}Running BitGet API environment test...${NC}"
./test_bitget_env.py

# Return code
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}Test completed successfully.${NC}"
else
    echo -e "${RED}Test failed with exit code: $exit_code${NC}"
fi

exit $exit_code 