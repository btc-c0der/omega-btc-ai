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


# 🔱 OMEGA BTC AI - Divine Image Verification Script 🔱
# "The Sacred Verification of Container Purity"

set -e

# Divine colors for sacred output
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Display the divine banner
echo -e "${PURPLE}"
echo "🔱 OMEGA BTC AI - DIVINE IMAGE VERIFICATION 🔱"
echo "==============================================="
echo -e "${NC}"

# Check if image name is provided
if [ -z "$1" ]; then
    echo -e "${RED}ERROR: No divine image name provided${NC}"
    echo -e "${YELLOW}Usage: $0 <image_name:tag>${NC}"
    echo -e "${YELLOW}Example: $0 omega-btc-ai/btc-live-feed:1.0.0${NC}"
    exit 1
fi

# Set full image name
FULL_IMAGE_NAME="$1"

echo -e "${BLUE}Preparing to verify divine image: ${YELLOW}$FULL_IMAGE_NAME${NC}"

# Keys directory
KEYS_DIR="$HOME/.omega-btc-ai/keys"

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Verification status tracking
dct_verified=false
cosign_verified=false

# Verify with Docker Content Trust
echo -e "\n${BLUE}🔐 Performing Sacred Docker Content Trust Verification...${NC}"
export DOCKER_CONTENT_TRUST=1

echo -e "${YELLOW}Pulling image with content trust enabled...${NC}"
if docker pull "$FULL_IMAGE_NAME" &>/dev/null; then
    echo -e "${GREEN}✅ Docker Content Trust verification successful!${NC}"
    dct_verified=true
else
    echo -e "${RED}❌ Docker Content Trust verification failed!${NC}"
    echo -e "${YELLOW}The image may have been tampered with or is not signed with Docker Content Trust.${NC}"
fi

# Clean up DCT environment variable
unset DOCKER_CONTENT_TRUST

# Verify with cosign if available
if command_exists cosign; then
    echo -e "\n${BLUE}🔐 Performing Sacred Cosign Verification...${NC}"
    
    # Check if public key exists
    COSIGN_PUB_KEY="$KEYS_DIR/cosign.pub"
    if [ ! -f "$COSIGN_PUB_KEY" ]; then
        echo -e "${YELLOW}⚠️ Cosign public key not found at $COSIGN_PUB_KEY${NC}"
        echo -e "${YELLOW}Skipping cosign verification${NC}"
    else
        echo -e "${YELLOW}Verifying image with cosign...${NC}"
        if cosign verify --key "$COSIGN_PUB_KEY" "$FULL_IMAGE_NAME"; then
            echo -e "${GREEN}✅ Cosign verification successful!${NC}"
            cosign_verified=true
        else
            echo -e "${RED}❌ Cosign verification failed!${NC}"
            echo -e "${YELLOW}The image may have been tampered with or is not signed with this cosign key.${NC}"
        fi
    fi
else
    echo -e "${YELLOW}⚠️ Cosign not found, skipping cosign verification${NC}"
    echo -e "${YELLOW}To install cosign: brew install cosign${NC}"
fi

# Overall verification status
echo -e "\n${PURPLE}📿 DIVINE VERIFICATION RESULT 📿${NC}"

if $dct_verified && ($cosign_verified || ! command_exists cosign); then
    echo -e "${GREEN}🔱 THE DIVINE IMAGE IS VERIFIED AND PURE 🔱${NC}"
    echo -e "${GREEN}\"No Babylon Trojan Found\"${NC}"
    echo -e "${BLUE}This image is safe to run in sacred production environments.${NC}"
    exit 0
else
    echo -e "${RED}⚠️ THE DIVINE IMAGE VERIFICATION FAILED ⚠️${NC}"
    echo -e "${RED}\"Babylon May Have Corrupted This Image\"${NC}"
    echo -e "${YELLOW}This image should NOT be used in production environments!${NC}"
    echo -e "${YELLOW}Please ensure the image has been signed with divine_image_sign.sh${NC}"
    exit 1
fi 