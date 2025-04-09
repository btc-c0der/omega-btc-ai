#!/bin/bash

# OMEGA BTC AI - Scaleway Deployment Script
# This script automates the process of deploying the system to Scaleway

set -e  # Exit on error

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "=================================================="
echo "  OMEGA BTC AI - SCALEWAY DEPLOYMENT SCRIPT"
echo "  Trap-Aware Dual Traders (TADT) System"
echo "=================================================="
echo -e "${NC}"

# Check if .env.scaleway exists
if [ ! -f .env.scaleway ]; then
    echo -e "${RED}Error: .env.scaleway file not found!${NC}"
    echo "Please create this file with your Scaleway configuration."
    exit 1
fi

# Create required directories
echo -e "${YELLOW}Creating required directories...${NC}"
mkdir -p logs/nginx config logs/trap-aware-traders logs/trap-probability-meter logs/divine-dashboard

# Check Docker and Docker Compose installation
echo -e "${YELLOW}Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Installing Docker...${NC}"
    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

echo -e "${YELLOW}Checking Docker Compose installation...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Installing Docker Compose...${NC}"
    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.19.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Load environment variables
echo -e "${YELLOW}Loading environment variables...${NC}"
export $(grep -v '^#' .env.scaleway | xargs)

# Build and start containers
echo -e "${YELLOW}Building and starting containers...${NC}"
docker-compose -f docker-compose.scaleway.yml build
docker-compose -f docker-compose.scaleway.yml up -d

# Check container status
echo -e "${YELLOW}Checking container status...${NC}"
docker-compose -f docker-compose.scaleway.yml ps

# Print success message
echo -e "${GREEN}"
echo "=================================================="
echo "  DEPLOYMENT COMPLETE!"
echo "=================================================="
echo -e "${NC}"
echo "Your Trap-Aware Dual Traders system is now running on Scaleway."
echo "Access the Divine Dashboard at http://your-server-ip:3000"
echo ""
echo -e "${YELLOW}To monitor logs:${NC}"
echo "docker-compose -f docker-compose.scaleway.yml logs -f"
echo ""
echo -e "${YELLOW}To stop the system:${NC}"
echo "docker-compose -f docker-compose.scaleway.yml down"
echo ""
echo -e "${BLUE}May the divine algorithms guide your trading strategy!${NC}" 