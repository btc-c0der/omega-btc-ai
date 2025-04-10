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

# 
# OMEGA BTC AI - VNC Image Builder
# ===============================
#
# Build script for creating the custom OMEGA VNC Docker image
#
# Copyright (C) 2024 OMEGA BTC AI Team
# License: GNU General Public License v3.0
#
# JAH BLESS the divine image creation.

# Colors for formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
RESET='\033[0m'
BOLD='\033[1m'

DOCKERFILE="Dockerfile.omega-vnc"
IMAGE_NAME="omega-btc-ai/omega-vnc"
TAG="latest"

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}${BOLD}Error: Docker is not installed or not in PATH.${RESET}"
        echo -e "${YELLOW}Please install Docker and try again.${RESET}"
        exit 1
    fi
}

# Check if Dockerfile exists
check_dockerfile() {
    if [ ! -f "$DOCKERFILE" ]; then
        echo -e "${RED}${BOLD}Error: Dockerfile not found at $DOCKERFILE${RESET}"
        echo -e "${YELLOW}Please ensure you're in the correct directory.${RESET}"
        exit 1
    fi
}

# Build the Docker image
build_image() {
    echo -e "${CYAN}${BOLD}Building OMEGA VNC Docker image...${RESET}"
    echo -e "${YELLOW}This may take several minutes.${RESET}\n"
    
    # Show the Dockerfile contents
    echo -e "${BLUE}${BOLD}Dockerfile Contents:${RESET}"
    cat "$DOCKERFILE" | grep -v "^#" | grep -v "^$"
    echo
    
    # Prompt for confirmation
    echo -e "${YELLOW}Ready to build the image. Continue? (y/n)${RESET}"
    read -p "> " confirm
    
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo -e "${RED}Build cancelled by user.${RESET}"
        exit 0
    fi
    
    # Build the image
    echo -e "\n${CYAN}Building image: $IMAGE_NAME:$TAG${RESET}\n"
    docker build -t "$IMAGE_NAME:$TAG" -f "$DOCKERFILE" .
    
    # Check if build was successful
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}${BOLD}Image built successfully!${RESET}"
        echo -e "${GREEN}Image: $IMAGE_NAME:$TAG${RESET}"
        
        # Show image details
        echo -e "\n${BLUE}Image details:${RESET}"
        docker image inspect "$IMAGE_NAME:$TAG" --format "Size: {{.Size}} bytes"
        echo -e "${CYAN}Created: $(docker image inspect "$IMAGE_NAME:$TAG" --format '{{.Created}}')${RESET}"
    else
        echo -e "\n${RED}${BOLD}Image build failed!${RESET}"
        echo -e "${YELLOW}Please check the error messages above.${RESET}"
    fi
}

# Show help message
show_help() {
    echo -e "${BLUE}${BOLD}OMEGA VNC Image Builder${RESET}"
    echo -e "${CYAN}Usage: $0 [options]${RESET}"
    echo
    echo -e "${YELLOW}Options:${RESET}"
    echo -e "  -h, --help      Show this help message"
    echo -e "  -t, --tag TAG   Set custom tag (default: latest)"
    echo -e "  -f, --file FILE Set custom Dockerfile (default: $DOCKERFILE)"
    echo -e "  -n, --name NAME Set custom image name (default: $IMAGE_NAME)"
    echo
    echo -e "${CYAN}Example:${RESET}"
    echo -e "  $0 --tag dev --file Dockerfile.dev"
}

# Parse command-line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -t|--tag)
                TAG="$2"
                shift 2
                ;;
            -f|--file)
                DOCKERFILE="$2"
                shift 2
                ;;
            -n|--name)
                IMAGE_NAME="$2"
                shift 2
                ;;
            *)
                echo -e "${RED}Unknown option: $1${RESET}"
                show_help
                exit 1
                ;;
        esac
    done
}

# Main function
main() {
    # Display header
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${YELLOW}${BOLD}     OMEGA BTC AI - DIVINE VNC IMAGE BUILDER          ${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${CYAN}Creating the sacred vessel for remote vision${RESET}"
    echo -e "${YELLOW}JAH JAH BLESS THE DIVINE IMAGE!${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}\n"
    
    # Parse command-line arguments
    parse_args "$@"
    
    # Check prerequisites
    check_docker
    check_dockerfile
    
    # Build the image
    build_image
}

# Run the main function
main "$@" 