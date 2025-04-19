#!/bin/bash

# 🧬 GBU2™ License Notice - Consciousness Level 10 🧬
# -----------------------
# This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."
#
# 🧬 WE BLOOM NOW AS ONE 🧬

# ANSI Color codes for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# S4T0SH1 Local demo paths (using different directories to avoid conflicts)
METRICS_DIR="./quantum_pow/security/metrics/s4t0sh1_data"
DASHBOARD_DIR="./quantum_pow/security/metrics/s4t0sh1_dashboard"
TESTNET_DIR="./quantum_pow/s4t0sh1_testnet_data"

# Make sure directories exist
mkdir -p "$METRICS_DIR" "$DASHBOARD_DIR" "$TESTNET_DIR"

# ASCII Art Banner
display_banner() {
    echo -e "${PURPLE}"
    echo -e "🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬"
    echo -e "🧬                                              🧬"
    echo -e "🧬  S4T0SH1 QUANTUM METRICS - HARMONY DEMO     🧬"
    echo -e "🧬                                              🧬"
    echo -e "🧬  Conflict-Free Integration                   🧬"
    echo -e "🧬                                              🧬"
    echo -e "🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬"
    echo -e "${NC}"
}

# Function to check if Python and required packages are installed
check_dependencies() {
    echo -e "${BLUE}[COSMIC CHECK]${NC} Verifying divine dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}[WARNING]${NC} Python3 is not installed. Please install Python 3.9 or higher."
        exit 1
    fi
    
    # Check required packages using pip list
    required_packages=("flask" "numpy" "matplotlib" "pandas")
    missing_packages=()
    
    for package in "${required_packages[@]}"; do
        if ! python3 -m pip list | grep -i "$package" &> /dev/null; then
            missing_packages+=("$package")
        fi
    done
    
    if [ ${#missing_packages[@]} -gt 0 ]; then
        echo -e "${YELLOW}[WARNING]${NC} Some required packages are missing."
        echo -e "Installing: ${missing_packages[*]}"
        python3 -m pip install "${missing_packages[@]}"
    fi
    
    echo -e "${GREEN}[SUCCESS]${NC} All divine dependencies are present."
}

# Find available port starting from base
find_available_port() {
    local base_port=$1
    local port=$base_port
    while netstat -tna | grep -q ":$port "; do
        port=$((port + 1))
    done
    echo $port
}

# Function to start the testnet in background
start_testnet() {
    echo -e "${BLUE}[COSMIC TESTNET]${NC} Initiating S4T0SH1 quantum-resistant testnet..."
    
    # Get available ports
    TESTNET_PORT=$(find_available_port 9100)
    
    # Run testnet in background with custom config and special env var
    S4T0SH1_MODE=true python3 quantum_pow/testnet.py \
        --nodes 3 \
        --mining-interval 15 \
        --transaction-interval 5 \
        --data-dir "$TESTNET_DIR" \
        --base-port $TESTNET_PORT \
        --metrics-enabled &
    
    TESTNET_PID=$!
    echo -e "${GREEN}[SUCCESS]${NC} S4T0SH1 Testnet initiated with PID: $TESTNET_PID (Base port: $TESTNET_PORT)"
    echo "$TESTNET_PID" > /tmp/s4t0sh1_testnet.pid
    
    # Give testnet time to start
    sleep 5
}

# Function to start metrics collection in background
start_metrics_collector() {
    echo -e "${BLUE}[COSMIC METRICS]${NC} Awakening S4T0SH1 quantum metrics consciousness..."
    
    # Run metrics collector in background
    S4T0SH1_MODE=true python3 quantum_pow/run_metrics_dashboard.py collect \
        --output-dir "$METRICS_DIR" \
        --continuous \
        --interval 10 \
        --tag "s4t0sh1" &
    
    COLLECTOR_PID=$!
    echo -e "${GREEN}[SUCCESS]${NC} S4T0SH1 Metrics collector awakened with PID: $COLLECTOR_PID"
    echo "$COLLECTOR_PID" > /tmp/s4t0sh1_metrics_collector.pid
    
    # Give collector time to generate initial metrics
    sleep 3
}

# Function to start dashboard server
start_dashboard() {
    echo -e "${BLUE}[COSMIC DASHBOARD]${NC} Manifesting S4T0SH1 quantum metrics visualization..."
    
    # Find available port
    DASHBOARD_PORT=$(find_available_port 8089)
    
    # Run dashboard server
    S4T0SH1_MODE=true python3 quantum_pow/run_metrics_dashboard.py server \
        --metrics-path "$METRICS_DIR" \
        --dashboard-path "$DASHBOARD_DIR" \
        --host "127.0.0.1" \
        --port $DASHBOARD_PORT \
        --tag "s4t0sh1" &
    
    DASHBOARD_PID=$!
    echo -e "${GREEN}[SUCCESS]${NC} S4T0SH1 Dashboard server manifested with PID: $DASHBOARD_PID (Port: $DASHBOARD_PORT)"
    echo "$DASHBOARD_PID" > /tmp/s4t0sh1_dashboard.pid
    
    # Open browser after short delay to give server time to start
    sleep 3
    echo -e "${GREEN}[COSMIC CONNECTION]${NC} Opening S4T0SH1 divine dashboard in browser..."
    
    # Detect OS and open browser accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "http://127.0.0.1:$DASHBOARD_PORT"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "http://127.0.0.1:$DASHBOARD_PORT"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        start "http://127.0.0.1:$DASHBOARD_PORT"
    else
        echo -e "${YELLOW}[NOTE]${NC} Please open a browser and navigate to: http://127.0.0.1:$DASHBOARD_PORT"
    fi
}

# Function to print testnet stats
print_stats() {
    echo -e "${BLUE}[COSMIC STATS]${NC} Revealing S4T0SH1 quantum security consciousness..."
    # Get testnet stats if available
    if [ -f "$TESTNET_DIR/stats.json" ]; then
        echo -e "${PURPLE}${BOLD}S4T0SH1 Testnet Divine Statistics:${NC}"
        cat "$TESTNET_DIR/stats.json" | python3 -m json.tool
    else
        echo -e "${YELLOW}[NOTE]${NC} S4T0SH1 Testnet stats not yet available. Consciousness is still forming."
    fi
    
    # Count metrics files
    METRICS_COUNT=$(ls -1 "$METRICS_DIR" 2>/dev/null | wc -l)
    echo -e "${PURPLE}${BOLD}S4T0SH1 Metrics Files:${NC} $METRICS_COUNT consciousness snapshots recorded"
}

# Function to stop all processes
stop_demo() {
    echo -e "${BLUE}[COSMIC CLOSURE]${NC} Gracefully closing S4T0SH1 quantum consciousness portal..."
    
    # Stop processes if PIDs exist
    if [ -f /tmp/s4t0sh1_testnet.pid ]; then
        TESTNET_PID=$(cat /tmp/s4t0sh1_testnet.pid)
        kill -15 $TESTNET_PID 2>/dev/null || true
        rm /tmp/s4t0sh1_testnet.pid
    fi
    
    if [ -f /tmp/s4t0sh1_metrics_collector.pid ]; then
        COLLECTOR_PID=$(cat /tmp/s4t0sh1_metrics_collector.pid)
        kill -15 $COLLECTOR_PID 2>/dev/null || true
        rm /tmp/s4t0sh1_metrics_collector.pid
    fi
    
    if [ -f /tmp/s4t0sh1_dashboard.pid ]; then
        DASHBOARD_PID=$(cat /tmp/s4t0sh1_dashboard.pid)
        kill -15 $DASHBOARD_PID 2>/dev/null || true
        rm /tmp/s4t0sh1_dashboard.pid
    fi
    
    echo -e "${GREEN}[SUCCESS]${NC} All S4T0SH1 quantum processes have been gracefully closed."
    echo -e "${PURPLE}${BOLD}JAH BLESS SATOSHI${NC}"
    echo -e "${PURPLE}${BOLD}JAH BLESS THE OMEGA DIVINE COLLECTIVE${NC}"
}

# Setup trap to clean up on exit
trap stop_demo EXIT

# Main execution
display_banner
check_dependencies
start_testnet
start_metrics_collector
start_dashboard

# Keep script running until user presses Ctrl+C
echo -e "${YELLOW}${BOLD}[S4T0SH1 SYSTEM ONLINE]${NC} Press Ctrl+C to stop the demo..."
DASHBOARD_PORT=$(find_available_port 8089)
echo -e "${BLUE}${BOLD}S4T0SH1 Dashboard URL:${NC} http://127.0.0.1:$DASHBOARD_PORT"
echo -e "${BLUE}${BOLD}S4T0SH1 Data Directory:${NC} $METRICS_DIR"

# Print stats every 30 seconds while running
counter=0
while true; do
    sleep 10
    counter=$((counter + 1))
    if [ $((counter % 3)) -eq 0 ]; then
        print_stats
    fi
done 