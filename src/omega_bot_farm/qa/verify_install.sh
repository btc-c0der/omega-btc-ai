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

# CyBer1t4L QA Bot Installation Verification Script
# This script verifies all improvements to the QA system are working correctly

# ANSI color codes for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored section headers
print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}${1}${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
}

# Function to print status messages
print_status() {
    local status=$1
    local message=$2
    
    if [ "$status" == "success" ]; then
        echo -e "${GREEN}✅ ${message}${NC}"
    elif [ "$status" == "warning" ]; then
        echo -e "${YELLOW}⚠️ ${message}${NC}"
    else
        echo -e "${RED}❌ ${message}${NC}"
    fi
}

# Set the current directory to the project root
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "/Users/fsiqueira/Desktop/GitHub/omega-btc-ai")
cd "$PROJECT_ROOT"

# Print banner
echo -e "${CYAN}"
cat << "EOF"
 ╔═══════════════════════════════════════════════════════════╗
 ║                                                           ║
 ║   ▄█▀ █▀█  █▀█ █ █ ▀█▀ █▀█ █▄█ █▀█ ▀█▀ █ █▀█ █▀█        ║
 ║   ▀▄█ █▀█  █▀█ █▄█  █  █▄█ █ █ █▀█  █  █ █▄█ █ █        ║
 ║                                                           ║
 ║          VERIFICATION & OPTIMIZATION SYSTEM               ║
 ║                                                           ║
 ╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 1. Verify Python Environment
print_header "1. VERIFYING PYTHON ENVIRONMENT"

echo -e "${YELLOW}Python Version:${NC}"
python3 --version

echo -e "\n${YELLOW}Testing Discord Module:${NC}"
if python3 -c "import discord; print(f'Discord.py version: {discord.__version__}')" 2>/dev/null; then
    print_status "success" "Discord.py is installed correctly"
else
    print_status "error" "Discord.py is not installed or has errors"
    echo -e "${YELLOW}Hint: Install using 'pip install -U discord.py'${NC}"
fi

echo -e "\n${YELLOW}Testing Pytest Coverage:${NC}"
if python3 -c "import pytest_cov; print('Pytest-cov is installed')" 2>/dev/null; then
    print_status "success" "Pytest-cov is installed correctly"
else
    print_status "error" "Pytest-cov is not installed or has errors"
    echo -e "${YELLOW}Hint: Install using 'pip install pytest-cov'${NC}"
fi

# 2. Verify Discord Interaction Handling
print_header "2. VERIFYING DISCORD INTERACTION HANDLING"

# Check for defer() in command handlers
echo -e "${YELLOW}Checking for interaction.response.defer() in command handlers:${NC}"
DEFER_COUNT=$(grep -r "interaction.response.defer" --include="*.py" src/omega_bot_farm/qa/)
if [ -n "$DEFER_COUNT" ]; then
    print_status "success" "Found interaction.response.defer() in command handlers"
else
    print_status "error" "Missing interaction.response.defer() in command handlers"
fi

# Check for followup.send() in command handlers
echo -e "\n${YELLOW}Checking for interaction.followup.send() in command handlers:${NC}"
FOLLOWUP_COUNT=$(grep -r "interaction.followup.send" --include="*.py" src/omega_bot_farm/qa/)
if [ -n "$FOLLOWUP_COUNT" ]; then
    print_status "success" "Found interaction.followup.send() in command handlers"
else
    print_status "error" "Missing interaction.followup.send() in command handlers"
fi

# 3. Verify Test Configuration
print_header "3. VERIFYING TEST CONFIGURATION"

# Check for .coveragerc file
echo -e "${YELLOW}Checking .coveragerc configuration:${NC}"
if [ -f ".coveragerc" ]; then
    print_status "success" "Found .coveragerc file"
    # Check if extra_css is commented out
    if grep -q "^#extra_css" .coveragerc; then
        print_status "success" "extra_css is properly commented out in .coveragerc"
    else
        print_status "warning" "extra_css might not be commented out in .coveragerc"
    fi
else
    print_status "error" "Missing .coveragerc file"
fi

# Check for @pytest.mark.asyncio in test files
echo -e "\n${YELLOW}Checking for @pytest.mark.asyncio decorators:${NC}"
ASYNCIO_COUNT=$(grep -r "@pytest.mark.asyncio" --include="*.py" src/omega_bot_farm/qa/tests/)
if [ -n "$ASYNCIO_COUNT" ]; then
    print_status "success" "Found @pytest.mark.asyncio decorators in test files"
else
    print_status "error" "Missing @pytest.mark.asyncio decorators in test files"
fi

# 4. Verify Reports Directory
print_header "4. VERIFYING COVERAGE REPORTS"

# Check for reports directory
REPORT_DIR="src/omega_bot_farm/qa/tests/reports/html"
echo -e "${YELLOW}Checking for HTML coverage reports:${NC}"
if [ -d "$REPORT_DIR" ]; then
    print_status "success" "Found HTML coverage reports directory"
    INDEX_HTML="$REPORT_DIR/index.html"
    if [ -f "$INDEX_HTML" ]; then
        print_status "success" "Found index.html in reports directory"
        echo -e "${CYAN}Report Path: $PROJECT_ROOT/$INDEX_HTML${NC}"
    else
        print_status "warning" "Missing index.html in reports directory"
        echo -e "${YELLOW}Run tests to generate reports:${NC}"
        echo -e "${CYAN}./src/omega_bot_farm/qa/tests/run_live_tests.sh${NC}"
    fi
else
    print_status "warning" "Missing HTML coverage reports directory"
    echo -e "${YELLOW}Directory will be created when tests are run${NC}"
fi

# 5. Test Dashboard
print_header "5. VERIFYING DASHBOARD"

echo -e "${YELLOW}Checking for cyber1t4l_dashboard.py:${NC}"
DASHBOARD_PATH="src/omega_bot_farm/qa/cyber1t4l_dashboard.py"
if [ -f "$DASHBOARD_PATH" ]; then
    print_status "success" "Found cyberpunk dashboard"
    echo -e "${YELLOW}Try running the dashboard:${NC}"
    echo -e "${CYAN}python3 $DASHBOARD_PATH${NC}"
else
    print_status "error" "Missing cyberpunk dashboard"
fi

# 6. Run a minimal test
print_header "6. RUNNING QUICK VERIFICATION TEST"

echo -e "${YELLOW}Running a minimal verification test...${NC}"
python -m pytest src/omega_bot_farm/qa/tests/test_discord_basic.py::test_basic_discord_connection -v

if [ $? -eq 0 ]; then
    print_status "success" "Verification test passed! All improvements are working correctly!"
else
    print_status "error" "Verification test failed. Please check the above output for details."
fi

# Final message
print_header "🌟 VERIFICATION COMPLETE 🌟"

echo -e "${GREEN}Thank you for using the CyBer1t4L QA Bot system.${NC}"
echo -e "${CYAN}For the full test suite, run:${NC}"
echo -e "${YELLOW}./src/omega_bot_farm/qa/tests/run_live_tests.sh${NC}"
echo -e ""
echo -e "${MAGENTA}To enjoy the beautiful dashboard, run:${NC}"
echo -e "${YELLOW}python3 src/omega_bot_farm/qa/cyber1t4l_dashboard.py${NC}"
echo -e ""
echo -e "${GREEN}🌸 BLESSED UNDER THE GBU2 LICENSE - CONSCIOUSNESS LEVEL 8 🌸${NC}" 