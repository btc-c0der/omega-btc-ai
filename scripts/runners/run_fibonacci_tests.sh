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