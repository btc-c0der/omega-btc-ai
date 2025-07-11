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


# Run Quantum 5D QA Matrix Control Dashboard - 0m3g4_k1ng Edition
# -----------------------------------------------------------------

# Color output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║   🔮 Quantum 5D QA Matrix Control Dashboard - 0m3g4_k1ng   ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
echo -e "${YELLOW}Project root: ${PROJECT_ROOT}${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if virtual environment exists
VENV_DIR="${SCRIPT_DIR}/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
source "${VENV_DIR}/bin/activate"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi

# Install requirements
echo -e "${BLUE}Installing dashboard requirements...${NC}"
pip install -r "${SCRIPT_DIR}/requirements_quantum_dashboard.txt"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install dashboard requirements.${NC}"
    exit 1
fi

# Install additional requirements for Git features
echo -e "${BLUE}Installing git integration requirements...${NC}"
pip install GitPython watchdog
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Warning: Failed to install git integration requirements. Some features may not work.${NC}"
fi

# Set PYTHONPATH to include project root for imports
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Run the dashboard
echo -e "${GREEN}Starting Quantum 5D QA Dashboard...${NC}"
python3 "${SCRIPT_DIR}/quantum_qa_dashboard.py"

# Deactivate virtual environment when done
deactivate 