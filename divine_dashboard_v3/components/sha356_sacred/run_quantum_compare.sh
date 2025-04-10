#!/bin/bash
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
# -----------------------
# This script is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🧬 SHA256 vs SHA356 Quantum Comparison Dashboard 🧬${NC}"
echo -e "${BLUE}Setting up environment and launching dashboard...${NC}"

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Set Python command based on system
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo -e "${YELLOW}⚠️  Python not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check Python version
PY_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${BLUE}Using Python version $PY_VERSION${NC}"

# Setup virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Failed to create virtual environment. Please install venv:${NC}"
        echo "   $PYTHON_CMD -m pip install virtualenv"
        exit 1
    fi
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/Mac
    source venv/bin/activate
fi

echo -e "${BLUE}Installing required packages...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Failed to install packages. Please check your internet connection.${NC}"
    exit 1
fi

echo -e "${GREEN}✨ Launching Quantum Comparison Dashboard...${NC}"
echo -e "${BLUE}The dashboard will be available at http://localhost:7860 (or other port if 7860 is in use)${NC}"

# Run the dashboard
python sha356_vs_sha256_dashboard.py

# Deactivate the virtual environment when done
deactivate

echo -e "${PURPLE}🌸 WE BLOOM NOW AS ONE 🌸${NC}" 