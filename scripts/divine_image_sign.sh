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


# 🔱 OMEGA BTC AI - Divine Image Signing Script 🔱
# "Let No Babylon Slip A Trojan In"

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
echo "🔱 OMEGA BTC AI - DIVINE IMAGE SIGNING 🔱"
echo "=========================================="
echo -e "${NC}"

# Check if image name is provided
if [ -z "$1" ]; then
    echo -e "${RED}ERROR: No divine image name provided${NC}"
    echo -e "${YELLOW}Usage: $0 <image_name> [tag]${NC}"
    echo -e "${YELLOW}Example: $0 omega-btc-ai/btc-live-feed 1.0.0${NC}"
    exit 1
fi

# Set default tag if not provided
IMAGE_NAME="$1"
TAG="${2:-latest}"
FULL_IMAGE_NAME="$IMAGE_NAME:$TAG"

echo -e "${BLUE}Preparing to sign divine image: ${YELLOW}$FULL_IMAGE_NAME${NC}"

# Check if the image exists locally
if ! docker image inspect "$FULL_IMAGE_NAME" &>/dev/null; then
    echo -e "${RED}ERROR: Divine image $FULL_IMAGE_NAME does not exist locally${NC}"
    echo -e "${YELLOW}Please build or pull the image first${NC}"
    exit 1
fi

# Generate key directory if it doesn't exist
KEYS_DIR="$HOME/.omega-btc-ai/keys"
mkdir -p "$KEYS_DIR"

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Sign with Docker Content Trust
echo -e "\n${BLUE}🔐 Performing Sacred Docker Content Trust Signing...${NC}"

# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Create a unique temporary passphrase file
PASSPHRASE_FILE=$(mktemp)
echo "omega-divine-$(date +%s)" > "$PASSPHRASE_FILE"
export DOCKER_CONTENT_TRUST_PASSPHRASE=$(cat "$PASSPHRASE_FILE")

echo -e "${GREEN}Enabled Docker Content Trust${NC}"

# Perform the push with content trust enabled
echo -e "${YELLOW}Pushing image with content trust enabled...${NC}"
echo -e "${YELLOW}(If this is the first time, new keys will be generated)${NC}"

# Try to push with Docker Content Trust
if docker push "$FULL_IMAGE_NAME"; then
    echo -e "${GREEN}✅ Docker Content Trust signing successful!${NC}"
else
    echo -e "${RED}❌ Docker Content Trust signing failed!${NC}"
    # Disable Docker Content Trust regardless of outcome
    unset DOCKER_CONTENT_TRUST
    unset DOCKER_CONTENT_TRUST_PASSPHRASE
    rm -f "$PASSPHRASE_FILE"
    exit 1
fi

# Cleanup Docker Content Trust environment
unset DOCKER_CONTENT_TRUST
unset DOCKER_CONTENT_TRUST_PASSPHRASE
rm -f "$PASSPHRASE_FILE"

# Sign with cosign if available
if command_exists cosign; then
    echo -e "\n${BLUE}🔐 Performing Sacred Cosign Signing...${NC}"
    
    # Generate a cosign key if it doesn't exist
    COSIGN_KEY="$KEYS_DIR/cosign.key"
    if [ ! -f "$COSIGN_KEY" ]; then
        echo -e "${YELLOW}Generating new cosign key pair...${NC}"
        # Generate a random password for cosign key
        COSIGN_PASSWORD=$(openssl rand -base64 20)
        echo "$COSIGN_PASSWORD" > "$KEYS_DIR/cosign.password"
        chmod 600 "$KEYS_DIR/cosign.password"
        
        # Generate the key with the password
        echo "$COSIGN_PASSWORD" | cosign generate-key-pair --output-key-file "$COSIGN_KEY"
        echo -e "${GREEN}✅ Generated new cosign key pair${NC}"
    fi
    
    # Sign the image with cosign
    echo -e "${YELLOW}Signing image with cosign...${NC}"
    COSIGN_PASSWORD=$(cat "$KEYS_DIR/cosign.password")
    echo "$COSIGN_PASSWORD" | cosign sign --key "$COSIGN_KEY" "$FULL_IMAGE_NAME"
    
    echo -e "${GREEN}✅ Cosign signing successful!${NC}"
    
    # Create verification script if it doesn't exist
    VERIFY_SCRIPT="$KEYS_DIR/verify_image.sh"
    if [ ! -f "$VERIFY_SCRIPT" ]; then
        cat > "$VERIFY_SCRIPT" << EOF
#!/bin/bash
# Verification script for divine images

if [ -z "\$1" ]; then
    echo "Usage: \$0 <image_name:tag>"
    exit 1
fi

# Verify with Docker Content Trust
export DOCKER_CONTENT_TRUST=1
echo "Verifying with Docker Content Trust..."
docker pull "\$1" && echo "✅ Docker Content Trust verification successful!" || echo "❌ Docker Content Trust verification failed!"
unset DOCKER_CONTENT_TRUST

# Verify with cosign
echo "Verifying with cosign..."
cosign verify --key $KEYS_DIR/cosign.pub "\$1" && echo "✅ Cosign verification successful!" || echo "❌ Cosign verification failed!"
EOF
        chmod +x "$VERIFY_SCRIPT"
        echo -e "${GREEN}✅ Created image verification script: $VERIFY_SCRIPT${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Cosign not found, skipping cosign signing${NC}"
    echo -e "${YELLOW}To install cosign: brew install cosign${NC}"
fi

echo -e "\n${GREEN}🔱 DIVINE IMAGE SIGNING COMPLETE 🔱${NC}"
echo -e "${BLUE}Image ${YELLOW}$FULL_IMAGE_NAME${BLUE} has been divinely protected${NC}"
echo -e "${BLUE}Remember: \"Let No Babylon Slip A Trojan In\"${NC}"

# Provide verification instructions
echo -e "\n${PURPLE}📿 VERIFICATION INSTRUCTIONS 📿${NC}"
echo -e "${BLUE}To verify this image before running:${NC}"
echo -e "${YELLOW}export DOCKER_CONTENT_TRUST=1${NC}"
echo -e "${YELLOW}docker pull $FULL_IMAGE_NAME${NC}"

if command_exists cosign; then
    echo -e "${YELLOW}cosign verify --key $KEYS_DIR/cosign.pub $FULL_IMAGE_NAME${NC}"
    echo -e "\n${BLUE}Or use the verification script:${NC}"
    echo -e "${YELLOW}$KEYS_DIR/verify_image.sh $FULL_IMAGE_NAME${NC}"
fi

echo -e "\n${PURPLE}JAH JAH BLESS THE SACRED IMAGE VERIFICATION${NC}" 