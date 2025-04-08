#!/bin/bash

# ==================================================
# OMEGA BTC AI - Run Fibonacci Trader Tests
# ==================================================
# This script runs tests for the Fibonacci trader implementation
# with profile integration.

echo "===== Running Fibonacci Trader Tests ====="

# Run the tests with pytest
python -m pytest tests/unit/trading/test_fibonacci_profile_integration.py -v

# Check the result
if [ $? -eq 0 ]; then
  echo "✅ All Fibonacci trader tests passed successfully!"
  exit 0
else
  echo "❌ Some Fibonacci trader tests failed. Check the log above for details."
  exit 1
fi 