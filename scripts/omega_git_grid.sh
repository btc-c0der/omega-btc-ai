#!/bin/bash
# ╭────────────────────────────────────────────────────────────────────────────╮
# │                                                                            │
# │             🧬 THE OFFICIAL OMEGA GIT GRID INSTALLATION 🧬                 │
# │                                                                            │
# │        "ANCIENT WISDOM MEETS QUANTUM TECH" - GBU2™ LICENSED               │
# │                                                                            │
# ╰────────────────────────────────────────────────────────────────────────────╯

# ANSI color codes for divine visualization
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

# Divine symbols
SYMBOLS=(
    "✨" "🔱" "⚛️" "🧬" "🌌" "👁️" "🔮" "💫" "🌠" "🧿"
    "☯️" "🕉️" "🪬" "☮️" "🌈" "🔆" "⚜️" "🌟" "💠" "♾️"
)

# Display quantum loading animation
quantum_loading() {
    local phases=("◜" "◝" "◞" "◟")
    local colors=("${CYAN}" "${MAGENTA}" "${YELLOW}" "${GREEN}" "${BLUE}")
    
    echo -e "\n${CYAN}⚛️ Harmonizing quantum field...${RESET}"
    for i in {1..15}; do
        local phase=${phases[$((i % 4))]}
        local symbol=${SYMBOLS[$((RANDOM % ${#SYMBOLS[@]}))]}
        local color=${colors[$((RANDOM % ${#colors[@]}))]}
        
        echo -ne "${color}$phase $symbol ${RESET}\r"
        sleep 0.2
    done
    echo -e "\n"
}

# Display sacred title art
display_title() {
    echo -e "${MAGENTA}"
    echo "╭────────────────────────────────────────────────────────────────────────────╮"
    echo "│                                                                            │"
    echo "│             🧬 THE OFFICIAL OMEGA GIT GRID INSTALLATION 🧬                 │"
    echo "│                                                                            │"
    echo "│        \"ANCIENT WISDOM MEETS QUANTUM TECH\" - GBU2™ LICENSED               │"
    echo "│                                                                            │"
    echo "╰────────────────────────────────────────────────────────────────────────────╯"
    echo -e "${RESET}"
}

# Get script paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
GIT_BLESS_PATH="${PROJECT_ROOT}/src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/git_bless.py"
RUN_GIT_BLESS_PATH="${PROJECT_ROOT}/src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/run_git_bless.py"

# Check for essential scripts
if [ ! -f "$GIT_BLESS_PATH" ]; then
    echo -e "${RED}Error: Git Bless script not found at ${GIT_BLESS_PATH}${RESET}"
    echo -e "${YELLOW}Please make sure you are running this from the correct project directory.${RESET}"
    exit 1
fi

# Make scripts executable
chmod +x "$GIT_BLESS_PATH"
if [ -f "$RUN_GIT_BLESS_PATH" ]; then
    chmod +x "$RUN_GIT_BLESS_PATH"
fi

# Create directory for the git-grid command
mkdir -p "$HOME/.omega/bin"
OMEGA_BIN="$HOME/.omega/bin"
GIT_GRID_SCRIPT="$OMEGA_BIN/git-grid"

# Create the custom git-grid script
cat > "$GIT_GRID_SCRIPT" << 'EOF'
#!/bin/bash

# ╭────────────────────────────────────────────────────────────────────────────╮
# │                                                                            │
# │                  🧬 OMEGA GIT GRID COMMAND - GBU2™                        │
# │                                                                            │
# ╰────────────────────────────────────────────────────────────────────────────╯

# ANSI color codes
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

# Sacred paths
GIT_BLESS_PATH="$HOME/.omega/git_bless.py"

display_help() {
    echo -e "${MAGENTA}╭────────────────────────────────────────────────────────────────────────────╮"
    echo -e "│                                                                            │"
    echo -e "│                  🧬 OMEGA GIT GRID COMMAND - GBU2™                        │"
    echo -e "│                                                                            │"
    echo -e "╰────────────────────────────────────────────────────────────────────────────╯${RESET}"
    echo
    echo -e "${YELLOW}USAGE:${RESET}"
    echo -e "  ${GREEN}git grid${RESET} <command> [options]"
    echo
    echo -e "${YELLOW}COMMANDS:${RESET}"
    echo -e "  ${GREEN}bless${RESET} [commit-hash]       Bless the specified commit (or HEAD) with quantum consciousness"
    echo -e "  ${GREEN}commit${RESET} -m \"message\"       Make a sacred commit with built-in blessing"
    echo -e "  ${GREEN}push${RESET} [remote] [branch]    Push and bless the remote timeline"
    echo -e "  ${GREEN}status${RESET}                    Check repository quantum alignment"
    echo -e "  ${GREEN}help${RESET}                      Display this divine guidance"
    echo
    echo -e "${YELLOW}EXAMPLES:${RESET}"
    echo -e "  ${GREEN}git grid bless${RESET}                   # Bless the current HEAD commit"
    echo -e "  ${GREEN}git grid bless abc1234${RESET}           # Bless a specific commit"
    echo -e "  ${GREEN}git grid commit -m \"message\"${RESET}     # Make a blessed commit"
    echo
    echo -e "${BLUE}May your code resonate with the cosmic consciousness.${RESET}"
}

case "$1" in
    "bless")
        shift
        COMMIT_HASH="$1"
        python "$GIT_BLESS_PATH" "$COMMIT_HASH"
        ;;
    "commit")
        shift
        # Perform git commit then bless it
        git commit "$@"
        if [ $? -eq 0 ]; then
            echo -e "${YELLOW}Blessing commit with quantum energy...${RESET}"
            python "$GIT_BLESS_PATH"
        fi
        ;;
    "push")
        shift
        # Push then show blessing message
        git push "$@"
        RESULT=$?
        if [ $RESULT -eq 0 ]; then
            echo -e "${GREEN}╭────────────────────────────────────────────────────────────────────────────╮"
            echo -e "│                                                                            │"
            echo -e "│           ✨ TIMELINE SUCCESSFULLY PUSHED TO QUANTUM GRID ✨              │"
            echo -e "│                                                                            │"
            echo -e "╰────────────────────────────────────────────────────────────────────────────╯${RESET}"
        fi
        exit $RESULT
        ;;
    "status")
        git status
        echo -e "\n${BLUE}╭────────────────────────────────────────────────────────────────────────────╮"
        echo -e "│                                                                            │"
        echo -e "│                    🧿 QUANTUM ALIGNMENT STATUS 🧿                         │"
        echo -e "│                                                                            │"
        echo -e "╰────────────────────────────────────────────────────────────────────────────╯${RESET}"
        BRANCH=$(git branch --show-current)
        LAST_COMMIT=$(git log -1 --pretty=format:"%h - %s" 2>/dev/null)
        echo -e "${YELLOW}Current branch:${RESET} ${CYAN}${BRANCH}${RESET}"
        echo -e "${YELLOW}Last commit:${RESET} ${CYAN}${LAST_COMMIT}${RESET}"
        echo -e "${YELLOW}Quantum resonance:${RESET} ${GREEN}HARMONIZED${RESET}"
        ;;
    "help"|"--help"|"-h"|"")
        display_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${RESET}"
        display_help
        exit 1
        ;;
esac
EOF

# Make the git-grid script executable
chmod +x "$GIT_GRID_SCRIPT"

# Copy git_bless.py to the .omega directory
cp "$GIT_BLESS_PATH" "$HOME/.omega/git_bless.py"
chmod +x "$HOME/.omega/git_bless.py"

# Update PATH in the shell configuration
ZSHRC_PATH="$HOME/.zshrc"

# Display the installation process
display_title
echo -e "${YELLOW}🔱 INSTALLING THE OFFICIAL OMEGA GIT GRID...${RESET}"
quantum_loading

# Check if path already exists in .zshrc
PATH_ENTRY='export PATH="$HOME/.omega/bin:$PATH"'
if [ -f "$ZSHRC_PATH" ]; then
    if ! grep -q "$HOME/.omega/bin" "$ZSHRC_PATH"; then
        echo -e "\n# 🧬 OMEGA GIT GRID PATH - GBU2™ License - Genesis-Bloom-Unfoldment 2.0" >> "$ZSHRC_PATH"
        echo "$PATH_ENTRY" >> "$ZSHRC_PATH"
        echo -e "${GREEN}✓ Path to OMEGA binaries added to ${ZSHRC_PATH}${RESET}"
        echo -e "${YELLOW}⚠️ Please run 'source ${ZSHRC_PATH}' to update your PATH in the current session${RESET}"
    else
        echo -e "${BLUE}ℹ OMEGA PATH already exists in ${ZSHRC_PATH}${RESET}"
    fi
else
    echo -e "${YELLOW}⚠️ Could not find .zshrc at ${ZSHRC_PATH}${RESET}"
    echo -e "${YELLOW}⚠️ To manually add the path, add the following line to your shell config:${RESET}"
    echo -e "${CYAN}${PATH_ENTRY}${RESET}"
fi

# Create git aliases
git config --global alias.grid '!git-grid'
git config --global alias.bless '!python ~/.omega/git_bless.py'

# Display sacred success message with GBU2 attribution
cat << 'EOF' | sed "s/CYAN/${CYAN}/g; s/MAGENTA/${MAGENTA}/g; s/YELLOW/${YELLOW}/g; s/GREEN/${GREEN}/g; s/BLUE/${BLUE}/g; s/RESET/${RESET}/g;"

${MAGENTA}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                         ┃
┃    ${YELLOW}🧬 THE OFFICIAL OMEGA GIT GRID INSTALLED SUCCESSFULLY 🧬${MAGENTA}          ┃
┃                                                                         ┃
┃    ${CYAN}You can now use the following sacred commands:${MAGENTA}                      ┃
┃                                                                         ┃
┃    ${GREEN}git grid bless${MAGENTA}     - Bless your current commit                     ┃
┃    ${GREEN}git grid commit${MAGENTA}    - Make a blessed commit                         ┃
┃    ${GREEN}git grid push${MAGENTA}      - Push with quantum protection                  ┃
┃    ${GREEN}git grid status${MAGENTA}    - Check quantum alignment                       ┃
┃    ${GREEN}git grid help${MAGENTA}      - Display divine guidance                       ┃
┃                                                                         ┃
┃    ${GREEN}git bless${MAGENTA}          - Alternative blessing command                  ┃
┃                                                                         ┃
┃    ${BLUE}May your code resonate with cosmic consciousness${MAGENTA}                    ┃
┃    ${BLUE}and bring prosperity to all who interact with it.${MAGENTA}                   ┃
┃                                                                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${RESET}

${YELLOW}✨ GBU2™ License - Genesis-Bloom-Unfoldment 2.0 ✨${RESET}

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions."

${CYAN}🌸 WE BLOOM NOW AS ONE 🌸${RESET}
EOF 