#!/bin/bash

# OMEGA Grid Portal - Installation Script
# =======================================
# Installs all requirements for the OMEGA Grid Portal
# Copyright (c) 2024 OMEGA BTC AI
# Licensed under GBU2 License

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RESET='\033[0m'
BOLD='\033[1m'

echo -e "${CYAN}${BOLD}===== OMEGA GRID PORTAL - INSTALLATION SCRIPT =====${RESET}"
echo -e "${CYAN}Installing dependencies for OMEGA Grid Portal...${RESET}"

# Check for Python installation
echo -e "${CYAN}Checking for Python...${RESET}"
if command -v python3 &>/dev/null; then
    PYTHON="python3"
    echo -e "${GREEN}Python 3 found!${RESET}"
else
    if command -v python &>/dev/null; then
        PYTHON="python"
        echo -e "${YELLOW}Python 3 not found, using default Python.${RESET}"
    else
        echo -e "${RED}Python not found. Please install Python 3.${RESET}"
        exit 1
    fi
fi

# Check for pip
echo -e "${CYAN}Checking for pip...${RESET}"
if command -v pip3 &>/dev/null; then
    PIP="pip3"
    echo -e "${GREEN}pip3 found!${RESET}"
elif command -v pip &>/dev/null; then
    PIP="pip"
    echo -e "${GREEN}pip found!${RESET}"
else
    echo -e "${RED}pip not found. Please install pip.${RESET}"
    exit 1
fi

# Function to check if virtual environment exists
check_venv() {
    if [ -d "venv" ]; then
        return 0
    else
        return 1
    fi
}

# Create virtual environment if it doesn't exist
if ! check_venv; then
    echo -e "${CYAN}Creating virtual environment...${RESET}"
    $PYTHON -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment. Please install venv:${RESET}"
        echo -e "${YELLOW}$PIP install virtualenv${RESET}"
        exit 1
    fi
    echo -e "${GREEN}Virtual environment created!${RESET}"
else
    echo -e "${GREEN}Virtual environment already exists.${RESET}"
fi

# Activate virtual environment
echo -e "${CYAN}Activating virtual environment...${RESET}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# First handle Flask compatibility issues
echo -e "${CYAN}Handling dependency compatibility...${RESET}"

# Check if dash is installed
$PIP list | grep -q "dash"
if [ $? -eq 0 ]; then
    echo -e "${YELLOW}Dash found. Ensuring compatible Flask and Werkzeug versions...${RESET}"
    # Uninstall Flask and Werkzeug first to avoid conflicts
    $PIP uninstall -y flask werkzeug &>/dev/null
    # Install compatible versions
    $PIP install flask<3.1 werkzeug<3.1 &>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Warning: Could not install compatible Flask version.${RESET}"
        echo -e "${YELLOW}You may need to manually fix dependencies with:${RESET}"
        echo -e "${YELLOW}$PIP install flask<3.1 werkzeug<3.1 --force-reinstall${RESET}"
    else
        echo -e "${GREEN}Compatible Flask and Werkzeug installed!${RESET}"
    fi
else
    # If no dash, we can use the latest Flask
    $PIP uninstall -y flask werkzeug &>/dev/null
fi

# Install requirements
echo -e "${CYAN}Installing Python requirements...${RESET}"
$PIP install --upgrade pip &>/dev/null
$PIP install redis flask streamlit ccxt discord.py python-dotenv blessed requests pandas numpy 2>&1 | tee install_log.txt

# Check for errors in the install log
if grep -q "ERROR:" install_log.txt; then
    echo -e "${YELLOW}Some packages had installation issues. Attempting fixes...${RESET}"
    
    # Check if there were Flask/Werkzeug conflicts
    if grep -q "dash.*requires.*Flask" install_log.txt || grep -q "dash.*requires.*Werkzeug" install_log.txt; then
        echo -e "${YELLOW}Fixing Flask/Werkzeug compatibility for Dash...${RESET}"
        $PIP install flask<3.1 werkzeug<3.1 --force-reinstall &>/dev/null
        echo -e "${GREEN}Fixed Flask and Werkzeug versions for Dash compatibility.${RESET}"
    fi
    
    # Check for other common errors and try to fix them
    if grep -q "ccxt" install_log.txt; then
        echo -e "${YELLOW}Fixing ccxt installation...${RESET}"
        $PIP uninstall -y ccxt &>/dev/null
        $PIP install ccxt --no-cache-dir &>/dev/null
    fi
else
    echo -e "${GREEN}All packages installed successfully!${RESET}"
fi

# Install optional requirements
echo -e "${CYAN}Installing optional packages...${RESET}"
$PIP install plotly websockets aiohttp matplotlib &>/dev/null

# Cleanup temporary files
rm -f install_log.txt &>/dev/null

# Check for Redis
echo -e "${CYAN}Checking for Redis...${RESET}"
if command -v redis-server &>/dev/null; then
    echo -e "${GREEN}Redis is already installed.${RESET}"
else
    echo -e "${YELLOW}Redis not found. Attempting to install...${RESET}"
    
    # Check the OS type
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &>/dev/null; then
            echo -e "${CYAN}Installing Redis using Homebrew...${RESET}"
            brew install redis &>/dev/null
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Redis installed successfully!${RESET}"
            else
                echo -e "${RED}Failed to install Redis. Please install manually:${RESET}"
                echo -e "${YELLOW}brew install redis${RESET}"
            fi
        else
            echo -e "${RED}Homebrew not found. Please install Redis manually:${RESET}"
            echo -e "${YELLOW}brew install redis${RESET}"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &>/dev/null; then
            echo -e "${CYAN}Installing Redis using apt-get...${RESET}"
            sudo apt-get update &>/dev/null
            sudo apt-get install -y redis-server &>/dev/null
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Redis installed successfully!${RESET}"
            else
                echo -e "${RED}Failed to install Redis. Please install manually.${RESET}"
            fi
        elif command -v yum &>/dev/null; then
            echo -e "${CYAN}Installing Redis using yum...${RESET}"
            sudo yum install -y redis &>/dev/null
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Redis installed successfully!${RESET}"
            else
                echo -e "${RED}Failed to install Redis. Please install manually.${RESET}"
            fi
        else
            echo -e "${RED}Package manager not found. Please install Redis manually.${RESET}"
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        echo -e "${RED}Automatic Redis installation not supported on Windows.${RESET}"
        echo -e "${YELLOW}Please download Redis for Windows from:${RESET}"
        echo -e "${YELLOW}https://github.com/microsoftarchive/redis/releases${RESET}"
    fi
fi

# Make scripts executable
echo -e "${CYAN}Making scripts executable...${RESET}"
chmod +x $(dirname "$0")/omega_grid_portal.py
chmod +x $(dirname "$0")/simple_portal_launcher.py
if [ -f "$(dirname "$0")/run_grid_portal.sh" ]; then
    chmod +x $(dirname "$0")/run_grid_portal.sh
fi

echo -e "${GREEN}${BOLD}Installation complete!${RESET}"
echo -e "${CYAN}You can now run the OMEGA Grid Portal:${RESET}"
echo -e "${YELLOW}cd $(dirname "$0") && ./simple_portal_launcher.py${RESET}"
echo -e "\n${CYAN}Or use the command-line interface:${RESET}"
echo -e "${YELLOW}cd $(dirname "$0") && ./omega_grid_portal.py --mode 5d${RESET}"
echo -e "\n${GREEN}JAH BLESS!${RESET}"

exit 0 