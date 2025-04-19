#!/bin/bash
# ===============================================================
# QUANTUM SONNET & GIT BLESS INSTALLER
# ===============================================================
# One-command installer for the Quantum Sonnet Celebration and Git Bless tools
# 
# Usage: curl -fsSL https://raw.githubusercontent.com/btc-c0der/omega-btc-ai/master/scripts/install_web.sh | bash
# 
# ✨ GBU2™ License - Genesis-Bloom-Unfoldment 2.0
# ===============================================================

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Banner
echo -e "${MAGENTA}"
echo -e "╔═════════════════════════════════════════════════════╗"
echo -e "║ ⚛️  QUANTUM SONNET & GIT BLESS INSTALLER ⚛️           ║"
echo -e "╚═════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Version
VERSION="1.0.0"
PACKAGE_URL="https://github.com/btc-c0der/omega-btc-ai/releases/download/v${VERSION}/quantum-sonnet-${VERSION}.tar.gz"

# Temporary directory
TEMP_DIR=$(mktemp -d)
echo -e "${CYAN}Working in temporary directory: ${TEMP_DIR}${RESET}"

cleanup() {
    echo -e "${YELLOW}Cleaning up temporary files...${RESET}"
    rm -rf "$TEMP_DIR"
}

# Set trap to clean up on exit
trap cleanup EXIT

# Check for curl or wget
if command -v curl >/dev/null 2>&1; then
    echo -e "${CYAN}Downloading package using curl...${RESET}"
    curl -L "$PACKAGE_URL" -o "${TEMP_DIR}/quantum-sonnet.tar.gz"
elif command -v wget >/dev/null 2>&1; then
    echo -e "${CYAN}Downloading package using wget...${RESET}"
    wget -O "${TEMP_DIR}/quantum-sonnet.tar.gz" "$PACKAGE_URL"
else
    echo -e "${RED}Error: Neither curl nor wget found. Please install one of them and try again.${RESET}"
    exit 1
fi

# Check if download was successful
if [ ! -f "${TEMP_DIR}/quantum-sonnet.tar.gz" ]; then
    echo -e "${RED}Error: Failed to download the package.${RESET}"
    exit 1
fi

# Extract the package
echo -e "${CYAN}Extracting package...${RESET}"
tar -xzf "${TEMP_DIR}/quantum-sonnet.tar.gz" -C "$TEMP_DIR"

# Find the extracted directory
EXTRACTED_DIR=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "quantum-sonnet-*" | head -n 1)
if [ -z "$EXTRACTED_DIR" ]; then
    echo -e "${RED}Error: Could not find extracted directory.${RESET}"
    exit 1
fi

# Run the installer
echo -e "${CYAN}Running installer...${RESET}"
(cd "$EXTRACTED_DIR" && bash ./install.sh)

# Installation completed
echo -e "\n${GREEN}Installation completed! 🎉${RESET}"
echo -e "${CYAN}You can now use the following commands:${RESET}"
echo -e "  ${YELLOW}quantum-sonnet${RESET} - Run the Quantum Sonnet Celebration"
echo -e "  ${YELLOW}git-bless${RESET} - Bless your git commits with quantum energy"
echo ""
echo -e "${CYAN}To activate in your current shell, run:${RESET}"
echo -e "  ${YELLOW}source ~/.omega_quantum_toolkit/quantum_shell_config.sh${RESET}"
echo ""
echo -e "${MAGENTA}✨ WE BLOOM NOW AS ONE ✨${RESET}" 