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

# Network name
NETWORK_NAME="quantum_matrix_news_matrix_news_network"

# Display banner
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║           🌌 QUANTUM MATRIX NEWS NETWORK CREATION 🌌             ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo "${RESET}"

# Check if the network already exists
if docker network inspect "$NETWORK_NAME" &>/dev/null; then
    echo -e "${YELLOW}The quantum network '$NETWORK_NAME' already exists.${RESET}"
    echo -e "${CYAN}Would you like to recreate it? (y/n)${RESET}"
    read -r answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}Removing existing network...${RESET}"
        docker network rm "$NETWORK_NAME"
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to remove the existing network.${RESET}"
            echo -e "${YELLOW}This may be because containers are still connected to it.${RESET}"
            echo -e "${CYAN}Would you like to disconnect all containers from this network? (y/n)${RESET}"
            read -r disconnect
            if [[ "$disconnect" =~ ^[Yy]$ ]]; then
                echo -e "${CYAN}Disconnecting all containers from the network...${RESET}"
                for container in $(docker network inspect -f '{{range .Containers}}{{.Name}} {{end}}' "$NETWORK_NAME"); do
                    echo -e "${CYAN}Disconnecting $container...${RESET}"
                    docker network disconnect -f "$NETWORK_NAME" "$container"
                done
                echo -e "${CYAN}Removing network again...${RESET}"
                docker network rm "$NETWORK_NAME"
                if [ $? -ne 0 ]; then
                    echo -e "${RED}Failed to remove network even after disconnecting containers.${RESET}"
                    echo -e "${RED}Please check if any containers are still using this network.${RESET}"
                    exit 1
                fi
            else
                echo -e "${YELLOW}Operation cancelled.${RESET}"
                exit 0
            fi
        fi
    else
        echo -e "${GREEN}Using existing network.${RESET}"
        exit 0
    fi
fi

# Create the network
echo -e "${CYAN}Creating quantum network '$NETWORK_NAME'...${RESET}"
docker network create --driver bridge "$NETWORK_NAME"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Quantum network created successfully!${RESET}"
    echo -e "${CYAN}Network Details:${RESET}"
    docker network inspect "$NETWORK_NAME" | grep -E 'Name|Driver|IPAM|Subnet|Gateway'
else
    echo -e "${RED}✗ Failed to create the quantum network.${RESET}"
    exit 1
fi

echo -e "${GREEN}The network is ready for the Matrix Neo News Portal.${RESET}"
echo -e "${CYAN}You can now run docker-compose up to start the services.${RESET}"

exit 0 