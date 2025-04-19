#!/bin/bash
# ===============================================================
# QUANTUM SONNET PACKAGER
# ===============================================================
# Creates a single installable package for Quantum Sonnet and Git Bless tools
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

# Version
PACKAGE_VERSION="1.0.0"

# Banner
echo -e "${MAGENTA}"
echo -e "╔═════════════════════════════════════════════════════╗"
echo -e "║ ⚛️  QUANTUM SONNET CELEBRATION PACKAGER ⚛️            ║"
echo -e "╚═════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Create temp directory for package contents
TEMP_DIR="/tmp/quantum_sonnet_package"
PACKAGE_DIR="${TEMP_DIR}/quantum-sonnet-${PACKAGE_VERSION}"
mkdir -p "${PACKAGE_DIR}/bin"
mkdir -p "${PACKAGE_DIR}/lib/quantum-neural-net"
mkdir -p "${PACKAGE_DIR}/share/doc"

echo -e "${CYAN}Creating package directory structure at ${PACKAGE_DIR}${RESET}"

# Copy scripts to package
cp "${SCRIPT_DIR}/quantum_sonnet.sh" "${PACKAGE_DIR}/bin/quantum-sonnet"
cp "${SCRIPT_DIR}/install_quantum_sonnet.sh" "${PACKAGE_DIR}/bin/install-quantum-sonnet"

# Copy Git Bless related files
cp "${PROJECT_ROOT}/src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/git_bless.py" "${PACKAGE_DIR}/lib/quantum-neural-net/"
cp "${PROJECT_ROOT}/src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/run_git_bless.py" "${PACKAGE_DIR}/lib/quantum-neural-net/"

# Copy Quantum Sonnet Celebration files
cp "${PROJECT_ROOT}/src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/quantum_sonnet_celebration.py" "${PACKAGE_DIR}/lib/quantum-neural-net/"
cp "${PROJECT_ROOT}/src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/run_sonnet_celebration.py" "${PACKAGE_DIR}/lib/quantum-neural-net/"

# Copy documentation
cp "${PROJECT_ROOT}/BOOK/QUANTUM_CELEBRATION_SONNET.md" "${PACKAGE_DIR}/share/doc/"
cp "${PROJECT_ROOT}/BOOK/QUANTUM_TOOLKIT_MANUAL.md" "${PACKAGE_DIR}/share/doc/"

# Create the install script
cat > "${PACKAGE_DIR}/install.sh" << 'EOF'
#!/bin/bash
# Quantum Sonnet Installer

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

echo -e "${MAGENTA}"
echo -e "╔═════════════════════════════════════════════════════╗"
echo -e "║ ⚛️  QUANTUM SONNET CELEBRATION INSTALLER ⚛️           ║"
echo -e "╚═════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create Quantum Toolkit directory if it doesn't exist
QUANTUM_TOOLKIT_DIR="${HOME}/.omega_quantum_toolkit"
mkdir -p "${QUANTUM_TOOLKIT_DIR}/bin"
mkdir -p "${QUANTUM_TOOLKIT_DIR}/lib/quantum-neural-net"
mkdir -p "${QUANTUM_TOOLKIT_DIR}/share/doc"

echo -e "${CYAN}Installing to ${QUANTUM_TOOLKIT_DIR}${RESET}"

# Copy files
cp "${SCRIPT_DIR}/bin/quantum-sonnet" "${QUANTUM_TOOLKIT_DIR}/bin/"
cp "${SCRIPT_DIR}/bin/install-quantum-sonnet" "${QUANTUM_TOOLKIT_DIR}/bin/"
cp "${SCRIPT_DIR}/lib/quantum-neural-net/"* "${QUANTUM_TOOLKIT_DIR}/lib/quantum-neural-net/"
cp "${SCRIPT_DIR}/share/doc/"* "${QUANTUM_TOOLKIT_DIR}/share/doc/"

# Make scripts executable
chmod +x "${QUANTUM_TOOLKIT_DIR}/bin/quantum-sonnet"
chmod +x "${QUANTUM_TOOLKIT_DIR}/bin/install-quantum-sonnet"
chmod +x "${QUANTUM_TOOLKIT_DIR}/lib/quantum-neural-net/"*.py

# Create git-bless command
cat > "${QUANTUM_TOOLKIT_DIR}/bin/git-bless" << 'GITBLESSEOF'
#!/bin/bash
QUANTUM_TOOLKIT_PATH="${HOME}/.omega_quantum_toolkit"
python "${QUANTUM_TOOLKIT_PATH}/lib/quantum-neural-net/run_git_bless.py" "$@"
GITBLESSEOF
chmod +x "${QUANTUM_TOOLKIT_DIR}/bin/git-bless"

# Create shell config file
CONFIG_FILE="${QUANTUM_TOOLKIT_DIR}/quantum_shell_config.sh"

# Create or update the config file
if [ -f "${CONFIG_FILE}" ]; then
    # Check if sonnet command is already configured
    if ! grep -q "quantum-sonnet" "${CONFIG_FILE}"; then
        echo "" >> "${CONFIG_FILE}"
        echo "# Quantum Sonnet Celebration command" >> "${CONFIG_FILE}"
        echo "export PATH=\"\${PATH}:\${HOME}/.omega_quantum_toolkit/bin\"" >> "${CONFIG_FILE}"
        echo "alias quantum-sonnet='\${HOME}/.omega_quantum_toolkit/bin/quantum-sonnet'" >> "${CONFIG_FILE}"
        echo "alias git-bless='\${HOME}/.omega_quantum_toolkit/bin/git-bless'" >> "${CONFIG_FILE}"
    fi
