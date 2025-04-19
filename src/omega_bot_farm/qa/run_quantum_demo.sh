#!/bin/bash
# Shell script to run the 0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D demo

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

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Get the project root directory (up two levels)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." &> /dev/null && pwd )"

# Define Python executable to use
PYTHON_CMD="python"

# Check if we have a virtual environment
if [ -d "$PROJECT_ROOT/venv" ]; then
    PYTHON_CMD="$PROJECT_ROOT/venv/bin/python"
elif [ -d "$PROJECT_ROOT/.venv" ]; then
    PYTHON_CMD="$PROJECT_ROOT/.venv/bin/python"
fi

# Make sure the quantum_runner directory is in path
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Add colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
RESET='\033[0m'

# Print banner
echo -e "\n${CYAN}╔════════════════════════════════════════════════════════════╗"
echo -e "║                                                            ║"
echo -e "║   🧪 0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D 🧬           ║"
echo -e "║                                                            ║"
echo -e "║   ${BLUE}Quantum Testing Framework Demo Launcher              ${CYAN}    ║"
echo -e "╚════════════════════════════════════════════════════════════╝${RESET}\n"

# Check for arguments
AUTO_RUN=""
if [ "$1" == "--auto-run" ]; then
    AUTO_RUN="--auto-run"
    echo -e "${YELLOW}Running in automated mode (shorter pauses)${RESET}\n"
fi

# Check for Kubernetes client
if python -c "import kubernetes" 2>/dev/null; then
    echo -e "${GREEN}✓ Kubernetes client detected${RESET}"
else
    echo -e "${YELLOW}⚠ Kubernetes client not installed${RESET}"
    echo -e "${YELLOW}For full experience, install with: pip install kubernetes${RESET}\n"
fi

echo -e "${BLUE}Launching the Quantum Test Runner demo...${RESET}\n"

# Run the demo script
"$PYTHON_CMD" "$SCRIPT_DIR/demo_quantum_runner.py" $AUTO_RUN

# Check exit status
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "\n${RED}Demo exited with errors (code $EXIT_CODE)${RESET}"
    exit $EXIT_CODE
fi 