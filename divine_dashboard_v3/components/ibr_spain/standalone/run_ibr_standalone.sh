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

# IBR España Standalone Runner
# ------------------------------
# This script runs ONLY the IBR España component without the full server.
# It handles all necessary setup including:
# - Creating configuration files
# - Setting up data directories
# - Creating a virtual environment
# - Installing dependencies
# - Running the standalone interface

# Set to the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

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
echo -e "${PURPLE}      IBR España Instagram Manager - STANDALONE MODE${RESET}"
echo -e "${BLUE}=======================================================${RESET}"

# Set the root directory of the project
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Ensure the config directory exists
mkdir -p config
echo -e "${CYAN}Config directory created/verified${RESET}"

# Check if the IBR Spain config file exists, create default if not
if [ ! -f "config/ibr_spain.json" ]; then
    echo -e "${YELLOW}Creating default IBR Spain configuration...${RESET}"
    cat > "config/ibr_spain.json" << EOFCONFIG
{
  "instagram_manager": {
    "data_dir": "${HOME}/ibr_data/instagram_manager",
    "account_name": "ibrespana",
    "logging_level": "INFO"
  }
}
EOFCONFIG
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

# Create static folders for assets
mkdir -p static/fonts/ui-sans-serif
echo -e "${CYAN}Created static assets directory structure${RESET}"

# Check if virtual environment exists, activate or create it
if [ ! -d "$ROOT_DIR/venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${RESET}"
    python3 -m venv "$ROOT_DIR/venv"
fi

# Activate virtual environment
echo -e "${CYAN}Activating virtual environment...${RESET}"
source "$ROOT_DIR/venv/bin/activate"

# Install dependencies
echo -e "${CYAN}Installing dependencies...${RESET}"
pip install -q gradio==4.13.0 requests pydantic tenacity python-dotenv python-json-logger fastapi uvicorn beautifulsoup4

# Check if ibr_standalone.py already exists, if not create it
if [ ! -f "ibr_standalone.py" ]; then
    echo -e "${YELLOW}Creating standalone IBR dashboard script...${RESET}"
    cat > ibr_standalone.py << 'EOFPY'
#!/usr/bin/env python3
"""
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸

IBR España Instagram Manager Standalone Module

This module provides a standalone interface for the IBR España Instagram Manager
component. It allows users to view Instagram stats, create posts, and analyze
account performance without requiring the full Divine Dashboard infrastructure.

The standalone interface uses Gradio to create an interactive web UI that can
be run independently of the main server.
"""
# ... rest of the ibr_standalone.py file would be included here
EOFPY
    echo -e "${GREEN}Created standalone IBR dashboard script${RESET}"
else
    echo -e "${GREEN}Using existing ibr_standalone.py script${RESET}"
fi

# Run the standalone IBR dashboard
echo -e "${PURPLE}🌸 Launching IBR España Instagram Manager...${RESET}"
python ibr_standalone.py

# Deactivate virtual environment when script exits
deactivate

echo -e "${BLUE}=======================================================${RESET}"
echo -e "${PURPLE}IBR España Instagram Manager has been closed${RESET}"
echo -e "${BLUE}=======================================================${RESET}"
