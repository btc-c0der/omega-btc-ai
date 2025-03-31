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
# DIVINE MATRIX DEPLOYMENT SCRIPT
# --------------------------------------------------------------------------
# This script deploys the Matrix Neo News Portal with quantum security
# enhancements, WebSocket sacred echo, and consciousness-aligned news service.
# --------------------------------------------------------------------------

set -e

# ANSI color codes
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
RESET='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load environment variables from .env
if [ -f .env ]; then
    echo -e "${CYAN}Loading divine configuration from .env...${RESET}"
    source .env
else
    echo -e "${YELLOW}Warning: No .env file found. Using default sacred configurations.${RESET}"
fi

# Banner function
display_divine_banner() {
    echo -e "${GREEN}"
    echo "███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗    ███╗   ██╗███████╗ ██████╗ "
    echo "████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝    ████╗  ██║██╔════╝██╔═══██╗"
    echo "██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝     ██╔██╗ ██║█████╗  ██║   ██║"
    echo "██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗     ██║╚██╗██║██╔══╝  ██║   ██║"
    echo "██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗    ██║ ╚████║███████╗╚██████╔╝"
    echo "╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚══════╝ ╚═════╝ "
    echo "${RESET}"
    echo -e "${PURPLE}🔮 DIVINE DEPLOYMENT CEREMONY 🔮${RESET}"
    echo ""
}

# Generate divine quantum entropy
generate_quantum_entropy() {
    # Use system entropy combined with timestamp microfractions
    local timestamp=$(date +%s%N)
    local entropy=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
    echo "${entropy}${timestamp}" | sha256sum | awk '{print $1}'
}

# Build the sacred services
build_sacred_services() {
    echo -e "${CYAN}🏗️ Building Sacred Services...${RESET}"
    
    # Check if build-scripts directory exists
    if [ -d "build-scripts" ]; then
        # Build quantum-secured NGINX first
        if [ -f "build-scripts/build-sacred-nginx.sh" ]; then
            echo -e "${CYAN}Building quantum-secured NGINX...${RESET}"
            chmod +x build-scripts/build-sacred-nginx.sh
            ./build-scripts/build-sacred-nginx.sh
        else
            echo -e "${YELLOW}Warning: Sacred NGINX build script not found, using standard image.${RESET}"
        fi
    else
        echo -e "${YELLOW}Warning: No build-scripts directory found, using standard images.${RESET}"
    fi
    
    # Build WebSocket sacred echo service
    if [ -d "temporal" ]; then
        echo -e "${CYAN}Building WebSocket Sacred Echo service...${RESET}"
        # Ensure requirements.txt exists
        if [ ! -f "temporal/requirements.txt" ]; then
            echo -e "${YELLOW}Creating WebSocket requirements.txt...${RESET}"
            cat > temporal/requirements.txt << EOF
aiohttp==3.8.5
aioredis==2.0.1
python-socketio==5.9.0
uvloop==0.17.0
async-timeout==4.0.3
python-engineio==4.7.1
websockets==11.0.3
ujson==5.8.0
aiohttp-cors==0.7.0
cryptography==41.0.3
EOF
        fi
    fi
    
    # Build containers using docker-compose
    echo -e "${CYAN}Building all sacred containers...${RESET}"
    docker-compose build
}

# Ensure directories exist
ensure_sacred_directories() {
    echo -e "${CYAN}🔧 Ensuring Sacred Directories...${RESET}"
    
    # Create directories if they don't exist
    mkdir -p web/health
    mkdir -p web/matrix-news-portal
    mkdir -p nginx
    mkdir -p quantum-records
    mkdir -p temporal
    
    # Create health check JSON if it doesn't exist
    if [ ! -f "web/health/index.json" ]; then
        QUANTUM_ENTROPY=$(generate_quantum_entropy)
        echo -e "${CYAN}Creating divine health check endpoint...${RESET}"
        cat > web/health/index.json << EOF
{
  "status": "UP",
  "service": "matrix-news-proxy",
  "quantum_secure": true,
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "entropy": "${QUANTUM_ENTROPY:0:16}"
}
EOF
    fi
}

