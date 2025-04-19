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


# 🔱 OMEGA BTC AI - Divine Dashboard Access Check 🔱
# This script tests access to the Kubernetes dashboard and fixes networking issues

# Divine Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
GOLD='\033[0;33m'
RESET='\033[0m'
BOLD='\033[1m'

# Divine Banner
echo -e "${GOLD}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                           "
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕯𝕬𝕾𝕳𝕭𝕺𝕬𝕽𝕯 𝕬𝕮𝕮𝕰𝕾𝕾  "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Check if kubectl is available
echo -e "${CYAN}${BOLD}=== Checking kubectl ===${RESET}"
if ! command -v kubectl &> /dev/null; then
  echo -e "${RED}❌ kubectl not found${RESET}"
  echo -e "${YELLOW}📌 Please install kubectl or ensure it's in your PATH${RESET}"
  exit 1
fi
echo -e "${GREEN}✅ kubectl found${RESET}"

# Check dashboard pod existence
echo -e "\n${CYAN}${BOLD}=== Checking Kubernetes Dashboard Pod ===${RESET}"
if kubectl get pod -n kubernetes-dashboard -l k8s-app=kubernetes-dashboard -o name &> /dev/null; then
  DASHBOARD_POD=$(kubectl get pod -n kubernetes-dashboard -l k8s-app=kubernetes-dashboard -o name | head -1)
  echo -e "${GREEN}✅ Dashboard pod found: ${DASHBOARD_POD}${RESET}"
  
  # Check dashboard pod status
  DASHBOARD_STATUS=$(kubectl get $DASHBOARD_POD -n kubernetes-dashboard -o jsonpath='{.status.phase}' 2>/dev/null)
  if [ "$DASHBOARD_STATUS" == "Running" ]; then
    echo -e "${GREEN}✅ Dashboard pod status: Running${RESET}"
  else
    echo -e "${RED}❌ Dashboard pod status: $DASHBOARD_STATUS${RESET}"
    echo -e "${YELLOW}📌 Pod not running properly. Let's check pod details:${RESET}"
    kubectl describe $DASHBOARD_POD -n kubernetes-dashboard | grep -E "State:|Reason:|Message:" | head -5
  fi
else
  echo -e "${RED}❌ Dashboard pod not found${RESET}"
  echo -e "${YELLOW}📌 Let's see what pods are in the kubernetes-dashboard namespace:${RESET}"
  kubectl get pods -n kubernetes-dashboard
fi

# Check dashboard service
echo -e "\n${CYAN}${BOLD}=== Checking Kubernetes Dashboard Service ===${RESET}"
if kubectl get service kubernetes-dashboard -n kubernetes-dashboard &> /dev/null; then
  echo -e "${GREEN}✅ Dashboard service found${RESET}"
  
  # Get service details
  DASHBOARD_PORT=$(kubectl get service kubernetes-dashboard -n kubernetes-dashboard -o jsonpath='{.spec.ports[0].port}')
  DASHBOARD_TARGET_PORT=$(kubectl get service kubernetes-dashboard -n kubernetes-dashboard -o jsonpath='{.spec.ports[0].targetPort}')
  DASHBOARD_TYPE=$(kubectl get service kubernetes-dashboard -n kubernetes-dashboard -o jsonpath='{.spec.type}')
  
  echo -e "${CYAN}📌 Dashboard service details:${RESET}"
  echo -e "${CYAN}   - Port: ${DASHBOARD_PORT}${RESET}"
  echo -e "${CYAN}   - Target Port: ${DASHBOARD_TARGET_PORT}${RESET}"
  echo -e "${CYAN}   - Type: ${DASHBOARD_TYPE}${RESET}"
else
  echo -e "${RED}❌ Dashboard service not found${RESET}"
  echo -e "${YELLOW}📌 Let's create the service:${RESET}"
  echo -e "${YELLOW}📌 Run: kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml${RESET}"
fi

# Check /etc/hosts
echo -e "\n${CYAN}${BOLD}=== Checking /etc/hosts ===${RESET}"
if grep -q "dashboard.omega-grid.local" /etc/hosts; then
  echo -e "${GREEN}✅ dashboard.omega-grid.local found in /etc/hosts${RESET}"
  # Display entry
  HOSTS_ENTRY=$(grep "dashboard.omega-grid.local" /etc/hosts)
  echo -e "${CYAN}📌 Entry: ${HOSTS_ENTRY}${RESET}"
