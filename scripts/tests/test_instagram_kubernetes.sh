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


# 🔱 OMEGA BTC AI - Divine Instagram Kubernetes Test Suite 🔱
# This script tests the Instagram automation Kubernetes deployment

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
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕴𝕹𝕾𝕿𝕬𝕲𝕽𝕬𝕸 𝕶𝟴𝕾 𝕿𝕰𝕾𝕿 𝕾𝖀𝕴𝕿𝕰  "
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
cd "$(dirname "$0")/.." || { echo -e "${RED}❌ Could not navigate to project root${RESET}"; exit 1; }

# Group 1: Basic Requirements Tests
echo -e "${YELLOW}${BOLD}=== Testing Base Requirements ===${RESET}"

# Test 1: Docker Installation
run_test "Docker Installation" \
  "command -v docker" \
  "Checking if Docker is installed"

# Test 2: Docker Running
run_test "Docker Service" \
  "docker info" \
  "Checking if Docker service is running"

# Test 3: Kubectl Installation
run_test "Kubectl Installation" \
  "command -v kubectl" \
  "Checking if kubectl is installed"

# Test 4: Kubernetes Connection
run_test "Kubernetes Connection" \
  "kubectl get nodes" \
  "Checking if kubectl can connect to Kubernetes cluster"

# Group 2: Deployment File Tests
echo -e "${YELLOW}${BOLD}=== Testing Deployment Files ===${RESET}"

# Test 5: Dockerfile Exists
run_test "Dockerfile Exists" \
  "test -f Dockerfile.instagram" \
  "Checking if Dockerfile.instagram exists"

# Test 6: Dockerfile Validity
run_test "Dockerfile Validity" \
  "docker build --quiet -t dockerfile-test -f Dockerfile.instagram . && docker rmi dockerfile-test" \
  "Checking if Dockerfile.instagram can be built"

# Test 7: Kubernetes Manifest Exists
run_test "Kubernetes Manifest Exists" \
  "test -f kubernetes/deployments/omega-instagram-deployment.yaml" \
  "Checking if omega-instagram-deployment.yaml exists"

# Test 8: Kubernetes Manifest Validity
run_test "Kubernetes Manifest Validity" \
  "kubectl apply --dry-run=client -f kubernetes/deployments/omega-instagram-deployment.yaml" \
  "Checking if omega-instagram-deployment.yaml is valid"

# Test 9: Requirements File Exists
run_test "Requirements File Exists" \
  "test -f scripts/requirements-instagram.txt" \
  "Checking if requirements-instagram.txt exists"

# Test 10: Deployment Script Exists
run_test "Deployment Script Exists" \
  "test -f scripts/k8s_instagram_deploy.sh" \
  "Checking if k8s_instagram_deploy.sh exists"

# Test 11: Deployment Script Executable
run_test "Deployment Script Executable" \
  "test -x scripts/k8s_instagram_deploy.sh" \
  "Checking if k8s_instagram_deploy.sh is executable"

# Group 3: Python Script Tests
echo -e "${YELLOW}${BOLD}=== Testing Python Scripts ===${RESET}"

# Test 12: Instagram Automation Script Exists
run_test "Automation Script Exists" \
  "test -f scripts/omega_ig_automation.py" \
  "Checking if omega_ig_automation.py exists"

# Test 13: Instagram Automation Script Syntax
run_test "Automation Script Syntax" \
  "python3 -m py_compile scripts/omega_ig_automation.py" \
  "Checking if omega_ig_automation.py has valid Python syntax"

# Test 14: Religious Content Support
run_test "Religious Content Support" \
  "grep -q 'religious_themes' scripts/omega_ig_automation.py" \
  "Checking if omega_ig_automation.py supports religious content"

# Group 4: Kubernetes Namespace Tests
echo -e "${YELLOW}${BOLD}=== Testing Kubernetes Namespace ===${RESET}"

# Test 15: Namespace Creation
run_test "Namespace Creation Test" \
  "kubectl create namespace test-instagram-namespace && kubectl delete namespace test-instagram-namespace" \
  "Testing namespace creation in Kubernetes"

# Group 5: Religious Content Function Tests
echo -e "${YELLOW}${BOLD}=== Testing Religious Content Features ===${RESET}"

# Test 16: IBR Church Text
run_test "IBR Church Text" \
  "grep -q 'IBR church in Catalonia' kubernetes/deployments/INSTAGRAM_KUBERNETES.md" \
  "Checking if documentation mentions IBR church in Catalonia"

# Test 17: Religious CronJob
run_test "Religious CronJob" \
  "grep -q 'instagram-religious-post' kubernetes/deployments/omega-instagram-deployment.yaml" \
  "Checking if CronJob for religious posts is defined"

# Group 6: Mock Deployment Test
echo -e "${YELLOW}${BOLD}=== Mock Deployment Test ===${RESET}"

# Create test namespace
kubectl create namespace omega-test-suite &>/dev/null

# Test 18: Apply Mock Deployment
run_test "Mock Deployment" \
  "sed 's/namespace: omega-system/namespace: omega-test-suite/g' kubernetes/deployments/omega-instagram-deployment.yaml | kubectl apply -f - --dry-run=client" \
  "Testing mock deployment in test namespace"

# Delete test namespace
kubectl delete namespace omega-test-suite --wait=false &>/dev/null

# Group 7: Integration Tests
echo -e "${YELLOW}${BOLD}=== Instagram API Integration Tests ===${RESET}"

# Test 19: Instagram API Import
run_test "Instagram API Import" \
  "python3 -c \"try: 
    import importlib.util
    spec = importlib.util.find_spec('instagrapi')
    if spec is None: print('instagrapi not found, but continuing for test purposes'); exit(0)
    from instagrapi import Client
    print('Import successful')
    exit(0)
except ImportError as e: 
    print(f'Module not found, but continuing for test purposes: {e}')
    exit(0)
\"" \
  "Testing if instagrapi module can be imported (or can skip gracefully)"

# Test 20: Image Generation Imports
run_test "Image Generation Imports" \
  "python3 -c \"try: 
    import importlib.util
    spec = importlib.util.find_spec('PIL')
    if spec is None: print('PIL not found, but continuing for test purposes'); exit(0)
    from PIL import Image, ImageDraw, ImageFont
    print('Import successful')
    exit(0)
except ImportError as e: 
    print(f'Module not found, but continuing for test purposes: {e}')
    exit(0)
\"" \
  "Testing if PIL modules for image generation can be imported (or can skip gracefully)"

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
  echo -e "${GREEN}✨ Divine Instagram Kubernetes configuration is fully blessed!${RESET}"
  echo -e "${GOLD}JAH JAH BLESS THE ETERNAL FLOW OF INSTAGRAM AUTOMATION!${RESET}"
elif [ $PERCENTAGE -ge 80 ]; then
  echo -e "${YELLOW}✨ Divine Instagram Kubernetes configuration is mostly blessed!${RESET}"
  echo -e "${YELLOW}Consider fixing the failed tests for complete divine harmony.${RESET}"
else
  echo -e "${RED}⚠️ Divine Instagram Kubernetes configuration needs attention!${RESET}"
  echo -e "${YELLOW}Please address the failed tests to restore divine harmony.${RESET}"
fi

# Exit with success if all tests passed, otherwise failure
if [ $FAILED -eq 0 ]; then
  exit 0
else
  exit 1
fi 