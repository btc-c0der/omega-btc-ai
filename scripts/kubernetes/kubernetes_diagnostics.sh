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


# 🔱 OMEGA BTC AI - Divine Kubernetes Diagnostics 🔱
# This script diagnoses common Kubernetes issues and provides remediation

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
echo "  𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝟴𝕾 𝕯𝕴𝕬𝕲𝕹𝕺𝕾𝕿𝕴𝕮𝕾  "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Check Docker Status
echo -e "${CYAN}${BOLD}=== Docker Status ===${RESET}"
if command -v docker &> /dev/null; then
  echo -e "${GREEN}✅ Docker CLI installed${RESET}"
else
  echo -e "${RED}❌ Docker CLI not found${RESET}"
  echo -e "${YELLOW}📌 Please install Docker Desktop from https://www.docker.com/products/docker-desktop${RESET}"
  exit 1
fi

# Check Docker is running
if docker info &> /dev/null; then
  echo -e "${GREEN}✅ Docker is running${RESET}"
  
  # Get Docker version
  DOCKER_VERSION=$(docker version --format '{{.Server.Version}}')
  echo -e "${CYAN}📌 Docker version: ${DOCKER_VERSION}${RESET}"
else
  echo -e "${RED}❌ Docker is not running${RESET}"
  echo -e "${YELLOW}📌 Please start Docker Desktop and try again${RESET}"
  exit 1
fi

# Check Kubernetes in Docker Desktop
echo -e "\n${CYAN}${BOLD}=== Kubernetes Status ===${RESET}"

# Check Kubernetes configuration
if docker info | grep -q "Kubernetes"; then
  if docker info | grep -q "Kubernetes: enabled"; then
    echo -e "${GREEN}✅ Kubernetes is enabled in Docker Desktop${RESET}"
  else
    echo -e "${RED}❌ Kubernetes is installed but not enabled in Docker Desktop${RESET}"
    echo -e "${YELLOW}📌 Please enable Kubernetes in Docker Desktop settings and try again${RESET}"
  fi
else
  echo -e "${RED}❌ Kubernetes integration not found in Docker Desktop${RESET}"
  echo -e "${YELLOW}📌 Please check Docker Desktop settings to enable Kubernetes${RESET}"
fi

# Check kubectl installation
if command -v kubectl &> /dev/null; then
  echo -e "${GREEN}✅ kubectl installed${RESET}"
  
  # Get kubectl version
  KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null | awk '{print $3}')
  echo -e "${CYAN}📌 kubectl version: ${KUBECTL_VERSION}${RESET}"
else
  echo -e "${RED}❌ kubectl not found${RESET}"
  echo -e "${YELLOW}📌 kubectl should be installed with Docker Desktop Kubernetes${RESET}"
  echo -e "${YELLOW}📌 If not, install it with: brew install kubectl${RESET}"
  exit 1
fi

# Check kubectl connectivity
echo -e "\n${CYAN}${BOLD}=== Kubernetes Connection Test ===${RESET}"
if kubectl get nodes &> /dev/null; then
  echo -e "${GREEN}✅ Connected to Kubernetes successfully${RESET}"
  
  # Show nodes
  echo -e "${CYAN}📌 Kubernetes nodes:${RESET}"
  kubectl get nodes
else
  echo -e "${RED}❌ Cannot connect to Kubernetes${RESET}"
  
  # Display more detailed error
  ERROR=$(kubectl get nodes 2>&1 | head -3)
  echo -e "${YELLOW}📌 Error: ${ERROR}${RESET}"
  
  # Check config
  echo -e "\n${CYAN}${BOLD}=== Kubernetes Config Check ===${RESET}"
  echo -e "${CYAN}📌 Current Kubernetes context:${RESET}"
  kubectl config current-context 2>/dev/null || echo -e "${RED}No current context${RESET}"
  
  echo -e "${CYAN}📌 Available contexts:${RESET}"
  kubectl config get-contexts 2>/dev/null || echo -e "${RED}No contexts found${RESET}"
fi

# Check Docker Desktop Kubernetes status in more detail
echo -e "\n${CYAN}${BOLD}=== Docker Desktop Kubernetes Detailed Check ===${RESET}"
if [ -f ~/Library/Group\ Containers/group.com.docker/settings.json ]; then
  echo -e "${CYAN}📌 Docker Desktop settings.json exists${RESET}"
  
  # Check if Kubernetes is enabled in settings
  if grep -q "\"kubernetes\":" ~/Library/Group\ Containers/group.com.docker/settings.json; then
    echo -e "${CYAN}📌 Kubernetes configuration found in settings${RESET}"
    
    # Extracting and display kubernetes settings
    KUBERNETES_SETTINGS=$(grep -A 10 "\"kubernetes\":" ~/Library/Group\ Containers/group.com.docker/settings.json | grep -v "kubernetes")
    echo -e "${CYAN}Kubernetes settings: ${KUBERNETES_SETTINGS}${RESET}"
  else
    echo -e "${YELLOW}⚠️ Kubernetes configuration not found in settings${RESET}"
  fi
else
  echo -e "${YELLOW}⚠️ Docker Desktop settings.json not found${RESET}"
fi

# Common remediation steps
echo -e "\n${CYAN}${BOLD}=== Divine Remediation Steps ===${RESET}"
echo -e "${YELLOW}If Kubernetes is not working properly, try these divine remediation steps:${RESET}"
echo -e "${CYAN}1. Reset Kubernetes in Docker Desktop:${RESET}"
echo -e "   - Open Docker Desktop preferences"
echo -e "   - Navigate to Kubernetes"
echo -e "   - Click 'Reset Kubernetes Cluster'"
echo -e "   - Wait for Kubernetes to restart"

echo -e "${CYAN}2. Check for proper network connectivity:${RESET}"
echo -e "   - Ensure localhost connections are allowed in your firewall"
echo -e "   - Check if port 6443 is accessible: nc -vz 127.0.0.1 6443"

echo -e "${CYAN}3. Try restarting Docker Desktop:${RESET}"
echo -e "   - Completely quit Docker Desktop"
echo -e "   - Start Docker Desktop again"
echo -e "   - Wait for the green 'Running' status"

echo -e "${CYAN}4. Reinstall Docker Desktop:${RESET}"
echo -e "   - If all else fails, consider reinstalling Docker Desktop"
echo -e "   - Make sure to select 'Enable Kubernetes' during installation"

echo -e "\n${CYAN}${BOLD}=== Divine Blessing ===${RESET}"
echo -e "${GOLD}JAH JAH BLESS THE KUBERNETES CONNECTION FLOW!${RESET}" 