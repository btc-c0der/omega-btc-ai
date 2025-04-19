#!/bin/bash

# OMEGA GRID PORTAL Runner Script
# This script launches the 5D UI Dashboard for Bot Management

# Colors for terminal output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Display banner
echo -e "${MAGENTA}${BOLD}"
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                         OMEGA GRID PORTAL                             ║"
echo "║                  5D QUANTUM BOT MANAGEMENT SYSTEM                     ║"
echo "║                                                                       ║"
echo "║                     Copyright (c) 2024 OMEGA BTC AI                   ║"
echo "║                     Licensed under GBU2 License                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

# Portal script path
PORTAL_SCRIPT="$SCRIPT_DIR/omega_grid_portal.py"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. Please install Python 3 to run OMEGA Grid Portal.${NC}"
    exit 1
fi

# Parse command line arguments
MODE="5d"
SHOW_STATUS=false
BOT_TO_START=""
BOT_TO_STOP=""
BOT_TO_RESTART=""
EXPORT_STATUS=""

# Process arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --mode)
            MODE="$2"
            shift
            shift
            ;;
        --status)
            SHOW_STATUS=true
            shift
            ;;
        --start)
            BOT_TO_START="$2"
            shift
            shift
            ;;
        --stop)
            BOT_TO_STOP="$2"
            shift
            shift
            ;;
        --restart)
            BOT_TO_RESTART="$2"
            shift
            shift
            ;;
        --export-status)
            EXPORT_STATUS="$2"
            shift
            shift
            ;;
        --help)
            echo -e "${CYAN}OMEGA GRID PORTAL - Usage:${NC}"
            echo -e "  --mode [matrix|web|5d]   Dashboard mode (default: 5d)"
            echo -e "  --start BOT_NAME         Start a specific bot"
            echo -e "  --stop BOT_NAME          Stop a specific bot"
            echo -e "  --restart BOT_NAME       Restart a specific bot"
            echo -e "  --status                 Show status of all bots"
            echo -e "  --export-status FILE     Export status to a file"
            echo -e "  --help                   Show this help message"
            echo ""
            echo -e "${CYAN}Examples:${NC}"
            echo -e "  ./run_grid_portal.sh --mode matrix               # Run Matrix terminal dashboard"
            echo -e "  ./run_grid_portal.sh --status                    # Show status of all bots and services"
            exit 0
            ;;
        *)
            echo -e "${YELLOW}Unknown option: $key${NC}"
            echo -e "Use --help to see available options"
            exit 1
            ;;
    esac
done

# Build command
CMD="python3 $PORTAL_SCRIPT --mode $MODE"

if [ ! -z "$BOT_TO_START" ]; then
    CMD="$CMD --start $BOT_TO_START"
fi

if [ ! -z "$BOT_TO_STOP" ]; then
    CMD="$CMD --stop $BOT_TO_STOP"
fi

if [ ! -z "$BOT_TO_RESTART" ]; then
    CMD="$CMD --restart $BOT_TO_RESTART"
fi

if $SHOW_STATUS; then
    CMD="$CMD --status"
fi

if [ ! -z "$EXPORT_STATUS" ]; then
    CMD="$CMD --export-status $EXPORT_STATUS"
fi

# Make the script executable if it's not
if [ ! -x "$PORTAL_SCRIPT" ]; then
    chmod +x "$PORTAL_SCRIPT"
fi

echo -e "${GREEN}Launching OMEGA Grid Portal in ${BOLD}$MODE${NC}${GREEN} mode...${NC}"
echo -e "${CYAN}Command: $CMD${NC}"
echo ""

# Execute the command
eval $CMD 