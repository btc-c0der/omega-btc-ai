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


# 🔱 OMEGA BTC AI - Divine IBR CLI Installation Script 🔱
# This script installs the IBR España CLI tool globally

# Divine Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
GOLD='\033[0;33m'
RESET='\033[0m'
BOLD='\033[1m'

# Divine Banner
echo -e "${GOLD}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                           "
echo "  𝕴𝕭𝕽 𝕰𝕾𝕻𝕬Ñ𝕬 𝕯𝕴𝖁𝕴𝕹𝕰 𝕮𝕷𝕴 𝕴𝕹𝕾𝕿𝕬𝕷𝕷𝕬𝕿𝕴𝕺𝕹  "
echo "                                                           "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Determine script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check Python version
check_python() {
    echo -e "${CYAN}Checking Python version...${RESET}"
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}Error: Python 3 is required but not found.${RESET}"
        exit 1
    fi

    # Check Python version
    PY_VERSION=$($PYTHON_CMD -c "import sys; print('{}.{}'.format(sys.version_info.major, sys.version_info.minor))")
    PY_MAJOR=$(echo $PY_VERSION | cut -d. -f1)
    
    if [ "$PY_MAJOR" -lt 3 ]; then
        echo -e "${RED}Error: Python 3.6+ is required, but found Python $PY_VERSION${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}Found Python $PY_VERSION${RESET}"
}

# Install dependencies
install_dependencies() {
    echo -e "${CYAN}Installing dependencies...${RESET}"
    
    # Check if pip is available
    if ! command_exists pip && ! command_exists pip3; then
        echo -e "${RED}Error: pip is required but not found.${RESET}"
        echo -e "${YELLOW}Please install pip first and try again.${RESET}"
        exit 1
    fi
    
    # Use pip3 if available, otherwise fall back to pip
    if command_exists pip3; then
        PIP_CMD="pip3"
    else
        PIP_CMD="pip"
    fi
    
    # Install dependencies from requirements file
    REQUIREMENTS_FILE="$SCRIPT_DIR/requirements-ibr-cli.txt"
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo -e "${CYAN}Installing required packages from $REQUIREMENTS_FILE${RESET}"
        $PIP_CMD install -r "$REQUIREMENTS_FILE"
    else
        echo -e "${RED}Error: Requirements file not found at $REQUIREMENTS_FILE${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}Dependencies installed successfully${RESET}"
}

# Create symbolic link to make CLI globally available
install_cli() {
    echo -e "${CYAN}Installing IBR CLI...${RESET}"
    
    CLI_SCRIPT="$SCRIPT_DIR/ibr_cli.py"
    TARGET_DIR="/usr/local/bin"
    TARGET_LINK="$TARGET_DIR/ibr"
    
    # Check if the CLI script exists
    if [ ! -f "$CLI_SCRIPT" ]; then
        echo -e "${RED}Error: CLI script not found at $CLI_SCRIPT${RESET}"
        exit 1
    fi
    
    # Make sure the script is executable
    chmod +x "$CLI_SCRIPT"
    
    # Create symbolic link (requires sudo)
    echo -e "${YELLOW}Creating symbolic link at $TARGET_LINK (requires sudo)${RESET}"
    sudo ln -sf "$CLI_SCRIPT" "$TARGET_LINK"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}IBR CLI installed successfully at $TARGET_LINK${RESET}"
    else
        echo -e "${RED}Error: Failed to create symbolic link. Try running with sudo.${RESET}"
        exit 1
    fi
}

# Create config directory if needed
create_config_dir() {
    CONFIG_DIR="$HOME/.ibr"
    echo -e "${CYAN}Creating configuration directory at $CONFIG_DIR${RESET}"
    
    mkdir -p "$CONFIG_DIR"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Configuration directory created successfully${RESET}"
    else
        echo -e "${RED}Error: Failed to create configuration directory${RESET}"
        exit 1
    fi
}

# Run tests
run_tests() {
    echo -e "${CYAN}Running tests...${RESET}"
    
    TESTS_DIR="$SCRIPT_DIR/tests"
    
    if [ -d "$TESTS_DIR" ]; then
        cd "$SCRIPT_DIR"
        if command_exists pytest; then
            pytest tests/
        else
            $PYTHON_CMD -m pytest tests/
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}All tests passed${RESET}"
        else
            echo -e "${RED}Some tests failed${RESET}"
            echo -e "${YELLOW}Continuing with installation anyway...${RESET}"
        fi
    else
        echo -e "${YELLOW}Warning: Tests directory not found at $TESTS_DIR${RESET}"
    fi
}

# Display usage information
show_usage() {
    echo -e "${CYAN}IBR CLI is now installed!${RESET}"
    echo
    echo -e "Usage:"
    echo -e "  ${BOLD}ibr${RESET} [command] [options]"
    echo
    echo -e "Commands:"
    echo -e "  ${BOLD}k8s${RESET}        - Kubernetes management commands"
    echo -e "  ${BOLD}instagram${RESET}  - Instagram integration commands"
    echo -e "  ${BOLD}config${RESET}     - Configuration management"
    echo
    echo -e "For a complete list of commands, run:"
    echo -e "  ${BOLD}ibr --help${RESET}"
    echo
    echo -e "${YELLOW}JAH JAH BLESS YOUR DIVINE USE OF THE IBR CLI!${RESET}"
}

# Main installation process
main() {
    check_python
    install_dependencies
    run_tests
    create_config_dir
    install_cli
    show_usage
}

main 