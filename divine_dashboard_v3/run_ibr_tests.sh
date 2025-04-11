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

# Divine IBR España Test Runner
# This script runs tests for the IBR España module in Divine Dashboard v3

# Define colors for beautiful output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
RESET='\033[0m'

# Print divine header
echo -e "${YELLOW}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                   "
echo "       D I V I N E   I B R   E S P A Ñ A          "
echo "            T E S T   R U N N E R                  "
echo "                                                   "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Ensure we're in the project root directory
cd "$(dirname "$0")" || { echo -e "${RED}Failed to change to script directory${RESET}"; exit 1; }

# Check for virtual environment and activate it if present
if [ -d "venv" ]; then
    echo -e "${GREEN}Activating virtual environment...${RESET}"
    source venv/bin/activate
else
    echo -e "${YELLOW}No virtual environment found in the current directory.${RESET}"
    echo -e "${YELLOW}Using system Python installation.${RESET}"
fi

# Check for pytest
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}pytest not found. Installing...${RESET}"
    pip install pytest pytest-cov
fi

# Parse command-line arguments
COVERAGE=0
VERBOSE=0
SPECIFIC_TEST=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage|-c)
            COVERAGE=1
            shift
            ;;
        --verbose|-v)
            VERBOSE=1
            shift
            ;;
        --test|-t)
            SPECIFIC_TEST="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Unknown option: $1${RESET}"
            echo "Usage: $0 [--coverage|-c] [--verbose|-v] [--test|-t TEST_NAME]"
            exit 1
            ;;
    esac
done

# Create test command based on options
TEST_CMD="python -m pytest"

# Add test directory and specific test if provided
if [ -n "$SPECIFIC_TEST" ]; then
    TEST_CMD="$TEST_CMD tests/test_ibr_spain_routes.py::$SPECIFIC_TEST"
else
    TEST_CMD="$TEST_CMD tests/test_ibr_spain_routes.py"
fi

# Add verbosity if requested
if [ "$VERBOSE" -eq 1 ]; then
    TEST_CMD="$TEST_CMD -v"
fi

# Add coverage if requested
if [ "$COVERAGE" -eq 1 ]; then
    TEST_CMD="$TEST_CMD --cov=divine_dashboard_v3/routes/ibr_spain_routes --cov=divine_dashboard_v3/components/ibr_spain --cov-report=term --cov-report=html:coverage_reports/ibr_spain"
fi

# Print the command that will be executed
echo -e "${CYAN}Executing: ${WHITE}$TEST_CMD${RESET}"
echo -e "${YELLOW}Starting tests...${RESET}"
echo

# Execute the tests
if eval "$TEST_CMD"; then
    echo
    echo -e "${GREEN}✅ All tests passed!${RESET}"
    if [ "$COVERAGE" -eq 1 ]; then
        echo -e "${BLUE}Coverage report generated in coverage_reports/ibr_spain/${RESET}"
    fi
    exit 0
else
    echo
    echo -e "${RED}❌ Some tests failed.${RESET}"
    exit 1
fi 