#!/bin/bash

# OMEGA BTC AI - Scaleway Installation Script
# This script sets up the necessary environment on a fresh Scaleway instance

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
echo "  OMEGA BTC AI - SCALEWAY INSTALLATION SCRIPT"
echo "  Trap-Aware Dual Traders (TADT) System"
echo "=================================================="
echo -e "${NC}"

# Update system packages
echo -e "${YELLOW}Updating system packages...${NC}"
apt-get update
apt-get upgrade -y

# Install necessary tools
echo -e "${YELLOW}Installing necessary tools...${NC}"
apt-get install -y git curl wget vim htop tmux jq zip unzip

# Install Docker
echo -e "${YELLOW}Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    usermod -aG docker $USER
else
    echo -e "${GREEN}Docker is already installed.${NC}"
fi

# Install Docker Compose
echo -e "${YELLOW}Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.19.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo -e "${GREEN}Docker Compose is already installed.${NC}"
fi

# Create directory for project
echo -e "${YELLOW}Creating project directory...${NC}"
mkdir -p /opt/omega-btc-ai
cd /opt/omega-btc-ai

# Clone repository (if not already cloned)
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Cloning repository...${NC}"
    git clone https://github.com/btc-c0der/omega-btc-ai.git .
    git checkout cloud-docker-setup
else
    echo -e "${YELLOW}Repository already exists. Pulling latest changes...${NC}"
    git pull
    git checkout cloud-docker-setup
fi

# Make the deployment script executable
echo -e "${YELLOW}Setting up deployment script...${NC}"
chmod +x deploy_to_scaleway.sh

# Create logs and config directories
echo -e "${YELLOW}Creating required directories...${NC}"
mkdir -p logs/nginx config logs/trap-aware-traders logs/trap-probability-meter logs/divine-dashboard

# Check if .env.scaleway exists
if [ ! -f .env.scaleway ]; then
    echo -e "${YELLOW}Creating .env.scaleway template...${NC}"
    cp .env.scaleway.example .env.scaleway
    echo -e "${RED}IMPORTANT: Edit .env.scaleway with your actual configuration values!${NC}"
    echo -e "Use: ${GREEN}nano .env.scaleway${NC}"
fi

# Setup complete
echo -e "${GREEN}"
echo "=================================================="
echo "  INSTALLATION COMPLETE!"
echo "=================================================="
echo -e "${NC}"
echo "Your Scaleway instance is now ready for deployment."
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit .env.scaleway with your actual values"
echo "   nano .env.scaleway"
echo ""
echo "2. Run the deployment script"
echo "   ./deploy_to_scaleway.sh"
echo ""
echo -e "${BLUE}May the divine algorithms guide your trading strategy!${NC}" 