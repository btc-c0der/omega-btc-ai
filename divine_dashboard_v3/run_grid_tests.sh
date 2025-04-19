#!/bin/bash

#
# "TEST RUNNER" — "OMEGA GRID PORTAL"
# ==================================
#
# "VIRGIL ABLOH" / "OFF-WHITE™" INSPIRED TEST RUNNER
# SHELL SCRIPT TO RUN ALL TESTS FOR THE OMEGA GRID PORTAL
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
BLACK="\033[30m"
BG_WHITE="\033[47m"
BG_BLACK="\033[40m"
BG_YELLOW="\033[43m"

# Define paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TESTS_DIR="$SCRIPT_DIR/tests"
VENV_DIR="$SCRIPT_DIR/venv"
PYTEST="$VENV_DIR/bin/pytest"
PYTHON="$VENV_DIR/bin/python"
JEST="$SCRIPT_DIR/node_modules/.bin/jest"

# Display banner
echo -e "\n"
echo -e "${BLACK}${BOLD}${BG_YELLOW}                                                           ${RESET}"
echo -e "${BLACK}${BOLD}${BG_YELLOW}    \"OMEGA GRID PORTAL\" — \"TEST COVERAGE\"                  ${RESET}"
echo -e "${BLACK}${BOLD}${BG_YELLOW}    \"VIRGIL ABLOH\" / \"OFF-WHITE™\" INSPIRED TEST SUITE      ${RESET}"
echo -e "${BLACK}${BOLD}${BG_YELLOW}                                                           ${RESET}"
echo -e "\n"

# Check if virtual environment exists
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
else
    echo -e "${GREEN}\"VIRTUAL ENVIRONMENT\"   \"FOUND\"${RESET}"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install testing dependencies
echo -e "${CYAN}\"INSTALLING TESTING DEPENDENCIES\"   \"PLEASE WAIT\"${RESET}"
pip install pytest pytest-asyncio pytest-cov httpx

# Install Node.js dependencies if needed
if [ ! -d "$SCRIPT_DIR/node_modules" ]; then
    echo -e "${YELLOW}\"NODE MODULES\"   \"NOT FOUND\"${RESET}"
    echo -e "${CYAN}\"INSTALLING JAVASCRIPT DEPENDENCIES\"   \"PLEASE WAIT\"${RESET}"
    
    # Check for npm
    if command -v npm &> /dev/null; then
        cd "$SCRIPT_DIR" && npm install jest @testing-library/jest-dom jest-environment-jsdom babel-jest
    else
        echo -e "${RED}\"ERROR\"   \"NPM NOT FOUND, SKIPPING JAVASCRIPT TESTS\"${RESET}"
    fi
fi

# Create test directories if they don't exist
mkdir -p "$TESTS_DIR/mocks"

# Run backend tests
echo -e "\n${CYAN}${BOLD}\"RUNNING PYTHON TESTS\"   \"BACKEND COVERAGE\"${RESET}\n"

# Run each Python test file
for test_file in "$TESTS_DIR"/test_*.py; do
    if [ -f "$test_file" ]; then
        echo -e "${YELLOW}\"TESTING\"   \"$(basename "$test_file")\"${RESET}"
        $PYTHON "$test_file"
        
        # Check result
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}\"TEST PASSED\"   \"$(basename "$test_file")\"${RESET}"
        else
            echo -e "${RED}\"TEST FAILED\"   \"$(basename "$test_file")\"${RESET}"
        fi
        echo -e "---------------------------------------------"
    fi
done

# Run frontend tests if Jest is available
if [ -f "$JEST" ]; then
    echo -e "\n${CYAN}${BOLD}\"RUNNING JAVASCRIPT TESTS\"   \"FRONTEND COVERAGE\"${RESET}\n"
    cd "$SCRIPT_DIR" && $JEST --config "$TESTS_DIR/jest.config.js"
else
    echo -e "\n${YELLOW}\"SKIPPING JAVASCRIPT TESTS\"   \"JEST NOT FOUND\"${RESET}\n"
fi

# Generate coverage report
echo -e "\n${CYAN}${BOLD}\"GENERATING COVERAGE REPORT\"   \"QUALITY METRICS\"${RESET}\n"
mkdir -p "$SCRIPT_DIR/coverage_reports"
$PYTEST "$TESTS_DIR" --cov=components --cov-report=html:coverage_reports/python

# Display summary
echo -e "\n"
echo -e "${BLACK}${BOLD}${BG_WHITE}                                                           ${RESET}"
echo -e "${BLACK}${BOLD}${BG_WHITE}    \"TEST COVERAGE COMPLETE\"   \"OMEGA GRID PORTAL\"        ${RESET}"
echo -e "${BLACK}${BOLD}${BG_WHITE}                                                           ${RESET}"
echo -e "\n"
echo -e "${CYAN}\"BACKEND COVERAGE REPORT\"   \"coverage_reports/python/index.html\"${RESET}"
echo -e "${CYAN}\"FRONTEND COVERAGE REPORT\"   \"coverage/lcov-report/index.html\"${RESET}"
echo -e "\n"

# Footer
echo -e "\n"
echo -e "${BOLD}${BG_BLACK}                                                           ${RESET}"
echo -e "${BOLD}${BG_BLACK}    \"c/o OMEGA GRID\"   \"FOR TESTING PURPOSES\"            ${RESET}"
echo -e "${BOLD}${BG_BLACK}                                                           ${RESET}" 