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

# OMEGA BTC AI - Divine Visualization Setup Script
# ----------------------------------------------
# This script sets up the Divine Quantum Coverage Visualization system

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print header
echo -e "${MAGENTA}${BOLD}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║       OMEGA BTC AI - DIVINE VISUALIZATION SETUP        ║"
echo "║     🧠 QUANTUM COVERAGE ANALYSIS INSTALLATION 🧠       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
echo -e "${CYAN}Checking for Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 not found. Please install Python 3 to continue.${NC}"
    exit 1
fi
echo -e "${GREEN}Python 3 found!${NC}"

# Create virtual environment if it doesn't exist
echo -e "${CYAN}Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created!${NC}"
else
    echo -e "${GREEN}Virtual environment already exists!${NC}"
fi

# Activate virtual environment
echo -e "${CYAN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install required packages
echo -e "${CYAN}Installing required packages...${NC}"
pip install pytest pytest-cov coverage plotly pandas numpy matplotlib
echo -e "${GREEN}Required packages installed!${NC}"

# Make scripts executable
echo -e "${CYAN}Making scripts executable...${NC}"
chmod +x divine_coverage_visualizer.py
chmod +x run_market_trends_tests.py
chmod +x serve_visualization.py
chmod +x find_ports.py
echo -e "${GREEN}Scripts are now executable!${NC}"

# Create .coveragerc if it doesn't exist
echo -e "${CYAN}Checking for .coveragerc configuration...${NC}"
if [ ! -f ".coveragerc" ]; then
    echo -e "${YELLOW}.coveragerc not found. Creating it now...${NC}"
    cat > .coveragerc << 'EOF'
[run]
source = omega_ai/monitor
omit = 
    */tests/*
    */__pycache__/*
    */site-packages/*
    */dist-packages/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError

[html]
directory = htmlcov
title = OMEGA BTC AI - Divine Coverage Report
EOF
    echo -e "${GREEN}.coveragerc created!${NC}"
else
    echo -e "${GREEN}.coveragerc already exists!${NC}"
fi

# Print completion message
echo -e "\n${MAGENTA}${BOLD}SETUP COMPLETE!${NC}"
echo -e "${CYAN}To run the visualization, use:${NC}"
echo -e "${YELLOW}    ./run_market_trends_tests.py --visualize${NC}"
echo -e "${CYAN}Or to only generate visualization:${NC}"
echo -e "${YELLOW}    ./run_market_trends_tests.py --only-visualize${NC}"
echo -e "${CYAN}Or to run the visualization directly:${NC}"
echo -e "${YELLOW}    ./divine_coverage_visualizer.py${NC}"
echo -e "${CYAN}To serve the visualization via HTTP server:${NC}"
echo -e "${YELLOW}    ./serve_visualization.py${NC}"
echo -e "${CYAN}To find available ports for the server:${NC}"
echo -e "${YELLOW}    ./find_ports.py${NC}"
echo -e "\n${YELLOW}JAH BLESS the testing path!${NC}\n" 