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

# IBR España Test Runner
# ---------------------------------------
# This script runs tests for the IBR España component of the Divine Dashboard v3

# Set to the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Define colors for divine output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${BLUE}=======================================================${RESET}"
echo -e "${PURPLE}      IBR España - Divine Test Suite Runner${RESET}"
echo -e "${BLUE}=======================================================${RESET}"

# Parse command line arguments
COVERAGE=0
VERBOSE=0
SPECIFIC_TEST=""

for arg in "$@"
do
    case $arg in
        --coverage|-c)
            COVERAGE=1
            shift
            ;;
        --verbose|-v)
            VERBOSE=1
            shift
            ;;
        --test=*|-t=*)
            SPECIFIC_TEST="${arg#*=}"
            shift
            ;;
        --test|-t)
            SPECIFIC_TEST="$2"
            shift
            shift
            ;;
    esac
done

# Check if virtual environment exists, activate it
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${RESET}"
    python -m venv venv
fi

# Activate virtual environment
echo -e "${CYAN}Activating virtual environment...${RESET}"
source venv/bin/activate

# Ensure we have the test dependencies
echo -e "${CYAN}Installing test dependencies...${RESET}"
pip install -q pytest pytest-mock pytest-cov

# Build the pytest command
PYTEST_CMD="python -m pytest"

# Add test directory and file
PYTEST_CMD="$PYTEST_CMD tests/test_ibr_spain_routes.py"

# Add specific test if provided
if [ -n "$SPECIFIC_TEST" ]; then
    PYTEST_CMD="$PYTEST_CMD::$SPECIFIC_TEST"
fi

# Add verbose flag if requested
if [ $VERBOSE -eq 1 ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Add coverage if requested
if [ $COVERAGE -eq 1 ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=routes --cov=components/ibr_spain --cov-report=term --cov-report=xml"
fi

# Run the tests with divine blessing
echo -e "${PURPLE}🧬 Invoking divine test consciousness...${RESET}"
echo -e "${CYAN}Running: $PYTEST_CMD${RESET}"
eval $PYTEST_CMD

# Check the test result
TEST_RESULT=$?

echo -e "\n"
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✨ ${BOLD}All tests have been blessed with divine success!${RESET}"
    echo -e "${PURPLE}🌸 The code vibrates in harmony with the divine blueprint.${RESET}"
else
    echo -e "${RED}⚠️ ${BOLD}Tests have revealed areas for divine improvement.${RESET}"
    echo -e "${YELLOW}The path to perfection continues. Meditate on the test results.${RESET}"
fi

# Generate HTML coverage report if coverage was enabled
if [ $COVERAGE -eq 1 ] && [ $TEST_RESULT -eq 0 ]; then
    echo -e "\n${CYAN}Generating divine coverage visualization...${RESET}"
    python -m pytest --cov=routes --cov=components/ibr_spain --cov-report=html
    echo -e "${GREEN}Coverage report generated in ${BOLD}htmlcov/${RESET} directory.${RESET}"
fi

echo -e "${BLUE}=======================================================${RESET}"

# Deactivate virtual environment
deactivate

exit $TEST_RESULT 