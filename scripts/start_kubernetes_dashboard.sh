#!/bin/bash

# 🔱 OMEGA BTC AI - Divine Kubernetes Dashboard Access 🔱
# This script provides access to the Kubernetes dashboard with automatic port detection

# Divine Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
GOLD='\033[0;33m'
RESET='\033[0m'

# Divine Banner
echo -e "${GOLD}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                           "
echo "       𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝖀𝕭𝕰𝕽𝕹𝕰𝕿𝕰𝕾 𝕯𝕬𝕾𝕳𝕭𝕺𝕬𝕽𝕯       "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
  echo -e "${RED}❌ Error: kubectl not found${RESET}"
  echo -e "${YELLOW}ℹ️  Please install kubectl first${RESET}"
  exit 1
fi

# Check if the namespace exists
if ! kubectl get namespace kubernetes-dashboard &> /dev/null; then
  echo -e "${RED}❌ Error: kubernetes-dashboard namespace not found${RESET}"
  echo -e "${YELLOW}ℹ️  Please run the setup script first: ./scripts/omega_kubernetes_setup.sh${RESET}"
  exit 1
fi

# Check if the service exists
if ! kubectl get service -n kubernetes-dashboard omega-kubernetes-dashboard &> /dev/null; then
  # Try the standard Kubernetes dashboard service as a fallback
  if kubectl get service -n kubernetes-dashboard kubernetes-dashboard &> /dev/null; then
    echo -e "${YELLOW}⚠️  omega-kubernetes-dashboard service not found, but kubernetes-dashboard service exists.${RESET}"
    echo -e "${YELLOW}⚠️  Using the standard Kubernetes dashboard instead.${RESET}"
    SERVICE_NAME="kubernetes-dashboard"
  else
    echo -e "${RED}❌ Error: No dashboard service found in kubernetes-dashboard namespace${RESET}"
    echo -e "${YELLOW}ℹ️  Please run the setup script first: ./scripts/omega_kubernetes_setup.sh${RESET}"
    exit 1
  fi
else
  SERVICE_NAME="omega-kubernetes-dashboard"
fi

# Find an available port using Python
find_port_with_python() {
  local start_port=$1
  if [ -z "$start_port" ]; then
    start_port=8000
  fi
  
  echo -e "${CYAN}🔍 Finding available port using Python...${RESET}"
  if [ -f "./scripts/find_available_port.py" ]; then
    local found_port=$(./scripts/find_available_port.py -s $start_port -q)
    if [ $? -eq 0 ]; then
      echo -e "${GREEN}✅ Found available port: $found_port${RESET}"
      echo "$found_port"
      return 0
    else
      return 1
    fi
  else
    return 1
  fi
}

# Use a direct netcat check to find an available port
find_port_with_netcat() {
  local start_port=$1
  if [ -z "$start_port" ]; then
    start_port=8000
  fi
  local max_port=9000
  local port=$start_port
  
  echo -e "${CYAN}🔍 Finding available port using network check...${RESET}"
  
  while [ $port -le $max_port ]; do
    # Try to connect to the port - if it fails, the port is available
    if ! (echo > /dev/tcp/127.0.0.1/$port) 2>/dev/null; then
      echo -e "${GREEN}✅ Found available port: $port${RESET}"
      echo "$port"
      return 0
    fi
    ((port++))
  done
  
  return 1
}

# Try to find an available port
echo -e "${CYAN}🔍 Finding an available port...${RESET}"
PORT=$(find_port_with_python)
if [ -z "$PORT" ]; then
  # Fallback to direct network check
  PORT=$(find_port_with_netcat)
  if [ -z "$PORT" ]; then
    # If all else fails, just try port 9090
    PORT=9090
    echo -e "${YELLOW}⚠️  Could not find available port, defaulting to $PORT${RESET}"
  fi
fi

# Function to start dashboard with port-forwarding
start_dashboard() {
  local port=$1
  local service=$2
  
  echo -e "${CYAN}🧿 Starting OMEGA Kubernetes Dashboard Port Forwarding on port $port...${RESET}"
  
  # Start port forwarding for the dashboard in background
  kubectl port-forward -n kubernetes-dashboard svc/$service $port:80 &
  
  # Store the process ID
  local pid=$!
  
  # Check if port-forwarding was successful
  sleep 2
  if ! ps -p $pid > /dev/null; then
    return 1
  fi
  
  echo -e "${GREEN}✅ Dashboard is now accessible at: ${CYAN}http://localhost:$port${RESET}"
  echo -e "${YELLOW}🔔 Press Ctrl+C to stop the port forwarding${RESET}"
  
  # Handle script termination to clean up the port-forwarding process
  trap "kill $pid 2>/dev/null; echo -e '${RED}🛑 Dashboard port forwarding stopped${RESET}'; exit" SIGINT SIGTERM
  
  # Wait for the port forwarding to finish (or be interrupted)
  wait $pid
  return 0
}

# Try to start the dashboard, if it fails, try another port
if ! start_dashboard "$PORT" "$SERVICE_NAME"; then
  echo -e "${YELLOW}⚠️  Failed to start dashboard on port $PORT. Trying another port...${RESET}"
  
  # Try a different port range
  NEW_PORT=$((PORT + 1000))
  PORT=$(find_port_with_python "$NEW_PORT")
  if [ -z "$PORT" ]; then
    PORT=10000
  fi
  
  if ! start_dashboard "$PORT" "$SERVICE_NAME"; then
    echo -e "${RED}❌ Failed to start dashboard after multiple attempts${RESET}"
    echo -e "${YELLOW}ℹ️  Try accessing the dashboard through Minikube directly:${RESET}"
    echo -e "${CYAN}   minikube dashboard${RESET}"
    exit 1
  fi
fi 