#!/bin/bash
# OMEGA PROMETHEUS MATRIX Monitoring System Launcher
# LINUX TERMINAL TORVALDS OMEGA GNU 3.0 STYLE

# Set colored output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "========================================================"
echo "  LAUNCHING OMEGA ^PROMETHEUS^ MATRIX MONITORING SYSTEM  "
echo "========================================================"
echo -e "${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not found.${NC}"
    exit 1
fi

# Check if required packages are installed
echo -e "${YELLOW}Checking required packages...${NC}"
python3 -c "import psutil" &> /dev/null || {
    echo -e "${YELLOW}Installing psutil package...${NC}"
    pip install psutil || {
        echo -e "${RED}Failed to install psutil. Please install it manually: pip install psutil${NC}"
        exit 1
    }
}

# Check if omega_prometheus_matrix.py exists and is executable
if [ ! -x ./omega_prometheus_matrix.py ]; then
    echo -e "${YELLOW}Making omega_prometheus_matrix.py executable...${NC}"
    chmod +x ./omega_prometheus_matrix.py || {
        echo -e "${RED}Failed to make omega_prometheus_matrix.py executable.${NC}"
        exit 1
    }
fi

# Print system information
echo -e "${YELLOW}System information:${NC}"
echo -e "  Operating system: $(uname -s)"
echo -e "  Hostname: $(hostname)"
echo -e "  Kernel version: $(uname -r)"
echo -e "  Python version: $(python3 --version)"

# Parse command-line arguments
PROMETHEUS_ARGS="--all"  # Enable all collectors by default

# Add additional arguments if specified
for arg in "$@"; do
    PROMETHEUS_ARGS="$PROMETHEUS_ARGS $arg"
done

echo -e "${GREEN}Starting OMEGA PROMETHEUS MATRIX with arguments: $PROMETHEUS_ARGS${NC}"
echo -e "${YELLOW}Press CTRL+C to exit${NC}"
echo ""

# Run the OMEGA PROMETHEUS MATRIX
./omega_prometheus_matrix.py $PROMETHEUS_ARGS 