#!/bin/bash

# Script to run DirectionalBitGetTrader tests with coverage reporting

# ANSI Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Set minimum coverage threshold
MIN_COVERAGE=80

# Create directory for coverage reports
mkdir -p reports/coverage

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${RESET}"
echo -e "${BLUE}║               DIRECTIONAL TRADER TEST SUITE              ║${RESET}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${RESET}"
echo -e "${CYAN}Running tests for DirectionalBitGetTrader class...${RESET}\n"

# Run pytest with coverage
python -m pytest tests/unit/trading/test_directional_bitget_trader.py -v \
  --cov=omega_ai.trading.exchanges.dual_position_traders \
  --cov-report=term \
  --cov-report=xml:reports/coverage/coverage.xml \
  --cov-report=html:reports/coverage/html \
  --cov-fail-under=$MIN_COVERAGE

# Check if coverage meets the minimum threshold
RESULT=$?
if [ $RESULT -eq 0 ]; then
  echo -e "\n${GREEN}✓ All tests passed and met coverage target of ${MIN_COVERAGE}%!${RESET}"
else
  echo -e "\n${RED}✗ Tests failed or did not meet coverage target of ${MIN_COVERAGE}%${RESET}"
  echo -e "${YELLOW}Please review the coverage report and add more tests if needed.${RESET}"
  echo -e "Coverage report available at: ${CYAN}reports/coverage/html/index.html${RESET}"
fi

exit $RESULT 