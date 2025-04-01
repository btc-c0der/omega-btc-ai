#!/bin/bash

# 🔱 OMEGA BTC AI - Divine Kubernetes Restart 🔱
# This script restarts Docker Desktop and Kubernetes properly

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
echo " 𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝖀𝕭𝕰𝕽𝕹𝕰𝕿𝕰𝕾 𝕽𝕰𝕭𝕺𝕽𝕹 "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Stop Docker Desktop
echo -e "${CYAN}${BOLD}=== Step 1: Stopping Docker Desktop ===${RESET}"
echo -e "${CYAN}📌 Checking for running Docker processes...${RESET}"

# Check if Docker is running
if pgrep -x "Docker" > /dev/null || pgrep -x "com.docker.backend" > /dev/null; then
    echo -e "${YELLOW}⚠️ Docker Desktop is running. Stopping it now...${RESET}"
    
    # Gracefully quit Docker Desktop
    if [ -d "/Applications/Docker.app" ]; then
        echo -e "${CYAN}📌 Closing Docker Desktop application...${RESET}"
        osascript -e 'quit app "Docker"'
        sleep 5
    fi
    
    # Check for and stop any remaining Docker processes
    if pgrep -x "com.docker.backend" > /dev/null; then
        echo -e "${YELLOW}⚠️ Stopping Docker background processes...${RESET}"
        killall com.docker.backend 2>/dev/null
        sleep 2
    fi
else
    echo -e "${GREEN}✅ Docker Desktop is not running${RESET}"
fi

# Clean up Docker Kubernetes caches on macOS
echo -e "\n${CYAN}${BOLD}=== Step 2: Cleaning Docker Kubernetes Cache ===${RESET}"

# Check for and remove Kubernetes configs that might be causing issues
if [ -d "$HOME/.kube" ]; then
    echo -e "${CYAN}📌 Backing up existing .kube directory...${RESET}"
    timestamp=$(date +%Y%m%d%H%M%S)
    cp -r "$HOME/.kube" "$HOME/.kube.backup.$timestamp"
    echo -e "${GREEN}✅ Backup created at $HOME/.kube.backup.$timestamp${RESET}"
fi

# Clean docker state directory
echo -e "${CYAN}📌 Checking Docker state directory...${RESET}"
DOCKER_STATE_DIR="$HOME/Library/Containers/com.docker.docker/Data/vm"
if [ -d "$DOCKER_STATE_DIR" ]; then
    echo -e "${YELLOW}⚠️ Consider resetting Kubernetes from Docker Desktop preferences${RESET}"
else
    echo -e "${GREEN}✅ Docker state directory not found or already clean${RESET}"
fi

# Start Docker Desktop with Kubernetes
echo -e "\n${CYAN}${BOLD}=== Step 3: Starting Docker Desktop ===${RESET}"
echo -e "${CYAN}📌 Opening Docker Desktop application...${RESET}"
open -a Docker

# Wait for Docker to start
echo -e "${CYAN}📌 Waiting for Docker to start (this may take a minute)...${RESET}"
attempt=0
max_attempts=30
while [ $attempt -lt $max_attempts ]; do
    if docker info &>/dev/null; then
        echo -e "${GREEN}✅ Docker has started successfully${RESET}"
        break
    fi
    echo -n "."
    sleep 2
    attempt=$((attempt+1))
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "\n${RED}❌ Docker did not start within the expected time${RESET}"
    echo -e "${YELLOW}📌 Please start Docker Desktop manually${RESET}"
    exit 1
fi

# Wait for Kubernetes to start
echo -e "\n${CYAN}${BOLD}=== Step 4: Waiting for Kubernetes to Initialize ===${RESET}"
echo -e "${CYAN}📌 This may take a few minutes...${RESET}"

# Check if Kubernetes is enabled in Docker Desktop
if ! docker info | grep -q "Kubernetes"; then
    echo -e "${RED}❌ Kubernetes not found in Docker Desktop${RESET}"
    echo -e "${YELLOW}📌 Please enable Kubernetes in Docker Desktop preferences:${RESET}"
    echo -e "${YELLOW}   1. Open Docker Desktop${RESET}"
    echo -e "${YELLOW}   2. Go to Preferences/Settings${RESET}"
    echo -e "${YELLOW}   3. Navigate to Kubernetes tab${RESET}"
    echo -e "${YELLOW}   4. Check 'Enable Kubernetes'${RESET}"
    echo -e "${YELLOW}   5. Click 'Apply & Restart'${RESET}"
    exit 1
