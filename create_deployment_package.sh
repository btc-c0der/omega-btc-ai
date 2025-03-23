#!/bin/bash

# OMEGA BTC AI - Deployment Package Creator
# This script creates a deployment package for Scaleway

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
echo "  OMEGA BTC AI - DEPLOYMENT PACKAGE CREATOR"
echo "  Trap-Aware Dual Traders (TADT) System"
echo "=================================================="
echo -e "${NC}"

# Create a timestamp for the package
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PACKAGE_NAME="omega_btc_ai_scaleway_${TIMESTAMP}.tar.gz"

echo -e "${YELLOW}Creating deployment package: ${PACKAGE_NAME}${NC}"

# Create a temporary directory
TEMP_DIR="temp_deployment_package"
mkdir -p $TEMP_DIR

# Copy necessary files
echo -e "${YELLOW}Copying deployment files...${NC}"
cp docker-compose.scaleway.yml $TEMP_DIR/
cp .env.scaleway.example $TEMP_DIR/
cp install_on_scaleway.sh $TEMP_DIR/
cp deploy_to_scaleway.sh $TEMP_DIR/
cp test_redis_connection.sh $TEMP_DIR/
cp CLOUD_DEPLOYMENT.md $TEMP_DIR/
cp -r docker $TEMP_DIR/

# Copy essential code files
echo -e "${YELLOW}Copying essential code files...${NC}"
mkdir -p $TEMP_DIR/omega_ai
cp -r omega_ai/tools $TEMP_DIR/omega_ai/
cp -r omega_ai/trading $TEMP_DIR/omega_ai/
cp -r omega_ai/utils $TEMP_DIR/omega_ai/
cp -r omega_ai/visualizer $TEMP_DIR/omega_ai/
cp -r omega_ai/__init__.py $TEMP_DIR/omega_ai/

# Create the package
echo -e "${YELLOW}Creating tarball...${NC}"
tar -czf $PACKAGE_NAME -C $TEMP_DIR .

# Clean up
echo -e "${YELLOW}Cleaning up temporary files...${NC}"
rm -rf $TEMP_DIR

# Done
echo -e "${GREEN}"
echo "=================================================="
echo "  DEPLOYMENT PACKAGE CREATED SUCCESSFULLY!"
echo "=================================================="
echo -e "${NC}"
echo "Package: ${PACKAGE_NAME}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Transfer the package to your Scaleway instance:"
echo "   scp ${PACKAGE_NAME} root@your-scaleway-ip:/opt/"
echo ""
echo "2. On your Scaleway instance, extract the package:"
echo "   mkdir -p /opt/omega-btc-ai"
echo "   tar -xzf /opt/${PACKAGE_NAME} -C /opt/omega-btc-ai"
echo ""
echo "3. Follow the instructions in CLOUD_DEPLOYMENT.md to complete the setup."
echo ""
echo -e "${BLUE}May the divine algorithms guide your trading strategy!${NC}" 