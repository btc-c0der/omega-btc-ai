#!/bin/bash

# OMEGA BTC AI - Redis SSL Certificate Deployment Script
# ====================================================
# This script deploys the Redis SSL certificate to Digital Ocean App Platform

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Logo display
echo -e "${MAGENTA}"
echo "🔱 OMEGA BTC AI - Redis SSL Certificate Deployment 🔱"
echo -e "${RESET}"

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}❌ Error: doctl not found. Please install the Digital Ocean CLI.${RESET}"
    echo "Installation instructions: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if authenticated
echo -e "${YELLOW}🔄 Checking Digital Ocean authentication...${RESET}"
if ! doctl account get &> /dev/null; then
    echo -e "${RED}❌ Error: Not authenticated with Digital Ocean.${RESET}"
    echo "Please run 'doctl auth init' and try again."
    exit 1
fi

# Configuration variables
APP_NAME="omega-btc-ai-live-feed-v3"
CERT_FILE="SSL_redis-btc-omega-redis.pem"

# Check if certificate file exists
if [ -z "$1" ]; then
    echo -e "${YELLOW}⚠️ No certificate file provided.${RESET}"
    
    # Check if it exists in the current directory
    if [ -f "./${CERT_FILE}" ]; then
        CERT_PATH="./${CERT_FILE}"
        echo -e "${GREEN}✅ Found certificate file in current directory: ${CERT_PATH}${RESET}"
    elif [ -f "../../../${CERT_FILE}" ]; then
        CERT_PATH="../../../${CERT_FILE}"
        echo -e "${GREEN}✅ Found certificate file in project root: ${CERT_PATH}${RESET}"
    else
        echo -e "${RED}❌ Certificate file not found.${RESET}"
        echo "Please specify the path to the certificate file as an argument:"
        echo "  ./deploy_cert.sh /path/to/SSL_redis-btc-omega-redis.pem"
        exit 1
    fi
else
    CERT_PATH="$1"
    if [ ! -f "$CERT_PATH" ]; then
        echo -e "${RED}❌ Certificate file not found at ${CERT_PATH}${RESET}"
        exit 1
    fi
fi

# Get app ID
echo -e "${YELLOW}🔍 Checking if app exists...${RESET}"
APP_ID=$(doctl apps list --format ID,Spec.Name --no-header | grep "$APP_NAME" | awk '{print $1}')

if [ -z "$APP_ID" ]; then
    echo -e "${RED}❌ App not found. Please deploy the app first.${RESET}"
    exit 1
fi

echo -e "${GREEN}✅ Found app: ${APP_NAME} (ID: ${APP_ID})${RESET}"

# Get component ID for each component
echo -e "${YELLOW}🔍 Getting component details...${RESET}"
COMPONENTS=$(doctl apps list-deployments $APP_ID --format ID,Phase --no-header | grep "active" | head -1 | awk '{print $1}')
DEPLOYMENT_ID=$(echo $COMPONENTS)

if [ -z "$DEPLOYMENT_ID" ]; then
    echo -e "${RED}❌ No active deployment found.${RESET}"
    exit 1
fi

echo -e "${GREEN}✅ Found active deployment: ${DEPLOYMENT_ID}${RESET}"

# Get components
echo -e "${YELLOW}🔍 Getting component details...${RESET}"
COMPONENTS=$(doctl apps get-deployment $APP_ID $DEPLOYMENT_ID --format Components --no-header)

echo -e "${BLUE}Components:${RESET}"
echo "$COMPONENTS"

# Create temporary directory for certificate
TEMP_DIR=$(mktemp -d)
cp "$CERT_PATH" "$TEMP_DIR/${CERT_FILE}"

# Upload certificate to each component
echo -e "${YELLOW}🔄 Uploading certificate to components...${RESET}"
echo -e "${YELLOW}This operation requires your app to be deployed and running.${RESET}"
echo -e "${YELLOW}If this fails, please try again after confirming your app is running.${RESET}"

for COMPONENT in $COMPONENTS; do
    # Skip empty lines
    if [ -z "$COMPONENT" ]; then
        continue
    fi
    
    # Clean up component name (remove brackets, commas, etc.)
    COMPONENT=$(echo $COMPONENT | tr -d '[] ,')
    
    echo -e "${BLUE}Uploading certificate to component: $COMPONENT${RESET}"
    
    # Use doctl ssh to upload the certificate
    doctl apps upload $APP_ID --component $COMPONENT --source "$TEMP_DIR/${CERT_FILE}" --destination "/workspace/${CERT_FILE}"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to upload certificate to component: $COMPONENT${RESET}"
        echo -e "${YELLOW}You may need to SSH into the component manually and upload the certificate:${RESET}"
        echo -e "${YELLOW}doctl apps ssh $APP_ID --component $COMPONENT${RESET}"
    else
        echo -e "${GREEN}✅ Certificate uploaded to component: $COMPONENT${RESET}"
    fi
done

# Clean up
rm -rf "$TEMP_DIR"

echo -e "${GREEN}🎉 Certificate deployment completed!${RESET}"
echo -e "${BLUE}You can verify the certificate is in place by SSH'ing into the components:${RESET}"
echo -e "${BLUE}doctl apps ssh $APP_ID --component <component-name>${RESET}"
echo -e "${BLUE}Then run: ls -la /workspace/${CERT_FILE}${RESET}" 