fi

# Wait for Kubernetes to be ready
attempt=0
max_attempts=60
while [ $attempt -lt $max_attempts ]; do
    if kubectl get nodes &>/dev/null; then
        echo -e "${GREEN}✅ Kubernetes is now running${RESET}"
        kubectl get nodes
        break
    fi
    echo -n "."
    sleep 5
    attempt=$((attempt+1))
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "\n${RED}❌ Kubernetes did not start within the expected time${RESET}"
    echo -e "${YELLOW}📌 Try resetting Kubernetes from Docker Desktop preferences${RESET}"
    exit 1
fi

# Check if kubernetes-dashboard namespace exists
echo -e "\n${CYAN}${BOLD}=== Step 5: Setting Up Dashboard ===${RESET}"
if ! kubectl get namespace kubernetes-dashboard &>/dev/null; then
    echo -e "${YELLOW}⚠️ kubernetes-dashboard namespace not found. Creating it...${RESET}"
    kubectl create namespace kubernetes-dashboard
    
    echo -e "${CYAN}📌 Deploying Kubernetes dashboard...${RESET}"
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
    
    echo -e "${CYAN}📌 Creating admin user for dashboard access...${RESET}"
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
else
    echo -e "${GREEN}✅ kubernetes-dashboard namespace already exists${RESET}"
fi

# Wait for dashboard to be ready
echo -e "${CYAN}📌 Waiting for dashboard to be ready (this may take a minute)...${RESET}"
attempt=0
max_attempts=30
while [ $attempt -lt $max_attempts ]; do
    if kubectl get deployment kubernetes-dashboard -n kubernetes-dashboard &>/dev/null; then
        echo -e "${GREEN}✅ Kubernetes dashboard deployment found${RESET}"
        
        # Check if it's ready
        READY=$(kubectl get deployment kubernetes-dashboard -n kubernetes-dashboard -o jsonpath='{.status.readyReplicas}')
        if [ "$READY" == "1" ]; then
            echo -e "${GREEN}✅ Kubernetes dashboard is ready${RESET}"
            break
        fi
    fi
    echo -n "."
    sleep 2
    attempt=$((attempt+1))
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "\n${YELLOW}⚠️ Dashboard may not be fully ready yet, but we'll continue${RESET}"
fi

# Try to access dashboard
echo -e "\n${CYAN}${BOLD}=== Step 6: Testing Dashboard Access ===${RESET}"

# Find available port
PORT=8443
while netstat -tna | grep -q ":$PORT "; do
    PORT=$((PORT+1))
done

echo -e "${CYAN}📌 Starting port forwarding on port $PORT...${RESET}"
kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard $PORT:443 &
PF_PID=$!

# Wait a moment
sleep 3

# Check if port forwarding is running
if ps -p $PF_PID > /dev/null; then
    echo -e "${GREEN}✅ Port forwarding started successfully${RESET}"
    
    # Generate token
    echo -e "${CYAN}📌 Generating access token...${RESET}"
    TOKEN=$(kubectl -n kubernetes-dashboard create token admin-user)
    
    echo -e "${GREEN}✅ Divine Kubernetes Reborn is complete!${RESET}"
    echo -e "${CYAN}📌 Dashboard URL: https://localhost:$PORT${RESET}"
    echo -e "${CYAN}📌 Access Token: ${TOKEN}${RESET}"
    
    # Keep port forwarding running until user interrupts
    echo -e "\n${YELLOW}📌 Press Ctrl+C to stop port forwarding when done${RESET}"
    wait $PF_PID
else
    echo -e "${RED}❌ Port forwarding failed to start${RESET}"
fi

# Cleanup
kill $PF_PID 2>/dev/null

echo -e "\n${GOLD}JAH JAH BLESS THE REBORN KUBERNETES FLOW!${RESET}" 