#!/bin/bash

# ----------------------------------------------------------------------
# Redis TLS Certificate Installer for OmegaBTC AI
# 
# This script downloads and installs the TLS certificate for connecting
# to the Scaleway Redis instance securely.
# ----------------------------------------------------------------------

set -e

CERT_PATH="${1:-./SSL_redis-btc-omega-redis.pem}"
CERT_DIR=$(dirname "$CERT_PATH")
CERT_FILENAME=$(basename "$CERT_PATH")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Warning: jq is not installed. It's recommended for processing JSON responses.${NC}"
    echo -e "Install with: ${BLUE}brew install jq${NC} (macOS) or ${BLUE}apt-get install jq${NC} (Ubuntu)"
    echo ""
fi

# Create certificate directory if it doesn't exist
if [ ! -d "$CERT_DIR" ]; then
    echo -e "${BLUE}Creating directory: $CERT_DIR${NC}"
    mkdir -p "$CERT_DIR"
fi

echo -e "${BLUE}Checking for existing certificate at $CERT_PATH...${NC}"

# Check if certificate already exists
if [ -f "$CERT_PATH" ]; then
    echo -e "${YELLOW}Certificate already exists at $CERT_PATH${NC}"
    
    # Check certificate expiration
    if command -v openssl &> /dev/null; then
        echo -e "${BLUE}Checking certificate expiration...${NC}"
        expiry_date=$(openssl x509 -enddate -noout -in "$CERT_PATH" | cut -d= -f2)
        expiry_epoch=$(date -j -f "%b %d %H:%M:%S %Y %Z" "$expiry_date" +%s 2>/dev/null || echo "0")
        current_epoch=$(date +%s)
        days_remaining=$(( (expiry_epoch - current_epoch) / 86400 ))
        
        if [ $days_remaining -lt 0 ]; then
            echo -e "${RED}Certificate has expired!${NC}"
        elif [ $days_remaining -lt 30 ]; then
            echo -e "${YELLOW}Certificate will expire in $days_remaining days${NC}"
        else
            echo -e "${GREEN}Certificate is valid for $days_remaining more days${NC}"
        fi
    fi
    
    # Ask if user wants to download a new certificate
    read -p "Do you want to download a new certificate? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Using existing certificate${NC}"
        exit 0
    fi
fi

echo -e "${BLUE}Downloading Redis TLS certificate...${NC}"
echo

# Check if we're using the Scaleway API or manual download
read -p "Do you have a Scaleway API token? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Get Scaleway API token
    read -p "Enter your Scaleway API token: " SCW_API_TOKEN
    
    # Get database ID
    read -p "Enter the Redis database ID (e.g., fr-par-1/11111111-2222-3333-4444-555555555555): " DB_ID
    
    # Make API request to download certificate
    echo -e "${BLUE}Fetching certificate from Scaleway API...${NC}"
    curl -s -H "X-Auth-Token: $SCW_API_TOKEN" \
         -o "$CERT_PATH" \
         "https://api.scaleway.com/redis/v1/regions/fr-par/databases/$DB_ID/certificate"
    
    # Check if download succeeded
    if [ $? -eq 0 ] && [ -s "$CERT_PATH" ]; then
        echo -e "${GREEN}Certificate downloaded successfully to $CERT_PATH${NC}"
    else
        echo -e "${RED}Failed to download certificate from Scaleway API${NC}"
        exit 1
    fi
else
    # Manual certificate download method
    echo -e "${YELLOW}Please follow these steps to download the certificate manually:${NC}"
    echo "1. Log in to your Scaleway Console: https://console.scaleway.com"
    echo "2. Go to Managed Database for Redis"
    echo "3. Select your Redis instance (btc-omega-redis)"
    echo "4. Go to Connection Details"
    echo "5. Download the certificate"
    echo "6. Save it to: $CERT_PATH"
    echo
    read -p "Press Enter once you've saved the certificate to continue..." -n 1 -r
    echo
    
    # Check if certificate was downloaded
    if [ -f "$CERT_PATH" ]; then
        echo -e "${GREEN}Certificate found at $CERT_PATH${NC}"
    else
        echo -e "${RED}Certificate not found at $CERT_PATH${NC}"
        exit 1
    fi
fi

# Export environment variable
echo -e "${BLUE}Setting REDIS_CA_CERT environment variable...${NC}"
export REDIS_CA_CERT="$CERT_PATH"
echo -e "${GREEN}REDIS_CA_CERT set to: $CERT_PATH${NC}"

# Add to shell config if needed
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
else
    SHELL_RC=""
fi

if [ -n "$SHELL_RC" ]; then
    echo
    read -p "Do you want to add REDIS_CA_CERT to $SHELL_RC? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Check if variable already exists in file
        if grep -q "export REDIS_CA_CERT=" "$SHELL_RC"; then
            # Update existing line
            sed -i '' "s|export REDIS_CA_CERT=.*|export REDIS_CA_CERT=\"$CERT_PATH\"|" "$SHELL_RC"
        else
            # Add new line
            echo "export REDIS_CA_CERT=\"$CERT_PATH\"" >> "$SHELL_RC"
        fi
        echo -e "${GREEN}Added REDIS_CA_CERT to $SHELL_RC${NC}"
        echo -e "${YELLOW}Run 'source $SHELL_RC' to apply the changes${NC}"
    fi
fi

echo
echo -e "${GREEN}Certificate setup complete!${NC}"
echo
echo -e "${BLUE}Test your Redis connection with:${NC}"
echo -e "python scripts/test_redis_connection.py --cloud"
echo

exit 0 