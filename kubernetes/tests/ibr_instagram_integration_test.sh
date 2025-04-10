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


# 🔱 OMEGA BTC AI - Divine IBR España Instagram Test Suite 🔱
# This script tests the IBR España Instagram integration in Kubernetes

# Divine Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
GOLD='\033[0;33m'
RESET='\033[0m'
BOLD='\033[1m'

# Test counter
PASSED=0
FAILED=0
TOTAL=0

# Divine Banner
echo -e "${GOLD}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                           "
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕴𝕭𝕽 𝕴𝕹𝕾𝕿𝕬𝕲𝕽𝕬𝕸 𝕿𝕰𝕾𝕿 𝕾𝖀𝕴𝕿𝕰  "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Helper function to run tests
run_test() {
  local test_name="$1"
  local test_command="$2"
  local test_description="$3"
  
  echo -e "${CYAN}🔍 Testing: ${BOLD}$test_name${RESET}"
  echo -e "${CYAN}   $test_description${RESET}"
  
  # Run the command and capture output
  TOTAL=$((TOTAL+1))
  if eval "$test_command" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASSED: $test_name${RESET}"
    PASSED=$((PASSED+1))
  else
    echo -e "${RED}❌ FAILED: $test_name${RESET}"
    FAILED=$((FAILED+1))
  fi
  echo
}

# Navigate to the project root directory
cd "$(dirname "$0")/../.." || { echo -e "${RED}❌ Could not navigate to project root${RESET}"; exit 1; }

# Set the namespace
NAMESPACE="ibr-spain"

# Group 1: Instagram Manifest Tests
echo -e "${YELLOW}${BOLD}=== Testing Instagram Integration Manifests ===${RESET}"

# Test 1: Instagram Connector Manifest Validation
run_test "Instagram Connector Manifest Validation" \
  "kubectl apply --dry-run=client -f kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Validating Instagram connector deployment manifest"

# Test 2: Secrets Configuration
run_test "Instagram Secrets Configuration" \
  "grep -q 'INSTAGRAM_ACCESS_TOKEN' kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Checking if Instagram secrets are defined"

# Test 3: CronJob Configuration
run_test "Instagram CronJob Configuration" \
  "grep -q 'instagram-refresh' kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Checking if Instagram refresh CronJob is configured"

# Test 4: Network Policy Configuration
run_test "Network Policy Configuration" \
  "grep -q 'NetworkPolicy' kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Checking if Network Policy is configured for Instagram connector"

# Group 2: Instagram Authentication Tests
echo -e "${YELLOW}${BOLD}=== Testing Instagram Authentication ===${RESET}"

# Test 5: Instagram Authentication Secrets
run_test "Instagram Authentication Secrets" \
  "grep -q 'INSTAGRAM_APP_SECRET' kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Checking if Instagram app secret is configured"

# Test 6: Instagram Account Configuration
run_test "Instagram Account Configuration" \
  "grep -q 'INSTAGRAM_ACCOUNT' kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Checking if Instagram account is configured as ibrespana"

# Group 3: Instagram API Functionality Tests
echo -e "${YELLOW}${BOLD}=== Testing Instagram API Functionality ===${RESET}"

# Test 7: API Integration in Frontend
run_test "Frontend Instagram Integration" \
  "grep -q 'getRecentPosts' ibr-ui/src/services/instagram.js" \
  "Checking if frontend has Instagram API integration"

# Test 8: Instagram Component Implementation
run_test "Instagram Feed Component" \
  "test -f ibr-ui/src/components/InstagramFeed.jsx" \
  "Checking if Instagram Feed component exists"

# Test 9: Instagram Service Tests
run_test "Instagram Service Tests" \
  "test -f ibr-ui/src/tests/unit/InstagramIntegration.test.js" \
  "Checking if Instagram service tests exist"

# Group 4: Cache and Performance Tests
echo -e "${YELLOW}${BOLD}=== Testing Cache and Performance Configuration ===${RESET}"

# Test 10: Redis Cache Integration
run_test "Redis Cache Integration" \
  "grep -q 'REDIS_HOST\|REDIS_PORT' kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Checking if Redis is configured for Instagram caching"

# Test 11: Cache TTL Configuration
run_test "Cache TTL Configuration" \
  "grep -q 'CACHE_TTL' kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Checking if cache TTL is configured"

# Test 12: Resource Limits
run_test "Resource Limits" \
  "grep -q 'resources\|cpu\|memory' kubernetes/ibr-spain/base/instagram-connector.yaml" \
  "Checking if resource limits are set"

# Group 5: Instagram Content Integration Tests
echo -e "${YELLOW}${BOLD}=== Testing Content Integration ===${RESET}"

# Test 13: Sermon Content Integration
run_test "Sermon Content Integration" \
  "grep -q 'getLatestSermon' ibr-ui/src/pages/Home.jsx" \
  "Checking if sermons are integrated from Instagram"

# Test 14: Scripture Content Integration
run_test "Scripture Content Integration" \
  "grep -q 'getLatestScripture' ibr-ui/src/pages/Home.jsx" \
  "Checking if scripture verses are integrated from Instagram"

# Test 15: Instagram Post Categorization
run_test "Instagram Post Categorization" \
  "grep -q 'categorizePost' ibr-ui/src/services/instagram.js" \
  "Checking if Instagram posts are categorized by content type"

# Summary
echo -e "${YELLOW}${BOLD}=== Test Summary ===${RESET}"
echo -e "${CYAN}Total tests: ${BOLD}$TOTAL${RESET}"
echo -e "${GREEN}Tests passed: ${BOLD}$PASSED${RESET}"
echo -e "${RED}Tests failed: ${BOLD}$FAILED${RESET}"

# Calculate percentage
PERCENTAGE=$(( (PASSED * 100) / TOTAL ))
echo -e "${CYAN}Test passing rate: ${BOLD}${PERCENTAGE}%${RESET}"

# Divine blessing or warning based on test results
if [ $PERCENTAGE -eq 100 ]; then
  echo -e "${GREEN}✨ Divine IBR España Instagram integration is fully blessed!${RESET}"
  echo -e "${GOLD}JAH JAH BLESS THE DIVINE FLOW OF CONTENT FROM INSTAGRAM TO IBR ESPAÑA!${RESET}"
elif [ $PERCENTAGE -ge 80 ]; then
  echo -e "${YELLOW}✨ Divine IBR España Instagram integration is mostly blessed!${RESET}"
  echo -e "${YELLOW}Consider fixing the failed tests for complete divine harmony.${RESET}"
else
  echo -e "${RED}⚠️ Divine IBR España Instagram integration needs attention!${RESET}"
  echo -e "${YELLOW}Please address the failed tests to restore divine harmony.${RESET}"
fi

# Exit with success if all tests passed, otherwise failure
if [ $FAILED -eq 0 ]; then
  exit 0
else
  exit 1
fi 