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

# 
# OMEGA BTC AI - Divine BTC Date Decoder Installer
# ===============================================
#
# Installs the BTC Date Decoder CLI command globally.
#
# Copyright (C) 2024 OMEGA BTC AI Team
# License: GNU General Public License v3.0
#
# JAH BLESS the eternal flow of time and markets.

# Colors for formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RESET='\033[0m'
BOLD='\033[1m'

echo -e "${YELLOW}${BOLD}OMEGA BTC AI${RESET} - ${CYAN}${BOLD}Divine BTC Date Decoder Installer${RESET}"
echo -e "${YELLOW}JAH BLESS the eternal flow of time and markets${RESET}\n"

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Check if user has sudo privileges
check_sudo() {
    if ! command -v sudo &> /dev/null; then
        echo -e "${RED}Error: This installation requires sudo privileges but sudo is not installed.${RESET}"
        exit 1
    fi
    
    # Check if the user has sudo privileges
    if ! sudo -v; then
        echo -e "${RED}Error: You need sudo privileges to install the btcdate command globally.${RESET}"
        exit 1
    fi
}

# Install the command
install_command() {
    BTCDATE_SCRIPT="$SCRIPT_DIR/btcdate"
    INSTALL_DIR="/usr/local/bin"
    
    if [ ! -f "$BTCDATE_SCRIPT" ]; then
        echo -e "${RED}Error: Could not find btcdate script at $BTCDATE_SCRIPT${RESET}"
        exit 1
    fi
    
    # Make sure the script is executable
    chmod +x "$BTCDATE_SCRIPT"
    
    # Install the script
    echo -e "${YELLOW}Installing btcdate command to $INSTALL_DIR...${RESET}"
    sudo cp "$BTCDATE_SCRIPT" "$INSTALL_DIR/btcdate"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}${BOLD}Success!${RESET} The ${CYAN}${BOLD}btcdate${RESET} command has been installed."
        echo -e "\nUsage examples:"
        echo -e "  ${CYAN}btcdate${RESET}                    - Analyze current date"
        echo -e "  ${CYAN}btcdate 2023-10-29${RESET}         - Analyze a specific date"
        echo -e "  ${CYAN}btcdate special${RESET}            - Analyze the special Oct 29, 2023 date"
        echo -e "  ${CYAN}btcdate interactive${RESET}        - Run in interactive mode"
        echo -e "  ${CYAN}btcdate next-divine 60${RESET}     - Find divine dates in next 60 days"
        echo -e "  ${CYAN}btcdate help${RESET}               - Show full help"
        
        echo -e "\n${YELLOW}JAH JAH BLESS THE ETERNAL FLOW OF TIME AND MARKETS.${RESET}"
    else
        echo -e "${RED}Failed to install the command. Check your permissions.${RESET}"
        exit 1
    fi
}

# Check if project settings file exists
create_config() {
    CONFIG_DIR="$HOME/.config/omega-btc-ai"
    CONFIG_FILE="$CONFIG_DIR/btcdate.conf"
    
    # Create config directory if it doesn't exist
    if [ ! -d "$CONFIG_DIR" ]; then
        mkdir -p "$CONFIG_DIR"
    fi
    
    # Create config file if it doesn't exist
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${YELLOW}Creating configuration file...${RESET}"
        cat > "$CONFIG_FILE" << EOF
# OMEGA BTC AI - BTC Date Decoder Configuration
# ============================================
# 
# JAH BLESS the eternal flow of time and markets.

# Path to the OMEGA BTC AI project root
PROJECT_ROOT="$SCRIPT_DIR"

# Default search range for divine dates (in days)
DEFAULT_DIVINE_SEARCH_DAYS=30

# Minimum divine score threshold (0.0 to 1.0)
DIVINE_SCORE_THRESHOLD=0.7

# Date format for display (standard strftime format)
DATE_FORMAT="%Y-%m-%d %H:%M:%S %Z"
EOF
        echo -e "${GREEN}Configuration file created at $CONFIG_FILE${RESET}"
    else
        echo -e "${GREEN}Configuration file already exists at $CONFIG_FILE${RESET}"
    fi
}

# Main function
main() {
    echo -e "${YELLOW}This script will install the btcdate command globally.${RESET}"
    echo -e "${YELLOW}You might be asked for your password.${RESET}\n"
    
    read -p "Do you want to continue? (y/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Installation cancelled.${RESET}"
        exit 1
    fi
    
    check_sudo
    install_command
    create_config
}

# Run the main function
main 