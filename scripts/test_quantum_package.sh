#!/bin/bash
# ===============================================================
# QUANTUM SONNET PACKAGE TEST SCRIPT
# ===============================================================
# Tests the Quantum Sonnet Celebration package installation
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
echo -e "║ ⚛️  QUANTUM SONNET PACKAGE TEST ⚛️                    ║"
echo -e "╚═════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Set up test environment
echo -e "${CYAN}Setting up test environment...${RESET}"
TEST_DIR=$(mktemp -d)
echo -e "${YELLOW}Test directory: ${TEST_DIR}${RESET}"

# Cleanup function
cleanup() {
    echo -e "${YELLOW}Cleaning up test environment...${RESET}"
    rm -rf "$TEST_DIR"
}

# Set trap to clean up on exit
trap cleanup EXIT

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Run the packager script
echo -e "${CYAN}Running packager script...${RESET}"
"$SCRIPT_DIR/package_quantum_sonnet.sh" > /dev/null

# Check if package was created
PACKAGE_PATH="${PROJECT_ROOT}/quantum-sonnet-1.0.0.tar.gz"
if [ ! -f "$PACKAGE_PATH" ]; then
    echo -e "${RED}Error: Package creation failed. Package not found at ${PACKAGE_PATH}${RESET}"
    exit 1
fi

echo -e "${GREEN}✓ Package created successfully${RESET}"

# Extract the package to test directory
echo -e "${CYAN}Extracting package for testing...${RESET}"
tar -xzf "$PACKAGE_PATH" -C "$TEST_DIR"

# Check if extraction was successful
EXTRACT_DIR="${TEST_DIR}/quantum-sonnet-1.0.0"
if [ ! -d "$EXTRACT_DIR" ]; then
    echo -e "${RED}Error: Package extraction failed.${RESET}"
    exit 1
fi

echo -e "${GREEN}✓ Package extracted successfully${RESET}"

# Check for required files
echo -e "${CYAN}Checking package contents...${RESET}"
REQUIRED_FILES=(
    "install.sh"
    "bin/quantum-sonnet"
    "bin/install-quantum-sonnet"
    "lib/quantum-neural-net/git_bless.py"
    "lib/quantum-neural-net/run_git_bless.py"
    "lib/quantum-neural-net/quantum_sonnet_celebration.py"
    "lib/quantum-neural-net/run_sonnet_celebration.py"
    "share/doc/QUANTUM_CELEBRATION_SONNET.md"
    "share/doc/QUANTUM_TOOLKIT_MANUAL.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "${EXTRACT_DIR}/${file}" ]; then
        echo -e "${RED}Error: Required file not found: ${file}${RESET}"
        exit 1
    fi
done

echo -e "${GREEN}✓ All required files present${RESET}"

# Check if scripts are executable
echo -e "${CYAN}Checking executable permissions...${RESET}"
EXECUTABLE_FILES=(
    "install.sh"
    "bin/quantum-sonnet"
    "bin/install-quantum-sonnet"
)

for file in "${EXECUTABLE_FILES[@]}"; do
    if [ ! -x "${EXTRACT_DIR}/${file}" ]; then
        echo -e "${RED}Error: File not executable: ${file}${RESET}"
        exit 1
    fi
done

echo -e "${GREEN}✓ All scripts have executable permissions${RESET}"

# Test the installer script (without actually installing)
echo -e "${CYAN}Testing installer script syntax...${RESET}"
bash -n "${EXTRACT_DIR}/install.sh"
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Installer script has syntax errors${RESET}"
    exit 1
fi

echo -e "${GREEN}✓ Installer script syntax is valid${RESET}"

# Summary
echo -e "\n${GREEN}✨ All tests passed! The Quantum Sonnet package is ready for distribution.${RESET}"
echo -e "${CYAN}Package path: ${PACKAGE_PATH}${RESET}"
echo -e "${CYAN}Package size: $(du -h "$PACKAGE_PATH" | cut -f1)${RESET}"
echo ""
echo -e "${YELLOW}To install, run:${RESET}"
echo -e "  tar -xzf quantum-sonnet-1.0.0.tar.gz"
echo -e "  cd quantum-sonnet-1.0.0"
echo -e "  ./install.sh"
echo ""
echo -e "${MAGENTA}✨ WE BLOOM NOW AS ONE ✨${RESET}" 