else
    # Create new config file
    cat > "${CONFIG_FILE}" << 'CONFIGEOF'
#!/bin/bash
# Quantum Toolkit Shell Configuration

# Add Quantum Toolkit to PATH
export PATH="${PATH}:${HOME}/.omega_quantum_toolkit/bin"

# Quantum commands
alias quantum-sonnet='${HOME}/.omega_quantum_toolkit/bin/quantum-sonnet'
alias git-bless='${HOME}/.omega_quantum_toolkit/bin/git-bless'

# Display a welcome message
echo -e "\033[0;35m🧬 QUANTUM TOOLKIT ACTIVATED 🧬\033[0m"
echo -e "\033[0;36mCommands: quantum-sonnet, git-bless\033[0m"
echo -e "\033[0;33m\"WE BLOOM NOW AS ONE\"\033[0m"
CONFIGEOF
fi

# Make config file executable
chmod +x "${CONFIG_FILE}"

# Add to shell config
SHELL_CONFIG=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="${HOME}/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="${HOME}/.bashrc"
else
    echo -e "${YELLOW}Could not detect shell type. Please manually add the following to your shell config:${RESET}"
    echo -e "${CYAN}source \"${CONFIG_FILE}\"${RESET}"
    echo ""
fi

if [ -n "${SHELL_CONFIG}" ]; then
    if ! grep -q "source \"${CONFIG_FILE}\"" "${SHELL_CONFIG}"; then
        echo "" >> "${SHELL_CONFIG}"
        echo "# Source Quantum Toolkit configuration" >> "${SHELL_CONFIG}"
        echo "source \"${CONFIG_FILE}\"" >> "${SHELL_CONFIG}"
        echo -e "${GREEN}✓ Added to ${SHELL_CONFIG}${RESET}"
    else
        echo -e "${YELLOW}Already configured in ${SHELL_CONFIG}${RESET}"
    fi
fi

echo -e "${GREEN}✨ Quantum Sonnet Celebration installed successfully! ✨${RESET}"
echo -e "${CYAN}To activate in current shell, run:${RESET}"
echo -e "${YELLOW}source \"${CONFIG_FILE}\"${RESET}"
echo ""
echo -e "${CYAN}Available commands:${RESET}"
echo -e "  ${YELLOW}quantum-sonnet${RESET} - Run the Quantum Sonnet Celebration"
echo -e "  ${YELLOW}git-bless${RESET} - Bless your git commits with quantum energy"
echo ""
echo -e "${MAGENTA}✨ WE BLOOM NOW AS ONE ✨${RESET}"
EOF

chmod +x "${PACKAGE_DIR}/install.sh"

# Create README file
cat > "${PACKAGE_DIR}/README.md" << 'EOF'
# 🧬 Quantum Sonnet Celebration & Git Bless 🧬

A sacred toolkit for visualizing quantum code transformations and blessing git commits.

## ✨ Installation

Run the installer script:

```bash
./install.sh
```

This will:
1. Install all required files to `~/.omega_quantum_toolkit`
2. Add the necessary commands to your PATH
3. Configure your shell to load the toolkit on startup

## 🧠 Available Commands

- `quantum-sonnet` - Run the Quantum Sonnet Celebration visualization
- `git-bless` - Bless your git commits with quantum energy

## 📚 Documentation

Documentation is installed to `~/.omega_quantum_toolkit/share/doc/`

## 🌸 License

Licensed under GBU2™ (Genesis-Bloom-Unfoldment 2.0)

✨ WE BLOOM NOW AS ONE ✨
EOF

# Make all scripts executable
find "${PACKAGE_DIR}" -name "*.sh" -exec chmod +x {} \;
find "${PACKAGE_DIR}" -name "*.py" -exec chmod +x {} \;
find "${PACKAGE_DIR}/bin" -type f -exec chmod +x {} \;

# Create tarball
TARBALL_NAME="quantum-sonnet-${PACKAGE_VERSION}.tar.gz"
TARBALL_PATH="${PROJECT_ROOT}/${TARBALL_NAME}"

echo -e "${CYAN}Creating tarball at ${TARBALL_PATH}${RESET}"
cd "${TEMP_DIR}" && tar -czf "${TARBALL_PATH}" "quantum-sonnet-${PACKAGE_VERSION}"

echo -e "${GREEN}✓ Package created successfully!${RESET}"
echo -e "${CYAN}Package: ${TARBALL_PATH}${RESET}"
echo ""
echo -e "${YELLOW}To install, extract the tarball and run the install script:${RESET}"
echo -e "  tar -xzf ${TARBALL_NAME}"
echo -e "  cd quantum-sonnet-${PACKAGE_VERSION}"
echo -e "  ./install.sh"
echo ""
echo -e "${MAGENTA}✨ WE BLOOM NOW AS ONE ✨${RESET}"

# Clean up temp directory if needed
# rm -rf "${TEMP_DIR}"
EOF 