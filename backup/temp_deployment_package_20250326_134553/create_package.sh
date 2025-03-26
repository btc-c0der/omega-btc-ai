#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Creating BTC Live Feed Deployment Package ===${NC}"
echo

# Create output directory if it doesn't exist
mkdir -p output

# Create the certs directory
mkdir -p certs
touch certs/.gitkeep

# Get package version and date
VERSION=$(date +"%Y%m%d.%H%M")
PACKAGE_NAME="btc_live_feed_package_${VERSION}.zip"

echo -e "${YELLOW}Package version: ${VERSION}${NC}"
echo -e "${YELLOW}Creating: ${PACKAGE_NAME}${NC}"
echo

# List of files to include
FILES=(
    "docker-compose.scaleway.yml"
    "docker-compose.local.yml"
    "docker/BTCLiveFeed.Dockerfile"
    "docker/nginx.conf"
    "btc_live_feed_cloud.py"
    "btc_gpu_accelerator.py"
    "redis_manager_cloud.py"
    "deploy_btc_feed.sh"
    "test_local_deployment.sh"
    "monitor_redis.py"
    "test_redis_data.py"
    "verify_deployment.py"
    "README.md"
    "requirements.txt"
    "certs/.gitkeep"
)

# Create the package
if zip -r "output/${PACKAGE_NAME}" "${FILES[@]}" 2>/dev/null; then
    echo -e "${GREEN}✅ Package created successfully at output/${PACKAGE_NAME}${NC}"
else
    echo -e "${RED}Failed to create package${NC}"
    exit 1
fi

# Calculate package size
SIZE=$(du -h "output/${PACKAGE_NAME}" | cut -f1)
echo -e "${YELLOW}Package size: ${SIZE}${NC}"

# List the contents of the package
echo
echo -e "${BLUE}Package contents:${NC}"
unzip -l "output/${PACKAGE_NAME}" | tail -n+4 | head -n-2 | awk '{print "  - " $4}'

echo
echo -e "${BLUE}=== Deployment Instructions ===${NC}"
echo -e "${GREEN}1. Transfer the package to your Scaleway instance:${NC}"
echo -e "   scp output/${PACKAGE_NAME} user@your-scaleway-instance:/path/to/destination/"
echo
echo -e "${GREEN}2. SSH to your Scaleway instance:${NC}"
echo -e "   ssh user@your-scaleway-instance"
echo
echo -e "${GREEN}3. Extract the package:${NC}"
echo -e "   unzip ${PACKAGE_NAME} -d btc_live_feed"
echo
echo -e "${GREEN}4. Change to the extracted directory:${NC}"
echo -e "   cd btc_live_feed"
echo
echo -e "${GREEN}5. Run the deployment script:${NC}"
echo -e "   chmod +x deploy_btc_feed.sh"
echo -e "   ./deploy_btc_feed.sh"
echo
echo -e "${BLUE}=== Package Creation Complete ===${NC}" 