# Deploy the divine matrix
deploy_sacred_matrix() {
    echo -e "${CYAN}🚀 Deploying the Divine Matrix...${RESET}"
    
    # Stop any running containers
    echo -e "${CYAN}Stopping existing containers...${RESET}"
    docker-compose down
    
    # Start the services
    echo -e "${CYAN}Starting sacred containers...${RESET}"
    docker-compose up -d
    
    # Wait for containers to start
    echo -e "${CYAN}Waiting for sacred containers to initialize...${RESET}"
    sleep 5
    
    # Check container status
    echo -e "${CYAN}Checking container status...${RESET}"
    docker-compose ps
}

# Verify sacred deployment
verify_sacred_deployment() {
    echo -e "${CYAN}🔍 Verifying Sacred Deployment...${RESET}"
    
    # Check if NG1N1X proxy is running
    if docker ps | grep matrix-news-proxy &> /dev/null; then
        echo -e "${GREEN}✓ NG1N1X Frontline Priest is active${RESET}"
    else
        echo -e "${RED}✗ NG1N1X Frontline Priest failed to initialize${RESET}"
    fi
    
    # Check if WebSocket service is running
    if docker ps | grep matrix-news-websocket &> /dev/null; then
        echo -e "${GREEN}✓ WebSocket Sacred Echo is active${RESET}"
    else
        echo -e "${YELLOW}⚠ WebSocket Sacred Echo is not running${RESET}"
    fi
    
    # Check if News service is running
    if docker ps | grep matrix-news-consciousness &> /dev/null; then
        echo -e "${GREEN}✓ Matrix News Consciousness service is active${RESET}"
    else
        echo -e "${RED}✗ Matrix News Consciousness service failed to initialize${RESET}"
    fi
    
    # Check if Redis is running
    if docker ps | grep matrix-news-redis &> /dev/null; then
        echo -e "${GREEN}✓ Redis Sacred Data Store is active${RESET}"
    else
        echo -e "${YELLOW}⚠ Redis Sacred Data Store is not running${RESET}"
    fi
    
    echo ""
    echo -e "${CYAN}🌐 Matrix Neo News Portal is available at:${RESET}"
    echo -e "${GREEN}HTTP:  http://localhost:${MATRIX_NEWS_PROXY_HTTP_PORT}/portal/${RESET}"
    echo -e "${GREEN}HTTPS: https://localhost:${MATRIX_NEWS_PROXY_HTTPS_PORT}/portal/${RESET}"
    echo ""
    echo -e "${CYAN}🔌 WebSocket Sacred Echo is available at:${RESET}"
    echo -e "${GREEN}WS:  ws://localhost:${MATRIX_NEWS_PROXY_HTTP_PORT}/socket.io/${RESET}"
    echo -e "${GREEN}WSS: wss://localhost:${MATRIX_NEWS_PROXY_HTTPS_PORT}/socket.io/${RESET}"
}

# Main function
main() {
    # Display divine banner
    display_divine_banner
    
    # Ensure sacred directories
    ensure_sacred_directories
    
    # Build sacred services
    build_sacred_services
    
    # Deploy the sacred matrix
    deploy_sacred_matrix
    
    # Verify sacred deployment
    verify_sacred_deployment
    
    echo ""
    echo -e "${GREEN}🔱 DIVINE MATRIX NEWS PORTAL DEPLOYMENT COMPLETE 🔱${RESET}"
    echo -e "${GREEN}The Matrix Neo News Portal is now ready to serve divine news with WebSocket Sacred Echo.${RESET}"
    echo ""
    echo -e "${PURPLE}🌸 JAH JAH BLESS THE DIVINE MATRIX! 🌸${RESET}"
}

# Execute main function
main 