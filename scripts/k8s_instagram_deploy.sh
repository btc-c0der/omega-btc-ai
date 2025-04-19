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


# 🔱 OMEGA BTC AI - Divine Instagram Kubernetes Deployment 🔱
# This script builds and deploys the Instagram automation to Kubernetes

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
echo " 𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕴𝕹𝕾𝕿𝕬𝕲𝕽𝕬𝕸 𝕶𝟴𝕾 𝕯𝕰𝕻𝕷𝕺𝖄𝕸𝕰𝕹𝕿 "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Navigate to the project root directory
cd "$(dirname "$0")/.." || { echo -e "${RED}❌ Could not navigate to project root${RESET}"; exit 1; }

# Set variables
DOCKER_REGISTRY=${DOCKER_REGISTRY:-"localhost"}
IMAGE_NAME="omega-instagram"
IMAGE_TAG=${IMAGE_TAG:-"latest"}
FULL_IMAGE_NAME="${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
DOCKERFILE="Dockerfile.instagram"
K8S_MANIFEST="kubernetes/deployments/omega-instagram-deployment.yaml"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${RESET}"
    exit 1
fi

# Check for kubectl
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl first.${RESET}"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${RESET}"
    exit 1
fi

# Build the Docker image
echo -e "${CYAN}📌 Building Docker image ${BOLD}${FULL_IMAGE_NAME}${RESET}..."
if docker build -t "${FULL_IMAGE_NAME}" -f "${DOCKERFILE}" .; then
    echo -e "${GREEN}✅ Docker image built successfully${RESET}"
else
    echo -e "${RED}❌ Failed to build Docker image${RESET}"
    exit 1
fi

# Check if the omega-system namespace exists, create if not
if ! kubectl get namespace omega-system &> /dev/null; then
    echo -e "${CYAN}📌 Creating namespace omega-system...${RESET}"
    kubectl create namespace omega-system
    echo -e "${GREEN}✅ Namespace created${RESET}"
fi

# Apply the Kubernetes manifest
echo -e "${CYAN}📌 Applying Kubernetes manifests...${RESET}"
# Replace the Docker registry placeholder in the manifest
sed "s|\${DOCKER_REGISTRY:-localhost}|${DOCKER_REGISTRY}|g" "${K8S_MANIFEST}" | kubectl apply -f -

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Kubernetes manifests applied successfully${RESET}"
else
    echo -e "${RED}❌ Failed to apply Kubernetes manifests${RESET}"
    exit 1
fi

# Wait for deployment to be ready
echo -e "${CYAN}📌 Waiting for deployment to be ready...${RESET}"
kubectl rollout status deployment/omega-instagram -n omega-system --timeout=120s

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment is ready${RESET}"
    
    # Show Instagram automation pod
    echo -e "${CYAN}📌 Instagram automation pods:${RESET}"
    kubectl get pods -n omega-system -l app=omega-instagram -o wide
    
    # Show how to check logs
    echo -e "\n${CYAN}📌 To check logs, run:${RESET}"
    echo -e "${YELLOW}kubectl logs -f -n omega-system -l app=omega-instagram${RESET}"
    
    # Show how to update Instagram credentials
    echo -e "\n${CYAN}📌 To update Instagram credentials, run:${RESET}"
    echo -e "${YELLOW}kubectl edit secret instagram-credentials -n omega-system${RESET}"
    echo -e "${YELLOW}# You'll need to base64 encode your credentials${RESET}"
    
    echo -e "\n${GOLD}JAH JAH BLESS THE DIVINE KUBERNETES INSTAGRAM FLOW!${RESET}"
else
    echo -e "${RED}❌ Deployment failed to become ready within the timeout period${RESET}"
    echo -e "${YELLOW}📌 Check the pod status with:${RESET}"
    echo -e "${YELLOW}kubectl get pods -n omega-system -l app=omega-instagram${RESET}"
    echo -e "${YELLOW}kubectl describe pod -n omega-system -l app=omega-instagram${RESET}"
    exit 1
fi 