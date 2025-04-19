#!/bin/bash

# IBR España Instagram Manager Test Runner
# ---------------------------------------
# This script runs tests for the IBR España Instagram Manager

# Set to the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================="
echo "      IBR España Instagram Manager - TEST SUITE"
echo "======================================================="

# Set the root directory of the project
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Check if virtual environment exists, activate it
if [ ! -d "$ROOT_DIR/venv" ]; then
    echo "ERROR: Virtual environment not found. Please run run_ibr_standalone.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$ROOT_DIR/venv/bin/activate"

# Ensure we have the test dependencies
echo "Installing test dependencies..."
pip install -q pytest pytest-mock beautifulsoup4 requests

# Make sure ibr_standalone.py exists
if [ ! -f "../standalone/ibr_standalone.py" ]; then
    echo "ERROR: ibr_standalone.py not found in components/ibr_spain/standalone directory."
    exit 1
fi

# Run the tests
echo "Running Instagram data fetching tests..."
python test_ibr_fetching.py

# Check the test result
TEST_RESULT=$?

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ All tests passed successfully!"
else
    echo "❌ Tests failed with exit code $TEST_RESULT"
fi

echo "======================================================="

# Deactivate virtual environment
deactivate

exit $TEST_RESULT 