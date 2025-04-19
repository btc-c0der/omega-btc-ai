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

# Simple script to run CyBer1t4L directly in the current terminal

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go to the project root directory
cd "$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")" || exit 1

# Get mode from command line argument, default to "coverage" if not provided
MODE="${1:-coverage}"

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       ${GREEN}CyBer1t4L QA Bot Direct Launcher${BLUE}               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"

# Kill any existing CyBer1t4L processes
echo -e "${YELLOW}Killing any existing CyBer1t4L processes...${NC}"
pkill -f "python.*cyber1t4l_qa_bot.py" || true

# Display current environment
echo -e "${GREEN}Current directory:${NC} $(pwd)"
echo -e "${GREEN}Python executable:${NC} $(which python)"
echo -e "${GREEN}Running in mode:${NC} ${YELLOW}${MODE}${NC}"

echo -e "${GREEN}Starting CyBer1t4L bot in foreground mode...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the bot${NC}"
echo ""

# Run the bot directly with the specified mode
python -m src.omega_bot_farm.qa.cyber1t4l_qa_bot --mode=$MODE

# This line is reached when the bot is stopped
echo -e "${RED}Bot has been stopped.${NC}" 