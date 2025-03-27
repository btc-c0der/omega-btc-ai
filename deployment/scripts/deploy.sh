#!/bin/bash

# OMEGA BTC AI - Digital Ocean Deployment Script
# ==============================================

# Set error handling
set -e

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
RESET='\033[0m'

echo -e "${PURPLE}"
echo "🔱 OMEGA BTC AI - Digital Ocean Deployment 🔱"
echo -e "==========================================${RESET}"
echo

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}❌ Error: doctl not found. Please install the Digital Ocean CLI.${RESET}"
    echo "Run: brew install doctl"
    exit 1
fi

# Check authentication
echo -e "${YELLOW}🔄 Checking Digital Ocean authentication...${RESET}"
if ! doctl account get &> /dev/null; then
    echo -e "${RED}❌ Error: Not authenticated with Digital Ocean.${RESET}"
    echo "Run 'doctl auth init' to authenticate."
    exit 1
fi

# Check if SSL certificate exists
CERT_PATH="deployment/digitalocean/certificates/SSL_redis-btc-omega-redis.pem"
if [ ! -f "$CERT_PATH" ]; then
    echo -e "${YELLOW}⚠️ SSL certificate not found at $CERT_PATH${RESET}"
    echo -e "${YELLOW}Creating directory for SSL certificates...${RESET}"
    mkdir -p "deployment/digitalocean/certificates"
    
    echo -e "${YELLOW}Using default self-signed certificate for Redis connection.${RESET}"
    echo -e "${YELLOW}For production, replace with proper SSL certificate.${RESET}"
    
    # Check if openssl is installed
    if command -v openssl &> /dev/null; then
        echo -e "${YELLOW}Generating self-signed certificate...${RESET}"
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout "$CERT_PATH" -out "$CERT_PATH" \
            -subj "/CN=localhost" 2>/dev/null
        
        echo -e "${GREEN}✅ Self-signed certificate generated.${RESET}"
    else
        echo -e "${RED}❌ OpenSSL not found. Cannot generate self-signed certificate.${RESET}"
        echo "Please install OpenSSL or manually create the certificate at $CERT_PATH"
        exit 1
    fi
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}⚠️ requirements.txt not found in root directory.${RESET}"
    echo -e "${YELLOW}Creating requirements.txt file...${RESET}"
    
    # Create basic requirements file
    cat > requirements.txt << EOF
# OMEGA BTC AI - BTC Live Feed v2 Dependencies
websockets>=10.0,<11.0
redis>=4.5.0,<5.0
aiohttp>=3.8.0,<4.0
asyncio>=3.4.3,<4.0
python-dotenv>=1.0.0,<2.0
cryptography>=40.0.0,<41.0
uvicorn>=0.18.0,<0.19.0
fastapi>=0.95.0,<0.96.0
pydantic>=1.10.0,<2.0
EOF
    
    echo -e "${GREEN}✅ requirements.txt created.${RESET}"
fi

# Prepare deployment
echo -e "${YELLOW}🔄 Preparing deployment...${RESET}"

# Validate app.yaml
if [ ! -f "deployment/digitalocean/app.yaml" ]; then
    echo -e "${RED}❌ Error: app.yaml not found at deployment/digitalocean/app.yaml${RESET}"
    exit 1
fi

# Deploy the application
echo -e "${YELLOW}🚀 Deploying to Digital Ocean App Platform...${RESET}"
APP_ID=$(doctl apps create --spec deployment/digitalocean/app.yaml --format ID --no-header)

if [ -n "$APP_ID" ]; then
    echo -e "${GREEN}✅ Deployment initiated!${RESET}"
    echo -e "${BLUE}📊 App ID: ${YELLOW}$APP_ID${RESET}"
    echo
    echo -e "${BLUE}Monitor deployment status:${RESET}"
    echo -e "${YELLOW}doctl apps get $APP_ID${RESET}"
    echo
    echo -e "${BLUE}View application logs:${RESET}"
    echo -e "${YELLOW}doctl apps logs $APP_ID${RESET}"
else
    echo -e "${RED}❌ Deployment failed.${RESET}"
    exit 1
fi

echo
echo -e "${PURPLE}==========================================${RESET}"
echo -e "${GREEN}🔱 OMEGA BTC AI - DEPLOYMENT COMPLETE 🔱${RESET}"
echo -e "${BLUE}(It may take a few minutes for the app to be fully deployed)${RESET}"
echo 