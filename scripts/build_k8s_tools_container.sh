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


# 🔱 OMEGA BTC AI - Divine Kubernetes Tools Container Builder 🔱
# This script builds the Docker container for Kubernetes management tools

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
echo " 𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝟴𝕾 𝕿𝕺𝕺𝕷𝕾 𝕮𝕺𝕹𝕿𝕬𝕴𝕹𝕰𝕽 "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Navigate to the project root directory
cd "$(dirname "$0")/.." || { echo -e "${RED}❌ Could not navigate to project root${RESET}"; exit 1; }

# Set variables
IMAGE_NAME="omega-k8s-tools"
IMAGE_TAG="latest"
DOCKERFILE="scripts/Dockerfile.k8s-tools"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop first.${RESET}"
    exit 1
fi

# Build the Docker image
echo -e "${CYAN}📌 Building ${BOLD}$IMAGE_NAME:$IMAGE_TAG${RESET}..."
if docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$DOCKERFILE" .; then
    echo -e "${GREEN}✅ Docker image ${BOLD}$IMAGE_NAME:$IMAGE_TAG${RESET}${GREEN} built successfully${RESET}"
else
    echo -e "${RED}❌ Failed to build Docker image${RESET}"
    exit 1
fi

# Display usage instructions
echo -e "\n${CYAN}${BOLD}=== Usage Instructions ===${RESET}"
echo -e "${CYAN}📌 To run the container with access to Docker socket:${RESET}"
echo -e "${YELLOW}docker run -it --rm \\"
echo "    -v /var/run/docker.sock:/var/run/docker.sock \\"
echo "    -v $HOME/.kube:/root/.kube \\"
echo "    $IMAGE_NAME:$IMAGE_TAG${RESET}"

echo -e "\n${CYAN}📌 To run specific commands:${RESET}"
echo -e "${YELLOW}docker run -it --rm \\"
echo "    -v /var/run/docker.sock:/var/run/docker.sock \\"
echo "    -v $HOME/.kube:/root/.kube \\"
echo "    $IMAGE_NAME:$IMAGE_TAG k8s-dashboard${RESET}"

echo -e "\n${CYAN}📌 Available commands:${RESET}"
echo -e "${CYAN}  - k8s-reborn         : Restart and reinitialize Kubernetes${RESET}"
echo -e "${CYAN}  - k8s-dashboard      : Start Kubernetes dashboard${RESET}"
echo -e "${CYAN}  - k8s-dashboard-check: Check dashboard access${RESET}"
echo -e "${CYAN}  - k8s-diagnostics    : Run Kubernetes diagnostics${RESET}"
echo -e "${CYAN}  - k8s-test           : Run Kubernetes test suite${RESET}"

# Create convenience script for running the container
RUN_SCRIPT="scripts/run_k8s_tools.sh"
echo -e "\n${CYAN}📌 Creating convenience script: ${BOLD}$RUN_SCRIPT${RESET}"

cat > "$RUN_SCRIPT" << EOF
#!/bin/bash

# 🔱 OMEGA BTC AI - Divine Kubernetes Tools Container Runner 🔱
# This script runs the Kubernetes tools container

# Divine Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
GOLD='\033[0;33m'
RESET='\033[0m'

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "\${RED}❌ Docker is not running. Please start Docker Desktop first.\${RESET}"
    exit 1
fi

# Run the container
echo -e "\${CYAN}📌 Starting Divine Kubernetes Tools container...\${RESET}"
docker run -it --rm \\
    -v /var/run/docker.sock:/var/run/docker.sock \\
    -v \$HOME/.kube:/root/.kube \\
    $IMAGE_NAME:$IMAGE_TAG "\$@"
EOF

chmod +x "$RUN_SCRIPT"
echo -e "${GREEN}✅ Convenience script created: ${BOLD}$RUN_SCRIPT${RESET}"
echo -e "${CYAN}📌 Run with: ${BOLD}./scripts/run_k8s_tools.sh${RESET}"

echo -e "\n${GOLD}JAH JAH BLESS THE CONTAINERIZED KUBERNETES FLOW!${RESET}" 