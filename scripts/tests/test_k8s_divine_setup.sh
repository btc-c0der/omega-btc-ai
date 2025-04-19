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


# 🔱 OMEGA BTC AI - Divine Kubernetes Test Suite 🔱
# This script tests the Kubernetes setup and services

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
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝟴𝕾 𝕿𝕰𝕾𝕿 𝕾𝖀𝕴𝕿𝕰  "
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

# Test 4: Docker Desktop Kubernetes
run_test "Docker Desktop Kubernetes" \
  "kubectl get nodes | grep -q docker-desktop" \
  "Checking if Docker Desktop's Kubernetes is enabled"

# Group 2: Namespace Tests
echo -e "${YELLOW}${BOLD}=== Testing Kubernetes Namespaces ===${RESET}"

# Test 5: Dashboard Namespace
run_test "Dashboard Namespace" \
  "kubectl get namespace kubernetes-dashboard" \
  "Checking if kubernetes-dashboard namespace exists"

# Test 6: Omega System Namespace
run_test "Omega System Namespace" \
  "kubectl get namespace omega-system 2>/dev/null || (kubectl create namespace omega-system && kubectl get namespace omega-system)" \
  "Checking/creating omega-system namespace"

# Test 7: Omega Dev Namespace
run_test "Omega Dev Namespace" \
  "kubectl get namespace omega-dev 2>/dev/null || (kubectl create namespace omega-dev && kubectl get namespace omega-dev)" \
  "Checking/creating omega-dev namespace"

# Test 8: Omega Monitoring Namespace
run_test "Omega Monitoring Namespace" \
  "kubectl get namespace omega-monitoring 2>/dev/null || (kubectl create namespace omega-monitoring && kubectl get namespace omega-monitoring)" \
  "Checking/creating omega-monitoring namespace"

# Group 3: Dashboard Tests
echo -e "${YELLOW}${BOLD}=== Testing Kubernetes Dashboard ===${RESET}"

# Test 9: Dashboard Deployment
run_test "Dashboard Deployment" \
  "kubectl get deployment -n kubernetes-dashboard kubernetes-dashboard 2>/dev/null || (echo 'Dashboard not installed, installing now...' && kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml && sleep 5 && kubectl get deployment -n kubernetes-dashboard kubernetes-dashboard)" \
  "Checking/deploying kubernetes-dashboard"

# Test 10: Dashboard Service
run_test "Dashboard Service" \
  "kubectl get service -n kubernetes-dashboard kubernetes-dashboard" \
  "Checking if dashboard service exists"

# Test 11: Admin ServiceAccount
run_test "Admin ServiceAccount" \
  "kubectl get serviceaccount -n kubernetes-dashboard admin-user 2>/dev/null || (kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
EOF
kubectl get serviceaccount -n kubernetes-dashboard admin-user)" \
  "Checking/creating admin-user ServiceAccount"

# Test 12: Admin ClusterRoleBinding
run_test "Admin ClusterRoleBinding" \
  "kubectl get clusterrolebinding admin-user 2>/dev/null || (kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF
kubectl get clusterrolebinding admin-user)" \
  "Checking/creating admin-user ClusterRoleBinding"

# Group 4: Redis Tests
echo -e "${YELLOW}${BOLD}=== Testing Redis Services ===${RESET}"

# Test 13: Redis Deployment
run_test "Redis Deployment" \
  "kubectl get deployment -n omega-system redis 2>/dev/null || (kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: omega-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:6.2-alpine
        ports:
        - containerPort: 6379
EOF
sleep 5 && kubectl get deployment -n omega-system redis)" \
  "Checking/deploying Redis"

# Test 14: Redis Service
run_test "Redis Service" \
  "kubectl get service -n omega-system redis 2>/dev/null || (kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: omega-system
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
EOF
kubectl get service -n omega-system redis)" \
  "Checking/creating Redis service"

