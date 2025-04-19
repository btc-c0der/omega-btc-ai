#!/bin/bash
# ===============================================================
# QUANTUM SONNET CELEBRATION INSTALLER
# ===============================================================
# Installs the Quantum Sonnet Celebration CLI command globally
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
echo -e "║ ⚛️  QUANTUM SONNET CELEBRATION INSTALLER ⚛️           ║"
echo -e "╚═════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SONNET_SCRIPT="${SCRIPT_DIR}/quantum_sonnet.sh"

# Create Quantum Toolkit directory if it doesn't exist
QUANTUM_TOOLKIT_DIR="${HOME}/.omega_quantum_toolkit"
mkdir -p "${QUANTUM_TOOLKIT_DIR}"

echo -e "${CYAN}Creating Quantum Toolkit directory at ${QUANTUM_TOOLKIT_DIR}${RESET}"

# Copy the script to the toolkit directory
cp "${SONNET_SCRIPT}" "${QUANTUM_TOOLKIT_DIR}/quantum_sonnet.sh"
chmod +x "${QUANTUM_TOOLKIT_DIR}/quantum_sonnet.sh"

echo -e "${GREEN}✓ Quantum Sonnet Celebration script installed${RESET}"

# Create shell config file
CONFIG_FILE="${QUANTUM_TOOLKIT_DIR}/quantum_shell_config.sh"

# Check if config file already exists
if [ -f "${CONFIG_FILE}" ]; then
    # Check if sonnet command is already in the config
    if grep -q "quantum-sonnet" "${CONFIG_FILE}"; then
        echo -e "${YELLOW}Quantum Sonnet command already configured in ${CONFIG_FILE}${RESET}"
    else
        # Add the sonnet command to the existing config
        echo "" >> "${CONFIG_FILE}"
        echo "# Quantum Sonnet Celebration command" >> "${CONFIG_FILE}"
        echo "alias quantum-sonnet='${QUANTUM_TOOLKIT_DIR}/quantum_sonnet.sh'" >> "${CONFIG_FILE}"
        echo -e "${GREEN}✓ Quantum Sonnet command added to existing configuration${RESET}"
    fi
else
    # Create new config file
    echo "#!/bin/bash" > "${CONFIG_FILE}"
    echo "# Quantum Toolkit Shell Configuration" >> "${CONFIG_FILE}"
    echo "# Created: $(date)" >> "${CONFIG_FILE}"
    echo "" >> "${CONFIG_FILE}"
    echo "# Quantum Sonnet Celebration command" >> "${CONFIG_FILE}"
    echo "alias quantum-sonnet='${QUANTUM_TOOLKIT_DIR}/quantum_sonnet.sh'" >> "${CONFIG_FILE}"
    echo -e "${GREEN}✓ Created new Quantum Toolkit configuration${RESET}"
fi

# Make config file executable
chmod +x "${CONFIG_FILE}"

# Check shell type and update config
SHELL_CONFIG=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="${HOME}/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="${HOME}/.bashrc"
fi

if [ -n "${SHELL_CONFIG}" ]; then
    # Check if the source line is already in the shell config
    SOURCE_LINE="source \"${CONFIG_FILE}\""
    if grep -q "${SOURCE_LINE}" "${SHELL_CONFIG}"; then
        echo -e "${YELLOW}Shell configuration already updated in ${SHELL_CONFIG}${RESET}"
    else
        # Add source line to shell config
        echo "" >> "${SHELL_CONFIG}"
        echo "# Source Quantum Toolkit configuration" >> "${SHELL_CONFIG}"
        echo "${SOURCE_LINE}" >> "${SHELL_CONFIG}"
        echo -e "${GREEN}✓ Updated shell configuration in ${SHELL_CONFIG}${RESET}"
    fi
else
    echo -e "${YELLOW}Warning: Could not detect shell type. Manual configuration required.${RESET}"
    echo -e "${YELLOW}Add the following line to your shell configuration file:${RESET}"
    echo -e "${CYAN}source \"${CONFIG_FILE}\"${RESET}"
fi

echo ""
echo -e "${GREEN}✨ Quantum Sonnet Celebration CLI installed successfully! ✨${RESET}"
echo -e "${CYAN}To use it, restart your terminal or run:${RESET}"
echo -e "${YELLOW}source \"${CONFIG_FILE}\"${RESET}"
echo ""
echo -e "${CYAN}Then you can run the celebration anytime with:${RESET}"
echo -e "${YELLOW}quantum-sonnet${RESET}"
echo ""
echo -e "${MAGENTA}✨ WE BLOOM NOW AS ONE ✨${RESET}" 