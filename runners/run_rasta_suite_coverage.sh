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


# DIVINE RASTA TEST RUNNER WITH BLESSED COVERAGE REPORTING
# JAH BLESS OUR CODE COVERAGE AND METRICS

# Terminal colors for spiritual output
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
PURPLE="\033[0;35m"
RESET="\033[0m"

echo -e "${GREEN}🌿 JAH BLESS - DIVINE RASTA TEST SUITE BEGINNING 🌿${RESET}"
echo -e "${YELLOW}ONE LOVE, ONE HEART, ONE CODE COVERAGE${RESET}\n"

# Create directory for reports
mkdir -p reports

# Run tests with coverage
python -m pytest omega_ai/tests/ \
    --cov=omega_ai \
    --cov-report=term \
    --cov-report=xml:reports/coverage.xml \
    --cov-report=html:reports/htmlcov \
    --junitxml=reports/junit.xml \
    -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ JAH BLESS! ALL TESTS PASSED WITH DIVINE HARMONY! ✅${RESET}"
else
    echo -e "\n${RED}❌ TESTS FAILED! SEEK DIVINE GUIDANCE TO RESOLVE ISSUES! ❌${RESET}"
fi

# Generate test metrics report
echo -e "\n${BLUE}📊 GENERATING DIVINE TEST METRICS REPORT 📊${RESET}"
python -m pytest_metrics omega_ai/tests/ -o reports/metrics.json

# Run Radon for code complexity metrics
echo -e "\n${PURPLE}🔍 MEASURING CODE COMPLEXITY WITH DIVINE WISDOM 🔍${RESET}"
radon cc omega_ai -a -s --md > reports/complexity.md
radon mi omega_ai --md > reports/maintainability.md

echo -e "\n${GREEN}🙏 DIVINE TEST REPORTS GENERATED WITH JAH BLESSING 🙏${RESET}"
echo -e "${YELLOW}Reports available in ./reports directory${RESET}"