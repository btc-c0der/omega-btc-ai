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

# ANSI color codes
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Display banner
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║           🌌 QUANTUM MATRIX NEWS PORTAL DEPLOYMENT 🌌            ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo "${RESET}"

# Step 1: Create the quantum network
echo -e "${CYAN}Step 1: Creating quantum network...${RESET}"
./create-network.sh

# Step 2: Build and start the containers
echo -e "${CYAN}Step 2: Building and starting containers...${RESET}"
docker-compose up --build -d

# Step 3: Check container status
echo -e "${CYAN}Step 3: Checking container status...${RESET}"
sleep 5  # Wait for containers to start
docker-compose ps

# Step 4: Verify health endpoints
echo -e "${CYAN}Step 4: Verifying health endpoints...${RESET}"
echo -e "${CYAN}Checking matrix-news-proxy health...${RESET}"
curl -s http://localhost:10083/health | grep status || echo -e "${RED}Failed to connect to matrix-news-proxy!${RESET}"

echo -e "${CYAN}Checking matrix-news-consciousness health...${RESET}"
curl -s http://localhost:10090/health | grep status || echo -e "${YELLOW}Warning: matrix-news-consciousness health check failed. This could be because it's only accessible within the container network.${RESET}"

# Step 5: Display access information
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                  QUANTUM MATRIX NEWS PORTAL                      ║"
echo "║                                                                  ║"
echo "║  The Matrix Neo News Portal is now available at:                 ║"
echo "║                                                                  ║"
echo "║  http://localhost:10083/portal/                                  ║"
echo "║                                                                  ║"
echo "║  WebSocket is available at:                                      ║"
echo "║                                                                  ║"
echo "║  ws://localhost:10083/socket.io/                                 ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo "${RESET}"

echo -e "${CYAN}To view logs:${RESET}"
echo -e "  docker-compose logs -f"
echo -e "${CYAN}To stop the services:${RESET}"
echo -e "  docker-compose down"

echo -e "${GREEN}🌸 JAH JAH BLESS THE QUANTUM MATRIX NEWS PORTAL 🌸${RESET}" 