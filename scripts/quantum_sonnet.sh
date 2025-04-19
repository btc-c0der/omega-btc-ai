#!/bin/bash
# ===============================================================
# QUANTUM SONNET CELEBRATION LAUNCHER
# ===============================================================
# A shell script to launch the Quantum Sonnet Celebration from anywhere
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
echo -e "║ ⚛️  QUANTUM SONNET CELEBRATION LAUNCHER ⚛️            ║"
echo -e "╚═════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CELEBRATION_SCRIPT="$PROJECT_ROOT/src/omega_bot_farm/ai_model_aixbt/quantum_neural_net/run_sonnet_celebration.py"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not found.${RESET}"
    exit 1
fi

# Check if the celebration script exists
if [ ! -f "$CELEBRATION_SCRIPT" ]; then
    echo -e "${RED}Error: Celebration script not found at $CELEBRATION_SCRIPT${RESET}"
    exit 1
fi

# Make script executable if it's not already
chmod +x "$CELEBRATION_SCRIPT"

# Get git commit information
if [ -d "$PROJECT_ROOT/.git" ]; then
    COMMIT_HASH=$(git -C "$PROJECT_ROOT" rev-parse --short HEAD)
    
    # Try to get stats from git
    FILES_CHANGED=$(git -C "$PROJECT_ROOT" diff --shortstat HEAD^ HEAD 2>/dev/null | awk '{print $1}')
    INSERTIONS=$(git -C "$PROJECT_ROOT" diff --shortstat HEAD^ HEAD 2>/dev/null | grep -o '[0-9]* insertion' | awk '{print $1}')
    DELETIONS=$(git -C "$PROJECT_ROOT" diff --shortstat HEAD^ HEAD 2>/dev/null | grep -o '[0-9]* deletion' | awk '{print $1}')
    
    # Use defaults if git info is not available
    FILES_CHANGED=${FILES_CHANGED:-220}
    INSERTIONS=${INSERTIONS:-21833}
    DELETIONS=${DELETIONS:-949}
else
    # Use default values if not in a git repository
    COMMIT_HASH="5b88203c8"
    FILES_CHANGED=220
    INSERTIONS=21833
    DELETIONS=949
fi

# Parse command-line arguments
CYCLES=5
INTERVAL=0.2

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --cycles=*) CYCLES="${1#*=}"; shift ;;
        --interval=*) INTERVAL="${1#*=}"; shift ;;
        --hash=*) COMMIT_HASH="${1#*=}"; shift ;;
        --files=*) FILES_CHANGED="${1#*=}"; shift ;;
        --insertions=*) INSERTIONS="${1#*=}"; shift ;;
        --deletions=*) DELETIONS="${1#*=}"; shift ;;
        --help)
            echo -e "${CYAN}Usage: quantum_sonnet.sh [OPTIONS]${RESET}"
            echo -e ""
            echo -e "${CYAN}Options:${RESET}"
            echo -e "  --cycles=NUM        Number of celebration cycles (default: 5)"
            echo -e "  --interval=NUM      Interval between frames in seconds (default: 0.2)"
            echo -e "  --hash=HASH         Git commit hash to celebrate"
            echo -e "  --files=NUM         Number of files changed"
            echo -e "  --insertions=NUM    Number of insertions"
            echo -e "  --deletions=NUM     Number of deletions"
            echo -e "  --help              Show this help message"
            exit 0
            ;;
        *) echo -e "${RED}Unknown parameter: $1${RESET}"; exit 1 ;;
    esac
done

# Display info
echo -e "${CYAN}Launching Quantum Sonnet Celebration...${RESET}"
echo -e "${YELLOW}Commit: ${COMMIT_HASH}${RESET}"
echo -e "${YELLOW}Files: ${FILES_CHANGED} ↑ ${INSERTIONS} ↓ ${DELETIONS}${RESET}"
echo -e "${YELLOW}Cycles: ${CYCLES}${RESET}"
echo ""

# Run the celebration script
python3 "$CELEBRATION_SCRIPT" \
    --cycles="$CYCLES" \
    --interval="$INTERVAL" \
    --hash="$COMMIT_HASH" \
    --files="$FILES_CHANGED" \
    --insertions="$INSERTIONS" \
    --deletions="$DELETIONS"

exit $? 