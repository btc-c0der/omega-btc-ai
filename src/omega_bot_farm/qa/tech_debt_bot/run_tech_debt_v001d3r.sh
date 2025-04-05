#!/bin/bash

# Run Tech Debt V001D3R - CYBERITAL™ Edition
# -----------------------------------------------------------------

# Color output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║   🧩 T3CH D3BT V001D3R - CYBERITAL™ Edition - 0m3g4_k1ng   ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
echo -e "${YELLOW}Project root: ${PROJECT_ROOT}${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if virtual environment exists
VENV_DIR="${SCRIPT_DIR}/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
source "${VENV_DIR}/bin/activate"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi

# Install requirements
echo -e "${BLUE}Installing requirements...${NC}"
pip install -r "${SCRIPT_DIR}/requirements.txt"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install requirements.${NC}"
    exit 1
fi

# Set PYTHONPATH to include project root for imports
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Parse command line arguments
DISCORD_MODE=false
WATCH_MODE=true
SCAN_ONLY=false
VERBOSE=false
CUSTOM_PATH=""
DEBUG_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -d|--discord)
            DISCORD_MODE=true
            shift
            ;;
        -w|--watch)
            WATCH_MODE=true
            shift
            ;;
        -s|--scan-only)
            SCAN_ONLY=true
            WATCH_MODE=false
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -p|--path)
            CUSTOM_PATH="$2"
            shift 2
            ;;
        --debug)
            DEBUG_MODE=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown argument: $1${NC}"
            exit 1
            ;;
    esac
done

# Check for .env file and load if it exists
ENV_FILE="${SCRIPT_DIR}/.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}Found .env file at ${ENV_FILE}${NC}"
    # Export env vars from .env file
    export $(grep -v '^#' $ENV_FILE | xargs)
else
    # Try root .env
    ROOT_ENV="${PROJECT_ROOT}/.env"
    if [ -f "$ROOT_ENV" ]; then
        echo -e "${YELLOW}No .env file in script directory. Using root .env at ${ROOT_ENV}${NC}"
        # Copy root .env to script directory
        cp "$ROOT_ENV" "$ENV_FILE"
        # Export env vars from .env file
        export $(grep -v '^#' $ROOT_ENV | xargs)
    else
        echo -e "${RED}No .env file found. Discord integration may not work.${NC}"
    fi
fi

# Debug: Check Discord environment variables
if [ "$DISCORD_MODE" = true ] || [ "$DEBUG_MODE" = true ]; then
    echo -e "${PURPLE}============ DISCORD CONFIGURATION DEBUG ============${NC}"
    
    # Check token
    TECH_DEBT_BOT_TOKEN="${TECH_DEBT_BOT_TOKEN:-}"
    TECH_DEBT_APP_ID="${TECH_DEBT_APP_ID:-}"
    
    echo -e "${BLUE}TECH_DEBT_APP_ID: ${NC}"
    if [ -n "$TECH_DEBT_APP_ID" ]; then
        echo -e "${GREEN}✅ Set to: ${TECH_DEBT_APP_ID}${NC}"
    else
        echo -e "${RED}❌ Not set${NC}"
    fi
    
    echo -e "${BLUE}TECH_DEBT_BOT_TOKEN: ${NC}"
    if [ -n "$TECH_DEBT_BOT_TOKEN" ]; then
        TOKEN_LENGTH=${#TECH_DEBT_BOT_TOKEN}
        TOKEN_START=${TECH_DEBT_BOT_TOKEN:0:10}
        TOKEN_END=${TECH_DEBT_BOT_TOKEN: -4}
        echo -e "${GREEN}✅ Set (${TOKEN_LENGTH} chars): ${TOKEN_START}...${TOKEN_END}${NC}"
    else
        echo -e "${RED}❌ Not set${NC}"
    fi
    
    # Check discord module
    echo -e "${BLUE}Checking discord module: ${NC}"
    if python3 -c "import discord; print('✅ Discord module installed')" 2>/dev/null; then
        echo -e "${GREEN}Discord module is installed${NC}"
    else
        echo -e "${RED}❌ Discord module not found. Installing...${NC}"
        pip install discord.py
    fi
    
    echo -e "${PURPLE}=================================================${NC}"
fi

# Run the voider
COMMAND="python3 ${SCRIPT_DIR}/tech_debt_v001d3r.py"

if [ "$DISCORD_MODE" = true ]; then
    COMMAND="${COMMAND} -d"
fi

if [ "$WATCH_MODE" = true ]; then
    COMMAND="${COMMAND} -w"
fi

if [ "$SCAN_ONLY" = true ]; then
    COMMAND="${COMMAND} -s"
fi

if [ "$VERBOSE" = true ]; then
    COMMAND="${COMMAND} -v"
fi

if [ -n "$CUSTOM_PATH" ]; then
    COMMAND="${COMMAND} -p \"${CUSTOM_PATH}\""
fi

echo -e "${GREEN}Starting T3CH D3BT V001D3R...${NC}"
echo -e "${BLUE}Command: ${COMMAND}${NC}"

# Run the command
eval $COMMAND

# Deactivate virtual environment when done
deactivate 