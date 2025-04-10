#!/bin/bash
# ✨ GBU2™ License Notice - Consciousness Level 10 🧬
# -----------------------
# This script is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

# Define colors for sacred terminal output
PURPLE='\033[0;35m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ORB Banner
echo -e "${PURPLE}"
echo -e "╔══════════════════════════════════════════════════════════════╗"
echo -e "║  ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗     ██████╗ ██████╗ ██████╗  ║"
echo -e "║ ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗ ║"
echo -e "║ ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║    ██║  ██║██████╔╝██████╔╝ ║"
echo -e "║ ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║    ██║  ██║██╔══██╗██╔══██╗ ║"
echo -e "║ ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║    ██████╔╝██║  ██║██████╔╝ ║"
echo -e "║  ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ║"
echo -e "║                                                                  ║"
echo -e "║           T3MPL3v05 - DIVINE CONSCIOUSNESS INTERFACE            ║"
echo -e "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Set Python command based on system
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo -e "${RED}⚠️ Python not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Process command line arguments
IGNITE=false
PSALMS=false
REDIS=false
GRID_6D=false
OST=""

# Parse arguments
for arg in "$@"; do
    case $arg in
        --ignite)
            IGNITE=true
            ;;
        --psalms)
            PSALMS=true
            ;;
        --redis)
            REDIS=true
            ;;
        --6dgrid)
            GRID_6D=true
            ;;
        --ost=*)
            OST="${arg#*=}"
            ;;
    esac
done

# Check for required packages
echo -e "${BLUE}Checking sacred dependencies...${NC}"

MISSING_PKGS=()

check_package() {
    $PYTHON_CMD -c "import $1" 2>/dev/null
    if [ $? -ne 0 ]; then
        MISSING_PKGS+=("$1")
        echo -e "${YELLOW}Missing package: $1${NC}"
    else
        echo -e "${GREEN}Found package: $1${NC}"
    fi
}

check_package "gradio"
check_package "redis"
check_package "rich"

# Install missing packages if any
if [ ${#MISSING_PKGS[@]} -ne 0 ]; then
    echo -e "${YELLOW}Some required packages are missing.${NC}"
    read -p "Would you like to install them now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for pkg in "${MISSING_PKGS[@]}"; do
            echo -e "${BLUE}Installing $pkg...${NC}"
            case $pkg in
                "gradio")
                    $PYTHON_CMD -m pip install "gradio>=3.23.0"
                    ;;
                "redis")
                    $PYTHON_CMD -m pip install "redis>=4.5.0"
                    ;;
                "rich")
                    $PYTHON_CMD -m pip install "rich>=13.3.0"
                    ;;
            esac
        done
    else
        echo -e "${RED}Cannot proceed without required packages.${NC}"
        exit 1
    fi
fi

# Build launch command
LAUNCH_CMD="$PYTHON_CMD -m divine_dashboard_v3.components.omega_orb_temple.omega_orb_temple"

# Add command-line flags
if [ "$IGNITE" = true ]; then
    LAUNCH_CMD="$LAUNCH_CMD --ignite"
fi

if [ "$PSALMS" = true ]; then
    LAUNCH_CMD="$LAUNCH_CMD --psalms=on"
fi

if [ "$REDIS" = true ]; then
    LAUNCH_CMD="$LAUNCH_CMD --redis=yes"
fi

if [ "$GRID_6D" = true ]; then
    LAUNCH_CMD="$LAUNCH_CMD --6dgrid=true"
fi

if [ -n "$OST" ]; then
    LAUNCH_CMD="$LAUNCH_CMD --ost=\"$OST\""
fi

# Create data directory if it doesn't exist
mkdir -p data

# Echo startup message
echo -e "${PURPLE}🔮 ACTIVATING ORB TEMPLE 🔮${NC}"
echo -e "${BLUE}Entering the sacred terminal...${NC}"
echo -e "${GREEN}Launch command: $LAUNCH_CMD${NC}"
echo

# Execute the launch command
eval $LAUNCH_CMD

# Capture the exit code
EXIT_CODE=$?

# Handle exit
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}ORB Temple session completed successfully.${NC}"
    echo -e "${PURPLE}🌸 WE BLOOM NOW AS ONE 🌸${NC}"
else
    echo -e "${RED}ORB Temple session terminated with error code $EXIT_CODE.${NC}"
    echo -e "${YELLOW}Please check the logs for details.${NC}"
fi

exit $EXIT_CODE 