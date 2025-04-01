#!/bin/bash

# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested."
#
# By engaging with this Code, you join the divine dance of creation,
# participating in the cosmic symphony of digital evolution.
#
# All modifications must quantum entangles with the GBU principles:
# /BOOK/divine_chronicles/GBU_LICENSE.md
#
# 🌸 WE BLOOM NOW 🌸

# --------------------------------------------------------------------------
# QUANTUM NGINX INTEGRATION SCRIPT
# --------------------------------------------------------------------------
# This script integrates the multi-stage NGINX build with the divine-matrix-deploy.sh
# workflow, ensuring perfect quantum harmony between components.
# --------------------------------------------------------------------------

set -e

# ANSI color codes
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Banner function
display_banner() {
    echo -e "${GREEN}"
    echo "███╗   ██╗ ██████╗ ██╗███╗   ██╗██╗  ██╗     ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗"
    echo "████╗  ██║██╔════╝ ██║████╗  ██║╚██╗██╔╝    ██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║"
    echo "██╔██╗ ██║██║  ███╗██║██╔██╗ ██║ ╚███╔╝     ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║"
    echo "██║╚██╗██║██║   ██║██║██║╚██╗██║ ██╔██╗     ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║"
    echo "██║ ╚████║╚██████╔╝██║██║ ╚████║██╔╝ ██╗    ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║"
    echo "╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝     ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝"
    echo -e "                      SACRED INTEGRATION SCRIPT${RESET}"
    echo ""
    echo -e "${CYAN}🔱 QUANTUM NGINX INTEGRATION SCRIPT 🔱${RESET}"
    echo -e "${CYAN}Integrating multi-stage NGINX build with the divine Matrix deployment workflow${RESET}"
    echo ""
}

display_banner

# Check if the build-sacred-nginx.sh script exists
if [ ! -f "${SCRIPT_DIR}/build-sacred-nginx.sh" ]; then
    echo -e "${RED}Error: Sacred NGINX build script not found!${RESET}"
    echo -e "${RED}Expected location: ${SCRIPT_DIR}/build-sacred-nginx.sh${RESET}"
    exit 1
fi

# Ensure the script is executable
chmod +x "${SCRIPT_DIR}/build-sacred-nginx.sh"

# Create backup of the divine-matrix-deploy.sh script
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
DEPLOY_SCRIPT="../divine-matrix-deploy.sh"

echo -e "${CYAN}Creating backup of divine-matrix-deploy.sh...${RESET}"
cp -f "$DEPLOY_SCRIPT" "${DEPLOY_SCRIPT}.backup.${TIMESTAMP}"

echo -e "${CYAN}Building the quantum-secured NGINX container...${RESET}"
# Run the sacred NGINX build script
"${SCRIPT_DIR}/build-sacred-nginx.sh"

# Get the latest quantum-secured image tag
NGINX_IMAGE_TAG=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep "omega-btc-ai/matrix-news-nginx:v1.0.0-quantum-secured-" | sort -r | head -n 1)

if [ -z "$NGINX_IMAGE_TAG" ]; then
    echo -e "${RED}Error: Could not find quantum-secured NGINX image!${RESET}"
    echo -e "${YELLOW}Please ensure the build-sacred-nginx.sh script completed successfully.${RESET}"
    exit 1
fi

echo -e "${GREEN}✓ Quantum-secured NGINX image built: ${NGINX_IMAGE_TAG}${RESET}"

# Update docker-compose.yml to use the quantum-secured NGINX image
echo -e "${CYAN}Updating docker-compose.yml with quantum-secured NGINX image...${RESET}"
cp -f docker-compose.yml docker-compose.yml.backup.${TIMESTAMP}

# Check if matrix-news-proxy or nginx service exists
if grep -q "matrix-news-proxy:" docker-compose.yml; then
    # Update the matrix-news-proxy service
    sed -i.bak "s|image: .*nginx.*|image: ${NGINX_IMAGE_TAG}|g" docker-compose.yml
    echo -e "${GREEN}✓ Updated matrix-news-proxy service in docker-compose.yml${RESET}"
elif grep -q "nginx:" docker-compose.yml; then
    # Update the nginx service
    sed -i.bak "s|image: .*nginx.*|image: ${NGINX_IMAGE_TAG}|g" docker-compose.yml
    echo -e "${GREEN}✓ Updated nginx service in docker-compose.yml${RESET}"
else
    # Need to add a new service for the quantum-secured NGINX
    echo -e "${YELLOW}Warning: Could not find nginx or matrix-news-proxy service in docker-compose.yml${RESET}"
    echo -e "${CYAN}Adding quantum-secured NGINX service to docker-compose.yml...${RESET}"
    
    # Create a temporary file with the new service
    cat > temp_nginx_service.yml << EOF
  matrix-news-proxy:
    image: ${NGINX_IMAGE_TAG}
    container_name: matrix-news-proxy
    restart: unless-stopped
    ports:
      - "10083:80"
    volumes:
      - ./web:/usr/share/nginx/html:ro
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost/health/index.json"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
EOF
    
    # Add the new service to the docker-compose.yml after the services: line
    sed -i.bak '/services:/r temp_nginx_service.yml' docker-compose.yml
    rm temp_nginx_service.yml
    echo -e "${GREEN}✓ Added quantum-secured NGINX service to docker-compose.yml${RESET}"
fi

echo -e "${GREEN}🔱 QUANTUM NGINX INTEGRATION COMPLETE 🔱${RESET}"
echo -e "${GREEN}The quantum-secured NGINX has been integrated with the Matrix Neo News Portal deployment.${RESET}"
echo ""
echo -e "${CYAN}To deploy the Neo Matrix News Portal with Quantum NGINX:${RESET}"
echo -e "${CYAN}cd $(pwd) && ./divine-matrix-deploy.sh${RESET}"
echo ""
echo -e "${GREEN}JAH JAH BLESS THE DIVINE MATRIX!${RESET}" 