else
  echo -e "${YELLOW}⚠️ dashboard.omega-grid.local not found in /etc/hosts${RESET}"
  echo -e "${YELLOW}📌 Consider adding this entry to /etc/hosts:${RESET}"
  echo -e "${YELLOW}📌 127.0.0.1 dashboard.omega-grid.local${RESET}"
  
  # Suggest command to add it
  echo -e "${YELLOW}📌 Run: sudo sh -c 'echo \"127.0.0.1 dashboard.omega-grid.local\" >> /etc/hosts'${RESET}"
fi

# Test port forwarding
echo -e "\n${CYAN}${BOLD}=== Testing Port Forwarding ===${RESET}"
echo -e "${CYAN}📌 Attempting to forward port...${RESET}"

# Find an available port
PORT=8443
while netstat -tna | grep -q ":$PORT "; do
  PORT=$((PORT+1))
done

# Start port forwarding in background
kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard $PORT:443 &
PF_PID=$!

# Wait a moment
echo -e "${CYAN}📌 Waiting for port forwarding to establish...${RESET}"
sleep 3

# Check if port forwarding is running
if ps -p $PF_PID > /dev/null; then
  echo -e "${GREEN}✅ Port forwarding started successfully on port $PORT${RESET}"
  
  # Test connection
  echo -e "${CYAN}📌 Testing connection to https://localhost:$PORT...${RESET}"
  if curl -k -s -o /dev/null -w "%{http_code}" https://localhost:$PORT > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Connection successful${RESET}"
  else
    echo -e "${YELLOW}⚠️ Connection issues. This could be due to:${RESET}"
    echo -e "${YELLOW}   - Firewall blocking localhost connections${RESET}"
    echo -e "${YELLOW}   - Dashboard service not fully ready${RESET}"
    echo -e "${YELLOW}   - TLS certificate issues (expected with self-signed certs)${RESET}"
  fi
  
  # Create access token
  echo -e "\n${CYAN}${BOLD}=== Creating Access Token ===${RESET}"
  echo -e "${CYAN}📌 Generating dashboard access token...${RESET}"
  
  # Check if admin-user exists
  if kubectl get serviceaccount admin-user -n kubernetes-dashboard &> /dev/null; then
    echo -e "${GREEN}✅ admin-user service account exists${RESET}"
  else
    echo -e "${YELLOW}⚠️ admin-user service account not found. Creating...${RESET}"
    kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
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
    echo -e "${GREEN}✅ admin-user service account created${RESET}"
  fi
  
  # Generate token
  TOKEN=$(kubectl -n kubernetes-dashboard create token admin-user)
  echo -e "${GREEN}✅ Access token generated${RESET}"
  echo -e "${CYAN}📌 Token: ${TOKEN}${RESET}"
  
  # Display access URLs
  echo -e "\n${CYAN}${BOLD}=== Dashboard Access ===${RESET}"
  echo -e "${CYAN}📌 Dashboard is now accessible at:${RESET}"
  echo -e "${CYAN}   - https://localhost:$PORT${RESET}"
  echo -e "${CYAN}   - https://dashboard.omega-grid.local:$PORT${RESET}"
  echo -e "${CYAN}📌 Use the token above to sign in${RESET}"
  
  # Keep port forwarding running
  echo -e "\n${CYAN}📌 Press Ctrl+C to stop port forwarding when done${RESET}"
  wait $PF_PID
else
  echo -e "${RED}❌ Port forwarding failed to start${RESET}"
  echo -e "${YELLOW}📌 Possible reasons:${RESET}"
  echo -e "${YELLOW}   - Port $PORT might be in use${RESET}"
  echo -e "${YELLOW}   - Insufficient permissions${RESET}"
  echo -e "${YELLOW}   - Kubernetes service might not be fully ready${RESET}"
fi

# Cleanup
kill $PF_PID 2>/dev/null

echo -e "\n${CYAN}${BOLD}=== Divine Blessing ===${RESET}"
echo -e "${GOLD}JAH JAH BLESS THE KUBERNETES DASHBOARD FLOW!${RESET}" 