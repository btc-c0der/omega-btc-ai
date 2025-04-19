#!/bin/bash

#
# OMEGA GRID PORTAL - Virgil Abloh / OFF-WHITE™ Launcher
# =====================================================
#
# Shell script to run the OMEGA GRID PORTAL with Virgil Abloh-inspired
# design integration.
#
# Copyright (c) 2024 OMEGA BTC AI
#

# Color definitions for terminal output
GREEN="\033[92m"
YELLOW="\033[93m"
CYAN="\033[96m"
RED="\033[91m"
RESET="\033[0m"
BOLD="\033[1m"

# Display banner
echo -e "${CYAN}${BOLD}"
echo -e "    ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗     ██████╗ ██████╗ ██╗██████╗ "
echo -e "   ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗   ██╔════╝ ██╔══██╗██║██╔══██╗"
echo -e "   ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║   ██║  ███╗██████╔╝██║██║  ██║"
echo -e "   ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║   ██║   ██║██╔══██╗██║██║  ██║"
echo -e "   ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║   ╚██████╔╝██║  ██║██║██████╔╝"
echo -e "    ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ "
echo -e "${RESET}"

echo -e "${BOLD}${YELLOW}    PORTAL LAUNCHER - \"VIRGIL ABLOH\" / \"OFF-WHITE™\" EDITION${RESET}"
echo -e "${CYAN}    \"INDUSTRIAL LUXURY\" COMMAND LINE INTERFACE${RESET}"
echo -e "${BOLD}${CYAN}    \"c/o OMEGA\"     FOR \"GRID ACCESS\"     2025${RESET}"
echo -e ""

# Define paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$SCRIPT_DIR/venv"

# Check if virtual environment exists, if not create it
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}\"VIRTUAL ENVIRONMENT\"   \"NOT FOUND\"${RESET}"
    echo -e "${CYAN}\"CREATING NEW ENVIRONMENT\"   \"PLEASE WAIT\"${RESET}"
    
    # Create virtual environment
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}\"ERROR\"   \"FAILED TO CREATE VIRTUAL ENVIRONMENT\"${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}\"VIRTUAL ENVIRONMENT\"   \"CREATED SUCCESSFULLY\"${RESET}"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Install requirements
    echo -e "${CYAN}\"INSTALLING DEPENDENCIES\"   \"PLEASE WAIT\"${RESET}"
    pip install -r "$SCRIPT_DIR/divine_requirements.txt"
    
    # Install fastapi, uvicorn, and other required packages if they're not in the requirements
    pip install fastapi uvicorn jinja2 python-multipart
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}\"ERROR\"   \"FAILED TO INSTALL DEPENDENCIES\"${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}\"DEPENDENCIES\"   \"INSTALLED SUCCESSFULLY\"${RESET}"
else
    echo -e "${GREEN}\"VIRTUAL ENVIRONMENT\"   \"FOUND\"${RESET}"
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
fi

# Check if we have required packages
pip list | grep -q "fastapi"
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}\"INSTALLING FASTAPI\"   \"REQUIRED PACKAGE\"${RESET}"
    pip install fastapi uvicorn jinja2 python-multipart
fi

# Print status
echo -e "${CYAN}\"OMEGA GRID PORTAL\"   \"CONFIGURATION\"${RESET}"
echo -e "${YELLOW}\"SCRIPT DIRECTORY\"   \"$SCRIPT_DIR\"${RESET}"
echo -e "${YELLOW}\"ROOT DIRECTORY\"   \"$ROOT_DIR\"${RESET}"
echo -e "${YELLOW}\"VIRTUAL ENVIRONMENT\"   \"$VENV_DIR\"${RESET}"

# Create or ensure static and templates directories exist
mkdir -p "$SCRIPT_DIR/static/css"
mkdir -p "$SCRIPT_DIR/static/js"
mkdir -p "$SCRIPT_DIR/templates"

# Check if frontend files exist
if [ ! -f "$SCRIPT_DIR/static/js/omega-grid-virgil.js" ]; then
    echo -e "${RED}\"WARNING\"   \"FRONTEND FILES NOT FOUND\"${RESET}"
    echo -e "${YELLOW}\"RUN SETUP SCRIPT FIRST\"${RESET}"
fi

# Run the FastAPI application
echo -e "\n${GREEN}${BOLD}\"LAUNCHING OMEGA GRID PORTAL\"   \"VIRGIL ABLOH EDITION\"${RESET}"
echo -e "${CYAN}\"PRESS CTRL+C TO EXIT\"${RESET}\n"

# Uncomment the line below to run with uvicorn directly if you prefer
python "$SCRIPT_DIR/fastapi_app.py"

# For production use:
# uvicorn fastapi_app:app --host 0.0.0.0 --port 8000

echo -e "\n${RED}\"PORTAL CLOSED\"   \"GRID DISCONNECTED\"${RESET}" 