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
# DIVINE MATRIX NEWS DEPLOYMENT SCRIPT
# --------------------------------------------------------------------------
# This script deploys the Matrix News Consciousness service without 
# disturbing the sacred container. It creates a bridge between the 
# existing Divine Matrix system and the new consciousness-aligned news
# integration.
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
cd "$SCRIPT_DIR"

# Banner function
display_banner() {
    echo -e "${GREEN}"
    echo "████████╗██╗  ██╗███████╗    ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗"
    echo "╚══██╔══╝██║  ██║██╔════╝    ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝"
    echo "   ██║   ███████║█████╗      ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ "
    echo "   ██║   ██╔══██║██╔══╝      ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ "
    echo "   ██║   ██║  ██║███████╗    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗"
    echo "   ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝"
    echo -e "                      NEO NEWS CONSCIOUSNESS PORTAL${RESET}"
    echo ""
    echo -e "${CYAN}🔱 DIVINE IMMUTABLE DEPLOYMENT SCRIPT 🔱${RESET}"
    echo ""
}

display_banner

# Configuration variables
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
IMAGE_TAG="v1.0.0-neo-style-${TIMESTAMP}"
CONTAINER_NAME="matrix-news-consciousness"
NETWORK_NAME="matrix-news-network"

# Step 1: Validate the sacred container
echo -e "${CYAN}Step 1: Validating the sacred container environment...${RESET}"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not in PATH${RESET}"
    exit 1
fi

# Check if the docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose is not installed or not in PATH${RESET}"
    exit 1
fi

echo -e "${GREEN}✓ Docker environment validated${RESET}"

# Step 2: Check if the sacred container is running
echo -e "${CYAN}Step 2: Checking if the sacred container is running...${RESET}"
if ! docker ps | grep news-service &> /dev/null; then
    echo -e "${YELLOW}Warning: The sacred news-service container does not appear to be running.${RESET}"
    echo -e "${YELLOW}The Matrix Neo News Portal will operate in standalone mode.${RESET}"
    STANDALONE_MODE=true
else
    echo -e "${GREEN}✓ Sacred container detected${RESET}"
    STANDALONE_MODE=false
fi

# Step 3: Build the immutable container image
echo -e "${CYAN}Step 3: Building the divine Neo-style Matrix News immutable container...${RESET}"

# Ensure the web directory has proper permissions
echo -e "${CYAN}Ensuring web assets have proper permissions...${RESET}"
chmod -R 755 ./web

# Check if there are any Git changes that haven't been committed
if command -v git &> /dev/null && git rev-parse --is-inside-work-tree &> /dev/null; then
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}Warning: You have uncommitted changes in your Git repository.${RESET}"
        echo -e "${YELLOW}It's recommended to commit your changes before building an immutable container.${RESET}"
        read -p "Do you want to continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${RED}Deployment aborted.${RESET}"
            exit 1
        fi
    fi
fi

# Docker build with the neo-style tag
echo -e "${CYAN}Building docker image omega-btc-ai/matrix-news:${IMAGE_TAG}...${RESET}"
docker build -t "omega-btc-ai/matrix-news:${IMAGE_TAG}" \
    --label "org.opencontainers.image.created=$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --label "org.opencontainers.image.version=${IMAGE_TAG}" \
    --label "org.opencontainers.image.authors=OMEGA BTC AI DIVINE COLLECTIVE" \
    --label "org.opencontainers.image.vendor=OMEGA BTC AI" \
    --label "org.opencontainers.image.title=Matrix Neo News Consciousness Portal" \
    --label "org.opencontainers.image.description=The Matrix Neo-style News Portal with consciousness alignment" \
    --no-cache .

echo -e "${GREEN}✓ Divine image built successfully${RESET}"

# Step 4: Update docker-compose with the new image tag
echo -e "${CYAN}Step 4: Updating docker-compose configuration...${RESET}"

# Create a backup of the original docker-compose.yml
cp docker-compose.yml docker-compose.yml.backup.${TIMESTAMP}

# Update the image tag in the docker-compose file
sed -i.bak "s|image: omega-btc-ai/matrix-news:consciousness-.*|image: omega-btc-ai/matrix-news:${IMAGE_TAG}|g" docker-compose.yml

echo -e "${GREEN}✓ docker-compose.yml updated with new image tag${RESET}"

# Step 5: Deploy using docker-compose
echo -e "${CYAN}Step 5: Deploying the Matrix Neo News Portal...${RESET}"

# Stop any existing containers
echo -e "${CYAN}Stopping existing containers...${RESET}"
docker-compose down -v || true

# Start the new containers
echo -e "${CYAN}Starting Neo-style Matrix News Portal containers...${RESET}"
docker-compose up -d

# Wait for containers to be fully up
echo -e "${CYAN}Waiting for containers to initialize...${RESET}"
sleep 10

# Verify deployment
echo -e "${CYAN}Verifying deployment...${RESET}"
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓ Matrix Neo News Portal deployed successfully!${RESET}"
else
    echo -e "${RED}Error: Deployment verification failed. Please check docker-compose logs.${RESET}"
    docker-compose logs
    exit 1
fi

# Step 6: Display access information
echo -e "${CYAN}Step 6: Deployment Complete${RESET}"
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}║                                                            ║${RESET}"
echo -e "${GREEN}║  🔱 THE MATRIX NEO NEWS PORTAL HAS BEEN DEPLOYED! 🔱       ║${RESET}"
echo -e "${GREEN}║                                                            ║${RESET}"
echo -e "${GREEN}╠════════════════════════════════════════════════════════════╣${RESET}"
echo -e "${GREEN}║                                                            ║${RESET}"
echo -e "${GREEN}║  Access the Neo-style Matrix News Portal at:               ║${RESET}"
echo -e "${GREEN}║  http://localhost:10083/                                   ║${RESET}"
echo -e "${GREEN}║                                                            ║${RESET}"
echo -e "${GREEN}║  Container image: omega-btc-ai/matrix-news:${IMAGE_TAG}    ║${RESET}"
echo -e "${GREEN}║                                                            ║${RESET}"
if [ "$STANDALONE_MODE" = true ]; then
    echo -e "${YELLOW}║  NOTE: Running in standalone mode (no sacred container)      ║${RESET}"
else
    echo -e "${GREEN}║  Integration: Connected to sacred news-service container      ║${RESET}"
fi
echo -e "${GREEN}║                                                            ║${RESET}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${RESET}"

echo ""
echo -e "${CYAN}To view logs: ${RESET}docker-compose logs -f"
echo -e "${CYAN}To stop service: ${RESET}docker-compose down"
echo ""
echo -e "${GREEN}JAH JAH BLESS THE DIVINE MATRIX!${RESET}"
echo "" 