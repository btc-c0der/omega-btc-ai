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


# DIVINE RASTA TEST RUNNER
# Executes tests with JAH BLESSING and generates reports

# Terminal colors for spiritual output
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
BLUE="\033[94m"
RESET="\033[0m"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to display progress bar
progress_bar() {
    local duration=$1
    local width=50
    local progress=0
    local block=$((duration / width))
    local empty=$((width - block))
    
    printf "${BLUE}["
    printf "%${block}s" | tr ' ' '='
    printf "%${empty}s" | tr ' ' ' '
    printf "]${RESET}\r"
}

# Function to display help
show_help() {
    echo -e "${GREEN}=====================================================${RESET}"
    echo -e "${GREEN}           OMEGA BTC AI - DIVINE TEST RUNNER          ${RESET}"
    echo -e "${GREEN}           JAH BLESS THE RIGHTEOUS TESTS!            ${RESET}"
    echo -e "${GREEN}=====================================================${RESET}"
    echo -e "\n${YELLOW}Usage:${RESET}"
    echo -e "  $0 [options] [test_files...]"
    echo -e "\n${YELLOW}Options:${RESET}"
    echo -e "  -h, --help          Show this help message"
    echo -e "  -p, --parallel      Run tests in parallel"
    echo -e "  -t, --tag TAG       Run tests with specific tag"
    echo -e "  -c, --clean         Clean up reports and coverage files"
    echo -e "  -v, --verbose       Show verbose output"
    echo -e "\n${YELLOW}Examples:${RESET}"
    echo -e "  $0                    # Run all tests"
    echo -e "  $0 -p                 # Run tests in parallel"
    echo -e "  $0 -t integration     # Run integration tests"
    echo -e "  $0 test_rasta_vibes.py # Run specific test file"
    echo -e "  $0 -c                 # Clean up and exit"
}

# Parse command line arguments
PARALLEL=false
TAG=""
CLEAN=false
VERBOSE=false
TEST_FILES=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            TEST_FILES+=("$1")
            shift
            ;;
    esac
done

# Clean up if requested
if [ "$CLEAN" = true ]; then
    echo -e "${YELLOW}🧹 Cleaning up divine test artifacts...${RESET}"
    rm -rf reports/ coverage.xml htmlcov/ .pytest_cache/
    echo -e "${GREEN}✨ Cleanup complete!${RESET}"
    exit 0
fi

# Check for required dependencies
if ! command_exists python; then
    echo -e "${RED}❌ Python is not installed!${RESET}"
    exit 1
fi

# Install required packages
echo -e "${YELLOW}📦 Installing required packages...${RESET}"
pip install pytest pytest-cov pytest-html pytest-xdist pytest-json-report

echo -e "${GREEN}=====================================================${RESET}"
echo -e "${GREEN}           OMEGA BTC AI - DIVINE TEST RUNNER          ${RESET}"
echo -e "${GREEN}           JAH BLESS THE RIGHTEOUS TESTS!            ${RESET}"
echo -e "${GREEN}=====================================================${RESET}"

# Create reports directory
mkdir -p reports

# Build pytest command
PYTEST_CMD="python -m pytest"
if [ "$PARALLEL" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -n auto"
fi

if [ -n "$TAG" ]; then
    PYTEST_CMD="$PYTEST_CMD -m $TAG"
fi

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Add test files if specified
if [ ${#TEST_FILES[@]} -gt 0 ]; then
    PYTEST_CMD="$PYTEST_CMD ${TEST_FILES[*]}"
else
    PYTEST_CMD="$PYTEST_CMD omega_ai/tests/"
fi

# Add coverage and reporting options
PYTEST_CMD="$PYTEST_CMD --cov=omega_ai --cov-report=term-missing --cov-report=html --html=reports/report.html --json-report --json-report-file=reports/pytest.json"

# Run tests with progress indication
echo -e "\n${YELLOW}🔥 Running divine tests with coverage...${RESET}"
if [ "$VERBOSE" = true ]; then
    $PYTEST_CMD
else
    $PYTEST_CMD | while IFS= read -r line; do
        echo -e "${BLUE}$line${RESET}"
        progress_bar 1
    done
fi

# Check test result
TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "\n${GREEN}✅ JAH BLESS! All tests passed with divine harmony!${RESET}"
else
    echo -e "\n${RED}❌ Some tests failed! Seek divine guidance to resolve issues.${RESET}"
fi

# Generate divine dashboard
echo -e "\n${YELLOW}📊 Generating divine test dashboard...${RESET}"
if [ -f "scripts/generate_divine_dashboard.py" ]; then
    python scripts/generate_divine_dashboard.py
else
    echo -e "${YELLOW}⚠️  Divine dashboard generator not found. Skipping...${RESET}"
fi

# Display coverage and test counts with enhanced statistics
if [ -f "reports/report.html" ]; then
    TOTAL_TESTS=$(grep -o '<testsuite.*tests="[0-9]*"' reports/report.html | grep -o 'tests="[0-9]*"' | grep -o '[0-9]*' || echo "0")
    PASSED_TESTS=$(grep -o 'passed="[0-9]*"' reports/report.html | grep -o '[0-9]*' || echo "0")
    FAILED_TESTS=$(grep -o 'failed="[0-9]*"' reports/report.html | grep -o '[0-9]*' || echo "0")
    SKIPPED_TESTS=$(grep -o 'skipped="[0-9]*"' reports/report.html | grep -o '[0-9]*' || echo "0")
else
    TOTAL_TESTS="0"
    PASSED_TESTS="0"
    FAILED_TESTS="0"
    SKIPPED_TESTS="0"
fi

# Get coverage percentage from term-missing output
COV_PERCENT=$(python -m pytest --cov=omega_ai --cov-report=term-missing omega_ai/tests/ | grep "TOTAL" | awk '{print $4}' | sed 's/%//' || echo "0")

echo -e "\n${YELLOW}=====================================================${RESET}"
echo -e "${GREEN}DIVINE TEST METRICS WITH JAH BLESSING:${RESET}"
echo -e "${GREEN}✓ Code Coverage: ${COV_PERCENT}%${RESET}"
echo -e "${GREEN}✓ Total Tests: ${TOTAL_TESTS}${RESET}"
echo -e "${GREEN}✓ Passed: ${PASSED_TESTS}${RESET}"
echo -e "${RED}✗ Failed: ${FAILED_TESTS}${RESET}"
echo -e "${YELLOW}⚠️  Skipped: ${SKIPPED_TESTS}${RESET}"
echo -e "${YELLOW}=====================================================${RESET}"

echo -e "\n${GREEN}🙏 View divine test dashboard at: reports/divine_dashboard.html${RESET}"
echo -e "${GREEN}🙏 View detailed HTML report at: reports/report.html${RESET}"
echo -e "${GREEN}🙏 View coverage report at: htmlcov/index.html${RESET}"

echo -e "\n${YELLOW}ONE LOVE, ONE HEART, ONE CODE${RESET}"

# Exit with test result code
exit $TEST_RESULT