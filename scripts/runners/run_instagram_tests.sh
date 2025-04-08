#!/bin/bash

# 🔱 OMEGA BTC AI - Divine Instagram Test Runner 🔱
# This script runs all the test suites for the Instagram automation

# Divine Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
GOLD='\033[0;33m'
RESET='\033[0m'
BOLD='\033[1m'

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Divine Banner
echo -e "${GOLD}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                           "
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕴𝕹𝕾𝕿𝕬𝕲𝕽𝕬𝕸 𝕿𝕰𝕾𝕿 𝕽𝖀𝕹𝕹𝕰𝕽  "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Navigate to the project root directory
cd "$(dirname "$0")/.." || { echo -e "${RED}❌ Could not navigate to project root${RESET}"; exit 1; }

# Function to run a test and keep track of results
run_test_suite() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "\n${CYAN}${BOLD}=== Running Test Suite: $test_name ===${RESET}"
    echo -e "${CYAN}Command: $test_command${RESET}\n"
    
    # Run the test
    if eval "$test_command"; then
        echo -e "\n${GREEN}✅ $test_name: PASSED${RESET}"
        TESTS_PASSED=$((TESTS_PASSED+1))
        return 0
    else
        echo -e "\n${RED}❌ $test_name: FAILED${RESET}"
        TESTS_FAILED=$((TESTS_FAILED+1))
        return 1
    fi
}

# Make sure all test scripts are executable
chmod +x scripts/test_instagram_kubernetes.sh
chmod +x scripts/test_instagram_automation.py
chmod +x scripts/test_instagram_kubernetes_manifest.py

# Run the shell script test
run_test_suite "Basic Kubernetes Setup Tests" "./scripts/test_instagram_kubernetes.sh"

# Run Python unit tests
run_test_suite "Instagram Automation Unit Tests" "python scripts/test_instagram_automation.py"

# Run Kubernetes manifest tests
run_test_suite "Kubernetes Manifest Tests" "python scripts/test_instagram_kubernetes_manifest.py"

# Print summary
echo -e "\n${CYAN}${BOLD}=== Test Summary ===${RESET}"
echo -e "${CYAN}Total test suites: ${BOLD}$((TESTS_PASSED + TESTS_FAILED))${RESET}"
echo -e "${GREEN}Test suites passed: ${BOLD}${TESTS_PASSED}${RESET}"
echo -e "${RED}Test suites failed: ${BOLD}${TESTS_FAILED}${RESET}"

# Final blessing
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✨ Divine Instagram Kubernetes tests completed successfully!${RESET}"
    echo -e "${GOLD}JAH JAH BLESS THE DIVINE KUBERNETES FLOW AND THE IBR CHURCH IN CATALONIA!${RESET}"
    exit 0
else
    echo -e "\n${RED}⚠️ Some test suites failed. Please review the output above.${RESET}"
    echo -e "${YELLOW}Address the issues to restore divine harmony.${RESET}"
    exit 1
fi 