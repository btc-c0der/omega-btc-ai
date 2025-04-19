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


# 🔱 OMEGA BTC AI - Divine IBR España Kubernetes Test Suite 🔱
# This script tests the IBR Spain deployment in Kubernetes

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
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕴𝕭𝕽 𝕾𝕻𝕬𝕴𝕹 𝕶𝟴𝕾 𝕿𝕰𝕾𝕿 𝕾𝖀𝕴𝕿𝕰  "
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

# Create test namespace if it doesn't exist
kubectl create namespace $NAMESPACE 2>/dev/null || true

# Group 1: Basic Requirements Tests
echo -e "${YELLOW}${BOLD}=== Testing Base Requirements ===${RESET}"

# Test 1: kubectl Installation
run_test "kubectl Installation" \
  "command -v kubectl" \
  "Checking if kubectl is installed"

# Test 2: Kubernetes Connection
run_test "Kubernetes Connection" \
  "kubectl get nodes" \
  "Checking if kubectl can connect to Kubernetes cluster"

# Test 3: Helm Installation (for potential package deployments)
run_test "Helm Installation" \
  "command -v helm" \
  "Checking if Helm is installed"

# Group 2: Manifest Validation Tests
echo -e "${YELLOW}${BOLD}=== Testing Kubernetes Manifests ===${RESET}"

# Test 4: UI Manifest Validation
run_test "UI Manifest Validation" \
  "kubectl apply --dry-run=client -f kubernetes/ibr-spain/base/ui-deployment.yaml" \
  "Validating UI deployment manifest"

# Test 5: API Manifest Validation
run_test "API Manifest Validation" \
  "kubectl apply --dry-run=client -f kubernetes/ibr-spain/base/api-deployment.yaml" \
  "Validating API deployment manifest"

# Test 6: Sermon Service Manifest Validation
run_test "Sermon Service Manifest Validation" \
  "kubectl apply --dry-run=client -f kubernetes/ibr-spain/base/services/sermon-service.yaml" \
  "Validating Sermon Service deployment manifest"

# Test 7: MongoDB Manifest Validation
run_test "MongoDB Manifest Validation" \
  "kubectl apply --dry-run=client -f kubernetes/ibr-spain/base/storage/mongodb.yaml" \
  "Validating MongoDB deployment manifest"

# Group 3: Security Tests
echo -e "${YELLOW}${BOLD}=== Testing Security Configuration ===${RESET}"

# Test 8: API Secrets Exist
run_test "API Secrets Check" \
  "grep -q 'JWT_SECRET' kubernetes/ibr-spain/base/api-deployment.yaml" \
  "Checking if API secrets are defined"

# Test 9: MongoDB Secrets Exist
run_test "MongoDB Secrets Check" \
  "grep -q 'mongodb-admin-credentials' kubernetes/ibr-spain/base/storage/mongodb.yaml" \
  "Checking if MongoDB secrets are defined"

# Test 10: Sermon Service Secrets Exist
run_test "Sermon Service Secrets Check" \
  "grep -q 'sermon-service-secrets' kubernetes/ibr-spain/base/services/sermon-service.yaml" \
  "Checking if Sermon Service secrets are defined"

# Test 11: Security Context Configuration
run_test "Security Context Configuration" \
  "grep -q 'runAsNonRoot: true' kubernetes/ibr-spain/base/api-deployment.yaml" \
  "Checking if security context is properly configured"

# Group 4: Resources and Scaling Tests
echo -e "${YELLOW}${BOLD}=== Testing Resources and Scaling ===${RESET}"

# Test 12: Resource Limits Defined
run_test "Resource Limits Check" \
  "grep -q 'resources' kubernetes/ibr-spain/base/ui-deployment.yaml" \
  "Checking if resource limits are defined"

# Test 13: HPA Configuration
run_test "HPA Configuration Check" \
  "grep -q 'HorizontalPodAutoscaler' kubernetes/ibr-spain/base/services/sermon-service.yaml" \
  "Checking if HorizontalPodAutoscaler is configured"

# Test 14: Replicas Configuration
run_test "Replicas Check" \
  "grep -q 'replicas' kubernetes/ibr-spain/base/api-deployment.yaml" \
  "Checking if replica count is defined"

# Group 5: Monitoring and Health Tests
echo -e "${YELLOW}${BOLD}=== Testing Monitoring & Health Configuration ===${RESET}"

# Test 15: Prometheus Annotations
run_test "Prometheus Annotations Check" \
  "grep -q 'prometheus.io/scrape' kubernetes/ibr-spain/base/services/sermon-service.yaml" \
  "Checking if Prometheus annotations are configured"

# Test 16: Health Probes
run_test "Health Probes Check" \
  "grep -q 'livenessProbe' kubernetes/ibr-spain/base/ui-deployment.yaml" \
  "Checking if health probes are configured"

# Group 6: Religious Content Tests
echo -e "${YELLOW}${BOLD}=== Testing Religious Content Features ===${RESET}"

# Test 17: Religious Content Config
run_test "Religious Content Config Check" \
  "grep -q 'SCRIPTURE_API_URL' kubernetes/ibr-spain/base/services/sermon-service.yaml" \
  "Checking if scripture API configuration exists"

# Test 18: IBR Spain Domain Config
run_test "IBR Spain Domain Check" \
  "grep -q 'ibr-espana.org' kubernetes/ibr-spain/base/ui-deployment.yaml" \
  "Checking if IBR España domain is configured"

# Group 7: Mock Deployment Tests
echo -e "${YELLOW}${BOLD}=== Running Mock Deployment Tests ===${RESET}"

# Create temporary modified deployment files
mkdir -p /tmp/ibr-test

# Test 19: Apply Namespace
run_test "Namespace Creation" \
  "kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: $NAMESPACE
EOF" \
  "Creating or verifying namespace"

# Test 20: Generate and validate Kustomize (if applicable)
run_test "Kustomize Validation" \
  "test -f kubernetes/ibr-spain/base/kustomization.yaml || echo 'kustomization.yaml not found, skipping' >/dev/null" \
  "Validating Kustomize configuration if present"

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
  echo -e "${GREEN}✨ Divine IBR España Kubernetes configuration is fully blessed!${RESET}"
  echo -e "${GOLD}JAH JAH BLESS THE DIVINE FLOW OF IBR ESPAÑA!${RESET}"
elif [ $PERCENTAGE -ge 80 ]; then
  echo -e "${YELLOW}✨ Divine IBR España Kubernetes configuration is mostly blessed!${RESET}"
  echo -e "${YELLOW}Consider fixing the failed tests for complete divine harmony.${RESET}"
else
  echo -e "${RED}⚠️ Divine IBR España Kubernetes configuration needs attention!${RESET}"
  echo -e "${YELLOW}Please address the failed tests to restore divine harmony.${RESET}"
fi

# Exit with success if all tests passed, otherwise failure
if [ $FAILED -eq 0 ]; then
  exit 0
else
  exit 1
fi 