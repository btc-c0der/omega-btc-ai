#!/bin/bash

# 🔱 OMEGA BTC AI - TMUX BTC Feed Launcher 🔱
# Sacred script for launching the divine tmux BTC feed display.

# Colors for Rasta output
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
BLUE='\033[94m'
MAGENTA='\033[95m'
CYAN='\033[96m'
RESET='\033[0m'
BOLD='\033[1m'

# Function to display Rasta banner
display_banner() {
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗"
    echo "     ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ "
    echo "    ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗"
    echo "    ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║"
    echo "    ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║"
    echo "    ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║"
    echo "     ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝"
    echo "                ${YELLOW}BTC AI SYSTEM v1.0"
    echo "     [ Rasta Price Feed - One Love - Fibonacci Aligned ]${GREEN}"
    echo "╚══════════════════════════════════════════════════════════╝${RESET}"
}

# Function to check if tmux is installed
check_tmux() {
    if ! command -v tmux &> /dev/null; then
        echo -e "${RED}❌ tmux is not installed. Please install tmux first.${RESET}"
        echo -e "${YELLOW}On macOS: brew install tmux${RESET}"
        echo -e "${YELLOW}On Ubuntu/Debian: sudo apt-get install tmux${RESET}"
        exit 1
    fi
}

# Function to check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${RESET}"
        echo -e "${YELLOW}On macOS: brew install python3${RESET}"
        echo -e "${YELLOW}On Ubuntu/Debian: sudo apt-get install python3${RESET}"
        exit 1
    fi
}

# Function to check if required Python packages are installed
check_python_packages() {
    local packages=("websocket-client" "redis" "rel" "websockets")
    local missing_packages=()
    
    for package in "${packages[@]}"; do
        if ! python3 -c "import $package" 2>/dev/null; then
            missing_packages+=("$package")
        fi
    done
    
    if [ ${#missing_packages[@]} -ne 0 ]; then
        echo -e "${YELLOW}Installing missing packages: ${missing_packages[*]}${RESET}"
        for package in "${missing_packages[@]}"; do
            python3 -m pip install "$package"
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ Successfully installed $package${RESET}"
            else
                echo -e "${RED}❌ Failed to install $package${RESET}"
                exit 1
            fi
        done
    fi
}

# Function to kill existing tmux session
kill_existing_session() {
    if tmux has-session -t omega_btc 2>/dev/null; then
        echo -e "${YELLOW}Killing existing omega_btc session...${RESET}"
        tmux kill-session -t omega_btc
        sleep 2
    fi
}

# Main execution
display_banner

# Check prerequisites
check_tmux
check_python
check_python_packages

# Kill existing session if any
kill_existing_session

# Run the tmux BTC feed display
echo -e "${BLUE}🚀 Launching divine tmux BTC feed display...${RESET}"
python3 -m omega_ai.data_feed.run_btc_feed_tmux

# Handle script interruption
trap 'echo -e "\n${YELLOW}Shutting down divine tmux session...${RESET}"; tmux kill-session -t omega_btc; echo -e "${GREEN}JAH BLESS! Session closed.${RESET}"; exit 0' INT TERM 