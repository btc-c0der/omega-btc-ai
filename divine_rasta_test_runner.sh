#!/bin/bash

# DIVINE RASTA TEST RUNNER
# Executes tests with JAH BLESSING and generates reports

# Terminal colors for spiritual output
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
RESET="\033[0m"

echo -e "${GREEN}=====================================================${RESET}"
echo -e "${GREEN}           OMEGA BTC AI - DIVINE TEST RUNNER          ${RESET}"
echo -e "${GREEN}           JAH BLESS THE RIGHTEOUS TESTS!            ${RESET}"
echo -e "${GREEN}=====================================================${RESET}"

# Create reports directory
mkdir -p reports

# Run tests with coverage and generate JSON report
echo -e "\n${YELLOW}🔥 Running divine tests with coverage...${RESET}"
python -m pytest omega_ai/tests/ \
    --cov=omega_ai \
    --cov-report=xml \
    --cov-report=html \
    --html=reports/report.html \
    -v \
    --json-report --json-report-file=reports/pytest.json

# Check test result
TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "\n${GREEN}✅ JAH BLESS! All tests passed with divine harmony!${RESET}"
else
    echo -e "\n${RED}❌ Some tests failed! Seek divine guidance to resolve issues.${RESET}"
fi

# Generate divine dashboard
echo -e "\n${YELLOW}📊 Generating divine test dashboard...${RESET}"
python scripts/generate_divine_dashboard.py

# Display coverage and test counts
COV_PERCENT=$(grep -o 'line-rate="[0-9.]*"' coverage.xml | grep -o '[0-9.]*' | awk '{print $1 * 100}')
TOTAL_TESTS=$(grep -o '<testsuite.*tests="[0-9]*"' reports/report.html | grep -o 'tests="[0-9]*"' | grep -o '[0-9]*')
PASSED_TESTS=$(grep -o 'passed="[0-9]*"' reports/report.html | grep -o '[0-9]*')

echo -e "\n${YELLOW}=====================================================${RESET}"
echo -e "${GREEN}DIVINE TEST METRICS WITH JAH BLESSING:${RESET}"
echo -e "${GREEN}✓ Code Coverage: ${COV_PERCENT:.1f}%${RESET}"
echo -e "${GREEN}✓ Tests Run: ${TOTAL_TESTS}${RESET}"
echo -e "${GREEN}✓ Tests Passed: ${PASSED_TESTS}${RESET}"
echo -e "${YELLOW}=====================================================${RESET}"

echo -e "\n${GREEN}🙏 View divine test dashboard at: reports/divine_dashboard.html${RESET}"
echo -e "${GREEN}🙏 View detailed HTML report at: reports/report.html${RESET}"
echo -e "${GREEN}🙏 View coverage report at: htmlcov/index.html${RESET}"

echo -e "\n${YELLOW}ONE LOVE, ONE HEART, ONE CODE${RESET}"

# Exit with test result code
exit $TEST_RESULT