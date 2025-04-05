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
#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Print header
echo -e "${BOLD}${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║   ⚛️  Quantum AI Knowledge Model - Test Runner  ⚛️          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo -e "${YELLOW}Script directory: ${SCRIPT_DIR}${NC}"

# Get project root
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")")"
echo -e "${YELLOW}Project root: ${PROJECT_ROOT}${NC}"

# Create the reports directory if it doesn't exist
REPORTS_DIR="${SCRIPT_DIR}/reports"
mkdir -p "$REPORTS_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if virtual environment exists
VENV_DIR="${SCRIPT_DIR}/../venv"
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

# Install required packages if needed
if ! python -c "import pytest" &> /dev/null || ! python -c "import psutil" &> /dev/null || ! python -c "import matplotlib" &> /dev/null; then
    echo -e "${BLUE}Installing required packages...${NC}"
    pip install pytest pytest-cov pytest-html psutil matplotlib
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install required packages.${NC}"
        exit 1
    fi
fi

# Set PYTHONPATH to include project root
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Parse command line arguments
UNIT=false
INTEGRATION=false
PERFORMANCE=false
ALL=false
COVERAGE=false
REPORT="$REPORTS_DIR/quantum_test_report_$(date +%Y%m%d_%H%M%S).json"
HTML="$REPORTS_DIR/quantum_test_report_$(date +%Y%m%d_%H%M%S)"
XML="$REPORTS_DIR/quantum_test_report_$(date +%Y%m%d_%H%M%S)"

# Parse arguments
for arg in "$@"; do
    case $arg in
        --unit)
            UNIT=true
            shift
            ;;
        --integration)
            INTEGRATION=true
            shift
            ;;
        --performance)
            PERFORMANCE=true
            shift
            ;;
        --all)
            ALL=true
            shift
            ;;
        --coverage)
            COVERAGE=true
            shift
            ;;
        --report=*)
            REPORT="${arg#*=}"
            shift
            ;;
        --html=*)
            HTML="${arg#*=}"
            shift
            ;;
        --xml=*)
            XML="${arg#*=}"
            shift
            ;;
        --help)
            echo -e "${BOLD}Usage:${NC}"
            echo "  $0 [options]"
            echo ""
            echo -e "${BOLD}Options:${NC}"
            echo "  --unit         Run unit tests only"
            echo "  --integration  Run integration tests only"
            echo "  --performance  Run performance tests only"
            echo "  --all          Run all tests (default if no other option specified)"
            echo "  --coverage     Generate coverage report"
            echo "  --report=FILE  Save test report to FILE"
            echo "  --html=PATH    Generate HTML report at PATH"
            echo "  --xml=PATH     Generate JUnit XML report at PATH"
            echo "  --help         Show this help message"
            exit 0
            ;;
        *)
            # Unknown option
            echo -e "${RED}Unknown option: $arg${NC}"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
done

# If no test type is specified, run all tests
if [ "$UNIT" = false ] && [ "$INTEGRATION" = false ] && [ "$PERFORMANCE" = false ]; then
    ALL=true
fi

# Build command
CMD="python ${SCRIPT_DIR}/run_quantum_tests.py"

if [ "$UNIT" = true ]; then
    CMD="$CMD --unit"
fi

if [ "$INTEGRATION" = true ]; then
    CMD="$CMD --integration"
fi

if [ "$PERFORMANCE" = true ]; then
    CMD="$CMD --performance"
fi

if [ "$ALL" = true ]; then
    CMD="$CMD --all"
fi

if [ "$COVERAGE" = true ]; then
    CMD="$CMD --coverage"
fi

CMD="$CMD --report=$REPORT --html=$HTML --xml=$XML"

# Run the tests
echo -e "${GREEN}Running tests with command:${NC}"
echo -e "${BLUE}$CMD${NC}"
echo ""

eval $CMD
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

# Exit with the same code as the test runner
exit $EXIT_CODE 