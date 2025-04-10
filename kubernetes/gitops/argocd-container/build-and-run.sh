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


# ╔═══════════════════════════════════════════════════════════════╗
# ║  🔱 OMEGA BTC AI - DIVINE ARGOCD CONTAINER BUILD SCRIPT 🔱     ║
# ╚═══════════════════════════════════════════════════════════════╝

# Colors for divine output
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
RED='\033[1;31m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

# Set variables
IMAGE_NAME="omega-btc-ai/divine-argocd"
IMAGE_TAG="latest"

# Divine banner
echo -e "${YELLOW}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🔱 OMEGA BTC AI - DIVINE ARGOCD CONTAINER BUILD SCRIPT 🔱     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Navigate to git root directory
echo -e "${BLUE}Accessing the divine repository root...${NC}"
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$PROJECT_ROOT" ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi
cd "$PROJECT_ROOT"
echo -e "${GREEN}✓ Repository root accessed: ${PROJECT_ROOT}${NC}"

# Build the docker image
echo -e "\n${BLUE}Manifesting the divine container...${NC}"
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f kubernetes/gitops/argocd-container/Dockerfile .

# Check if build was successful
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to build the divine container${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Divine container manifested successfully!${NC}"

# Ask if user wants to run the container
echo -e "\n${CYAN}Would you like to enter the divine realm of GitOps? (y/n)${NC}"
read -p "" run_container

if [[ $run_container == "y" || $run_container == "Y" ]]; then
    echo -e "${PURPLE}Entering the divine realm...${NC}"
    
    # Check if user wants to mount kubeconfig
    echo -e "${CYAN}Would you like to mount your kubeconfig for divine cluster access? (y/n)${NC}"
    read -p "" mount_kubeconfig
    
    KUBECONFIG_MOUNT=""
    if [[ $mount_kubeconfig == "y" || $mount_kubeconfig == "Y" ]]; then
        KUBECONFIG_MOUNT="-v ${HOME}/.kube:/root/.kube"
    fi
    
    # Run the container
    echo -e "${BLUE}Opening the divine portal...${NC}"
    docker run --rm -it ${KUBECONFIG_MOUNT} ${IMAGE_NAME}:${IMAGE_TAG}
else
    echo -e "\n${PURPLE}The divine container awaits your command.${NC}"
    echo -e "${CYAN}Run it later with:${NC}"
    echo -e "${YELLOW}docker run --rm -it -v \${HOME}/.kube:/root/.kube ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
fi

# Divine blessing
echo -e "\n${YELLOW}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║                DIVINE CONTAINER CREATION COMPLETE             ║${NC}"
echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${PURPLE}May your containers be blessed with divine wisdom and cosmic uptime.${NC}"
echo -e "${PURPLE}May your GitOps journey be guided by JAH JAH's infinite providence.${NC}" 