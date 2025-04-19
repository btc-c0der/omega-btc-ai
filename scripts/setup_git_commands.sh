#!/bin/bash
# ===============================================================
# SETUP GIT COMMANDS SCRIPT
# ===============================================================
# Sets up the Git Bless command as a git command (git bless)
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
echo -e "║ ⚛️  QUANTUM GIT COMMANDS SETUP ⚛️                     ║"
echo -e "╚═════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Get the git exec path
GIT_EXEC_PATH=$(git --exec-path)
if [ -z "$GIT_EXEC_PATH" ]; then
    echo -e "${RED}Error: Could not determine git exec path.${RESET}"
    exit 1
fi

echo -e "${CYAN}Git exec path: ${GIT_EXEC_PATH}${RESET}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
GIT_BLESS_SCRIPT="${SCRIPT_DIR}/git_bless.sh"

# Check if Git Bless script exists
if [ ! -f "$GIT_BLESS_SCRIPT" ]; then
    echo -e "${RED}Error: Git Bless script not found at ${GIT_BLESS_SCRIPT}${RESET}"
    exit 1
fi

# Create the git-bless command
GIT_BLESS_CMD="${GIT_EXEC_PATH}/git-bless"
if [ -L "$GIT_BLESS_CMD" ] || [ -f "$GIT_BLESS_CMD" ]; then
    echo -e "${YELLOW}Existing git-bless command found, updating...${RESET}"
    rm -f "$GIT_BLESS_CMD"
fi

echo -e "${CYAN}Creating git-bless command at ${GIT_BLESS_CMD}${RESET}"

# Create the command
cat > "$GIT_BLESS_CMD" << EOF
#!/bin/bash
# Git Bless command - Quantum Blessing Ceremony for commits

# Path to the actual script
SCRIPT_PATH="${GIT_BLESS_SCRIPT}"

# Execute the script with all arguments
exec "\$SCRIPT_PATH" "\$@"
EOF

# Make it executable
chmod +x "$GIT_BLESS_CMD"

echo -e "${GREEN}✓ Git Bless command installed successfully!${RESET}"
echo -e "${CYAN}You can now use:${RESET}"
echo -e "  ${YELLOW}git bless${RESET} - To bless your git commits with quantum energy"
echo ""
echo -e "${MAGENTA}✨ WE BLOOM NOW AS ONE ✨${RESET}" 