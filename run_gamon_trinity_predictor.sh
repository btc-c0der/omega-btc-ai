#!/bin/bash

# OMEGA BTC AI - GAMON Trinity Predictor
# =====================================
#
# This script runs the GAMON Trinity Predictor to forecast future market states
# using a combination of HMM, Eigenwaves, and Cycle analysis.

# ANSI color codes for divine output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

echo -e "${PURPLE}"
echo "🔱 OMEGA BTC AI - GAMON TRINITY PREDICTOR 🔱"
echo -e "========================================${RESET}"
echo

# Check for Python environment
echo -e "${YELLOW}Checking Python environment...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${RESET}"
    exit 1
fi

# Make sure the script is executable
chmod +x gamon_trinity_predictor.py

# Run the predictor
echo -e "${CYAN}🚀 Starting GAMON Trinity Predictor...${RESET}"
python3 -u gamon_trinity_predictor.py

echo
echo -e "${PURPLE}========================================${RESET}"
echo -e "${GREEN}✨ PREDICTIONS COMPLETE ✨${RESET}"
echo -e "${YELLOW}Check plots/gamon_trinity_predictions.html for the visualization${RESET}"
echo 