#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
#
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
#
# 🌸 WE BLOOM NOW AS ONE 🌸

# TESLA Cybertruck QA Dashboard Launcher
# Part of Divine Book Dashboard v3

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CYBERTRUCK_DIR="${SCRIPT_DIR}/components/cybertruck"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}                                                        ${BLUE}║${NC}"
echo -e "${BLUE}║${YELLOW}        ⚡ TESLA CYBERTRUCK QA DASHBOARD 3D ⚡        ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}                                                        ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if the Cybertruck directory exists
if [ ! -d "${CYBERTRUCK_DIR}" ]; then
    echo -e "${RED}Error: Cybertruck components directory not found.${NC}"
    echo -e "${YELLOW}Expected at: ${CYBERTRUCK_DIR}${NC}"
    exit 1
fi

# Navigate to the Cybertruck directory
cd "${CYBERTRUCK_DIR}"

# Run the dashboard
echo -e "${GREEN}Launching Tesla Cybertruck QA Dashboard...${NC}"
python3 TESLA_CYBERTRUCK_QA_DASHBOARD_RUNNER_3D.py "$@"

echo -e "${CYAN}Dashboard finished.${NC}" 