# Group 5: Monitoring Tests
echo -e "${YELLOW}${BOLD}=== Testing Monitoring Services ===${RESET}"

# Test 15: Prometheus Deployment
run_test "Prometheus Deployment" \
  "kubectl get deployment -n omega-monitoring prometheus 2>/dev/null || (echo 'Prometheus not installed, installing now...' && kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: omega-monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: omega-monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config-volume
          mountPath: /etc/prometheus
      volumes:
      - name: config-volume
        configMap:
          name: prometheus-config
EOF
sleep 5 && kubectl get deployment -n omega-monitoring prometheus)" \
  "Checking/deploying Prometheus"

# Test 16: Grafana Deployment
run_test "Grafana Deployment" \
  "kubectl get deployment -n omega-monitoring grafana 2>/dev/null || (echo 'Grafana not installed, installing now...' && kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: omega-monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana
        ports:
        - containerPort: 3000
EOF
sleep 5 && kubectl get deployment -n omega-monitoring grafana)" \
  "Checking/deploying Grafana"

# Test 17: Prometheus Service
run_test "Prometheus Service" \
  "kubectl get service -n omega-monitoring prometheus 2>/dev/null || (kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: omega-monitoring
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
EOF
kubectl get service -n omega-monitoring prometheus)" \
  "Checking/creating Prometheus service"

# Test 18: Grafana Service
run_test "Grafana Service" \
  "kubectl get service -n omega-monitoring grafana 2>/dev/null || (kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: omega-monitoring
spec:
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000
EOF
kubectl get service -n omega-monitoring grafana)" \
  "Checking/creating Grafana service"

# Group 6: Port Forwarding Test
echo -e "${YELLOW}${BOLD}=== Testing Port Forwarding ===${RESET}"

# Test 19: Port Forwarding Test Function
port_forwarding_test() {
  # Try to find an available port
  PORT=8443
  while netstat -tna | grep -q ":$PORT "; do
    PORT=$((PORT+1))
  done
  
  # Start port forwarding in background
  kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard $PORT:443 &
  PF_PID=$!
  
  # Wait a moment to ensure port-forwarding is established
  sleep 2
  
  # Check if port-forwarding started successfully
  if ps -p $PF_PID > /dev/null; then
    # Try to connect to the forwarded port
    curl -k https://localhost:$PORT > /dev/null 2>&1
    CURL_STATUS=$?
    
    # Kill the port-forwarding process
    kill $PF_PID 2>/dev/null
    wait $PF_PID 2>/dev/null
    
    # Return the result of the curl command
    return $CURL_STATUS
  else
    return 1
  fi
}

run_test "Dashboard Port Forwarding" \
  "port_forwarding_test" \
  "Testing port forwarding to kubernetes-dashboard"

# Group 7: Token Generation Test
echo -e "${YELLOW}${BOLD}=== Testing Token Generation ===${RESET}"

# Test 20: Token Generation
run_test "Dashboard Token Generation" \
  "kubectl -n kubernetes-dashboard create token admin-user" \
  "Testing token generation for dashboard access"

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
  echo -e "${GREEN}✨ Divine Kubernetes configuration is fully blessed!${RESET}"
  echo -e "${YELLOW}JAH JAH BLESS THE ETERNAL FLOW OF KUBERNETES!${RESET}"
elif [ $PERCENTAGE -ge 80 ]; then
  echo -e "${YELLOW}✨ Divine Kubernetes configuration is mostly blessed!${RESET}"
  echo -e "${YELLOW}Consider fixing the failed tests for complete divine harmony.${RESET}"
else
  echo -e "${RED}⚠️ Divine Kubernetes configuration needs attention!${RESET}"
  echo -e "${YELLOW}Please address the failed tests to restore divine harmony.${RESET}"
fi

# Exit with success if all tests passed, otherwise failure
if [ $FAILED -eq 0 ]; then
  exit 0
else
  exit 1
fi 