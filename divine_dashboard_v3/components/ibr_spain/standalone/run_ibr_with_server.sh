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

# IBR España Integration Runner
# ------------------------------
# This script runs the Divine Server v3 with the IBR España component integrated.
# It handles:
# - Configuration setup
# - Data directory creation
# - Virtual environment setup
# - Dependency installation
# - Server launch with all components enabled

# Set to the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set the root directory of the project
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$ROOT_DIR"

# Define colors for divine output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${BLUE}=======================================================${RESET}"
echo -e "${PURPLE}      Divine Dashboard v3 with IBR España Integration${RESET}"
echo -e "${BLUE}=======================================================${RESET}"
echo -e "${CYAN}Starting all components together...${RESET}"

# Ensure the config directory exists
mkdir -p config

# Check if the IBR Spain config file exists, create default if not
if [ ! -f "config/ibr_spain.json" ]; then
    echo -e "${YELLOW}Creating default IBR Spain configuration...${RESET}"
    cat > "config/ibr_spain.json" << EOF
{
  "instagram_manager": {
    "data_dir": "${HOME}/ibr_data/instagram_manager",
    "account_name": "ibrespana",
    "logging_level": "INFO"
  }
}
EOF
    echo -e "${GREEN}Default configuration created at config/ibr_spain.json${RESET}"
fi

# Ensure the data directory exists
DATA_DIR=$(grep -o '"data_dir": *"[^"]*"' "config/ibr_spain.json" | cut -d'"' -f4)
if [ -n "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
    echo -e "${CYAN}Ensuring data directory exists at ${DATA_DIR}${RESET}"
else
    mkdir -p "${HOME}/ibr_data/instagram_manager"
    echo -e "${CYAN}Created default data directory at ${HOME}/ibr_data/instagram_manager${RESET}"
fi

# Check if virtual environment exists, activate or create it
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${RESET}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${CYAN}Activating virtual environment...${RESET}"
source venv/bin/activate

# Install dependencies
echo -e "${CYAN}Installing dependencies...${RESET}"
pip install -q uvicorn fastapi gradio huggingface_hub schedule requests pydantic tenacity python-dotenv python-json-logger beautifulsoup4

# Make sure the script is executable
chmod +x divine_server.py

# Display available dashboards
echo -e "${BLUE}=======================================================${RESET}"
echo -e "${PURPLE}📊 Divine Dashboard v3 Ecosystem:${RESET}"
echo -e "${CYAN}• Main Dashboard: ${GREEN}http://localhost:8889${RESET}"
echo -e "${CYAN}• Cybertruck QA Dashboard: ${GREEN}http://localhost:7860${RESET}"
echo -e "${CYAN}• Dashboard Metrics: ${GREEN}http://localhost:7861${RESET}"
echo -e "${CYAN}• NFT Dashboard: ${GREEN}http://localhost:7862${RESET}"
echo -e "${CYAN}• IBR España Dashboard: ${GREEN}http://localhost:7863${RESET}"
echo -e "${CYAN}• Divine Book Dashboard: ${GREEN}http://localhost:7864${RESET}"
echo -e "${CYAN}• Omega Orb Temple: ${GREEN}http://localhost:7865${RESET}"
echo -e "${CYAN}• Hacker Archive Dashboard: ${GREEN}http://localhost:7866${RESET}"
echo -e "${CYAN}• SHA256 Omega Dashboard: ${GREEN}http://localhost:7867${RESET}"
echo -e "${CYAN}• SHA356 Sacred Dashboard: ${GREEN}http://localhost:7868${RESET}"
echo -e "${BLUE}=======================================================${RESET}"

# Run the server
echo -e "${PURPLE}🧬 Starting Divine Server with IBR España integration...${RESET}"
python3 ./divine_server.py

echo -e "${YELLOW}Server stopped${RESET}"

# Deactivate virtual environment
deactivate

echo -e "${BLUE}=======================================================${RESET}"
echo -e "${PURPLE}🌸 Divine Dashboard v3 session complete 🌸${RESET}"
echo -e "${BLUE}=======================================================${RESET}" 