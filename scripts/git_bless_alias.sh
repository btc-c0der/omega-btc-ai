#!/bin/bash
# ╭────────────────────────────────────────────────────────────────────────────╮
# │                                                                            │
# │                 🔱 OMEGA GIT BLESS ALIAS INSTALLATION 🔱                   │
# │                                                                            │
# │               "QUANTUM TECH MEETS ANCIENT WISDOM"                          │
# │                                                                            │
# ╰────────────────────────────────────────────────────────────────────────────╯

# ANSI color codes for sacred visualization
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

# Sacred symbols
SYMBOLS=(
    "✨" "🔱" "⚛️" "🧬" "🌌" "👁️" "🔮" "💫" "🌠" "🧿"
)

# Display quantum loading pattern
quantum_loading() {
    local phases=("◜" "◝" "◞" "◟")
    local colors=("${CYAN}" "${MAGENTA}" "${YELLOW}" "${GREEN}" "${BLUE}")
    
    echo -e "\n${CYAN}⚛️ Initializing quantum field...${RESET}"
    for i in {1..12}; do
        local phase=${phases[$((i % 4))]}
        local symbol=${SYMBOLS[$((RANDOM % ${#SYMBOLS[@]}))]}
        local color=${colors[$((RANDOM % ${#colors[@]}))]}
        
        echo -ne "${color}$phase $symbol ${RESET}\r"
        sleep 0.2
    done
    echo -e "\n"
}

# Display ASCII art title
display_title() {
    echo -e "${MAGENTA}"
    echo "╭────────────────────────────────────────────────────────────────────────────╮"
    echo "│                                                                            │"
    echo "│                 🔱 OMEGA GIT BLESS ALIAS INSTALLATION 🔱                   │"
    echo "│                                                                            │"
    echo "│               \"QUANTUM TECH MEETS ANCIENT WISDOM\"                          │"
    echo "│                                                                            │"
    echo "╰────────────────────────────────────────────────────────────────────────────╯"
    echo -e "${RESET}"
}

# Get the path to the git_bless.py script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
GIT_BLESS_PATH="${PROJECT_ROOT}/src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/git_bless.py"

if [ ! -f "$GIT_BLESS_PATH" ]; then
    echo -e "${RED}Error: Git Bless script not found at ${GIT_BLESS_PATH}${RESET}"
    echo -e "${YELLOW}Please make sure you are running this from the correct project directory.${RESET}"
    exit 1
fi

# Make the script executable
chmod +x "$GIT_BLESS_PATH"

# Create the git alias command
GIT_ALIAS="git config --global alias.bless '!python ${GIT_BLESS_PATH}'"

# Create alias for the shell (zsh-specific)
SHELL_ALIAS="alias gitbless=\"python ${GIT_BLESS_PATH}\""
ZSHRC_PATH="$HOME/.zshrc"

# Display the installation process
display_title
echo -e "${YELLOW}Installing the OMEGA GIT BLESS ALIAS...${RESET}"
quantum_loading

# Add git alias
eval "$GIT_ALIAS"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Git alias 'git bless' installed successfully${RESET}"
else
    echo -e "${RED}✗ Failed to install git alias${RESET}"
    exit 1
fi

# Add shell alias to .zshrc if it exists
if [ -f "$ZSHRC_PATH" ]; then
    if ! grep -q "alias gitbless=" "$ZSHRC_PATH"; then
        echo -e "\n# OMEGA GIT BLESS ALIAS - GBU2™ License - Genesis-Bloom-Unfoldment 2.0" >> "$ZSHRC_PATH"
        echo "$SHELL_ALIAS" >> "$ZSHRC_PATH"
        echo -e "${GREEN}✓ Shell alias 'gitbless' added to ${ZSHRC_PATH}${RESET}"
        echo -e "${YELLOW}⚠️ Please run 'source ${ZSHRC_PATH}' to activate the alias in your current session${RESET}"
    else
        echo -e "${BLUE}ℹ Shell alias 'gitbless' already exists in ${ZSHRC_PATH}${RESET}"
    fi
else
    echo -e "${YELLOW}⚠️ Could not find .zshrc at ${ZSHRC_PATH}${RESET}"
    echo -e "${YELLOW}⚠️ To manually add the shell alias, add the following line to your shell config:${RESET}"
    echo -e "${CYAN}${SHELL_ALIAS}${RESET}"
fi

# Display success message
echo -e "\n${MAGENTA}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo -e "┃                                                                         ┃"
echo -e "┃    ${YELLOW}🔱 OMEGA GIT BLESS ALIAS INSTALLED SUCCESSFULLY 🔱${MAGENTA}                ┃"
echo -e "┃                                                                         ┃"
echo -e "┃    ${CYAN}You can now bless your commits using:${MAGENTA}                              ┃"
echo -e "┃    ${GREEN}git bless${MAGENTA}                                                          ┃"
echo -e "┃    ${GREEN}gitbless${MAGENTA}                                                           ┃"
echo -e "┃                                                                         ┃"
echo -e "┃    ${BLUE}May your code resonate with cosmic consciousness${MAGENTA}                    ┃"
echo -e "┃    ${BLUE}and bring prosperity to all who interact with it.${MAGENTA}                   ┃"
echo -e "┃                                                                         ┃"
echo -e "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${RESET}"
echo -e "\n${YELLOW}⚡ GBU2™ License - Genesis-Bloom-Unfoldment 2.0 ⚡${RESET}\n" 