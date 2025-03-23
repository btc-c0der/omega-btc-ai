#!/bin/bash
# ========================================================
# OMEGA DEV FRAMEWORK - Divine Watcher Launcher
# ========================================================
#
# This script launches the Divine Watcher to monitor your codebase
# and automatically run the TDD Oracle when files are saved.
# For test files that pass all tests, it also creates and pushes
# a QA approved git tag with the TDD-OMEGA-QA-APPROVED suffix.
#
# Usage:
#   ./run_divine_watcher.sh [directory_to_watch]
#
# If no directory is specified, the script will watch the current directory.

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${MAGENTA}${BOLD}"
echo "============================================================"
echo "       OMEGA DEV FRAMEWORK - DIVINE WATCHER LAUNCHER        "  
echo "============================================================"
echo -e "${NC}"

# Ensure the watcher script is executable
chmod +x omega_watcher.py
chmod +x omega_tdd_oracle.py

# Get the directory to watch
WATCH_DIR="$1"
if [ -z "$WATCH_DIR" ]; then
    WATCH_DIR="."
    echo -e "${YELLOW}No directory specified. Watching current directory.${NC}"
else
    echo -e "${CYAN}Watching directory: $WATCH_DIR${NC}"
fi

# Find the tests directory if it exists
TEST_DIR=""
if [ -d "tests" ]; then
    TEST_DIR="tests"
    echo -e "${GREEN}Found tests directory: $TEST_DIR${NC}"
elif [ -d "test" ]; then
    TEST_DIR="test"
    echo -e "${GREEN}Found tests directory: $TEST_DIR${NC}"
fi

# Inform about QA tagging functionality
echo -e "${MAGENTA}${BOLD}FEATURE: Auto QA-Tagging${NC}"
echo -e "${CYAN}When test files pass all tests, a QA-approved git tag will be automatically created.${NC}"
echo -e "${CYAN}These tags follow the format: vX.Y.Z-TDD-OMEGA-QA-APPROVED-testname-N${NC}"
echo -e "${CYAN}where N is an auto-incrementing counter to prevent tag conflicts.${NC}"
echo -e "${CYAN}Tags will be pushed to origin automatically.${NC}"
echo ""

# Launch the watcher
echo -e "${YELLOW}${BOLD}Launching Divine Watcher...${NC}"
echo -e "${CYAN}Press Ctrl+C to stop the watcher${NC}"
echo ""

if [ -n "$TEST_DIR" ]; then
    ./omega_watcher.py --watch-dir "$WATCH_DIR" --test-path "$TEST_DIR"
else
    ./omega_watcher.py --watch-dir "$WATCH_DIR"
fi 