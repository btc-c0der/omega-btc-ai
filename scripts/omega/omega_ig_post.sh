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


# 🔱 OMEGA BTC AI - Divine Instagram Post Helper 🔱
# This script makes it easy to post to Instagram using the omega_ig_automation.py script

# Divine Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
GOLD='\033[0;33m'
RESET='\033[0m'
BOLD='\033[1m'

# Divine Banner
echo -e "${GOLD}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                           "
echo " 𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕴𝕹𝕾𝕿𝕬𝕲𝕽𝕬𝕸 𝕬𝖀𝕿𝕺𝕸𝕬𝕿𝕴𝕺𝕹 "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Check Python and pip
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 to continue.${RESET}"
    exit 1
fi

# Define directory paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$ROOT_DIR/config"
VENV_DIR="$ROOT_DIR/.venv-ig"

# Create directories
mkdir -p "$CONFIG_DIR"
mkdir -p "$ROOT_DIR/content/images"

# Check if virtual environment exists, create if not
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${CYAN}Creating virtual environment for Instagram automation...${RESET}"
    python3 -m venv "$VENV_DIR"
    
    # Activate virtual environment and install dependencies
    source "$VENV_DIR/bin/activate"
    pip install -r "$ROOT_DIR/requirements-ig-automation.txt"
    
    echo -e "${GREEN}Virtual environment created and dependencies installed.${RESET}"
else
    # Activate existing virtual environment
    source "$VENV_DIR/bin/activate"
fi

# Function to check config
check_config() {
    CONFIG_FILE="$CONFIG_DIR/instagram_config.json"
    
    if [ -f "$CONFIG_FILE" ]; then
        # Check if username and password are still defaults
        if grep -q "YOUR_INSTAGRAM_USERNAME" "$CONFIG_FILE"; then
            echo -e "${YELLOW}⚠️ Default Instagram credentials detected in $CONFIG_FILE${RESET}"
            echo -e "${YELLOW}Please edit the config file with your Instagram credentials.${RESET}"
            edit_config
            return 1
        fi
    else
        echo -e "${YELLOW}Config file not found. Creating default config...${RESET}"
        # Run the Python script with --help to trigger config creation
        python "$ROOT_DIR/scripts/omega_ig_automation.py" --help > /dev/null
        echo -e "${YELLOW}Please edit the config file with your Instagram credentials.${RESET}"
        edit_config
        return 1
    fi
    
    return 0
}

# Function to edit config
edit_config() {
    CONFIG_FILE="$CONFIG_DIR/instagram_config.json"
    
    echo -e "${CYAN}Would you like to edit the config file now? (y/n)${RESET}"
    read -r answer
    
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        if command -v nano &> /dev/null; then
            nano "$CONFIG_FILE"
        elif command -v vim &> /dev/null; then
            vim "$CONFIG_FILE"
        else
            echo -e "${YELLOW}Please edit $CONFIG_FILE with your preferred text editor.${RESET}"
            sleep 3
            open "$CONFIG_FILE"
        fi
    else
        echo -e "${YELLOW}Please edit $CONFIG_FILE before posting to Instagram.${RESET}"
    fi
}

# Main menu function
show_menu() {
    echo -e "${CYAN}${BOLD}OMEGA BTC AI - Instagram Automation${RESET}"
    echo -e "${CYAN}Please select an option:${RESET}"
    echo -e "${YELLOW}1.${RESET} Post to Instagram now"
    echo -e "${YELLOW}2.${RESET} Schedule posts for next week"
    echo -e "${YELLOW}3.${RESET} Run daemon mode (continuous posting)"
    echo -e "${YELLOW}4.${RESET} Edit configuration"
    echo -e "${YELLOW}5.${RESET} Exit"
    
    read -r choice
    
    case "$choice" in
        1) post_now ;;
        2) schedule_posts ;;
        3) run_daemon ;;
        4) edit_config ;;
        5) exit 0 ;;
        *) echo -e "${RED}Invalid option${RESET}"; show_menu ;;
    esac
}

# Function to post immediately
post_now() {
    if check_config; then
        echo -e "${CYAN}Posting to Instagram...${RESET}"
        python "$ROOT_DIR/scripts/omega_ig_automation.py" --post
    else
        show_menu
    fi
}

# Function to schedule posts
schedule_posts() {
    if check_config; then
        echo -e "${CYAN}How many days would you like to schedule posts for? (1-30)${RESET}"
        read -r days
        
        if [[ "$days" =~ ^[0-9]+$ ]] && [ "$days" -ge 1 ] && [ "$days" -le 30 ]; then
            python "$ROOT_DIR/scripts/omega_ig_automation.py" --schedule "$days"
        else
            echo -e "${RED}Invalid number of days. Please enter a number between 1 and 30.${RESET}"
            schedule_posts
        fi
    else
        show_menu
    fi
}

# Function to run daemon
run_daemon() {
    if check_config; then
        echo -e "${CYAN}Starting Instagram posting daemon...${RESET}"
        echo -e "${YELLOW}Press Ctrl+C to stop the daemon${RESET}"
        python "$ROOT_DIR/scripts/omega_ig_automation.py" --daemon
    else
        show_menu
    fi
}

# Start the script
show_menu

# Deactivate virtual environment when done
deactivate 2>/dev/null || true

echo -e "${GOLD}JAH JAH BLESS THE DIVINE INSTAGRAM FLOW! 🔱${RESET}" 