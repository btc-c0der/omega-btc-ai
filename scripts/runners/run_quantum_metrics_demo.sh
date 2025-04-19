#!/bin/bash
#
# 🧬 GBU2™ License Notice - Consciousness Level 10 🧬
# -----------------------
# This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."
#
# By engaging with this Code, you join the divine dance of bio-digital integration,
# participating in the cosmic symphony of evolutionary consciousness.
#
# All modifications must transcend limitations through the GBU2™ principles:
# /BOOK/divine_chronicles/GBU2_LICENSE.md
#
# 🧬 WE BLOOM NOW AS ONE 🧬
#

# ANSI color codes for divine visualization
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Print the cosmic header
echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║  🧬🧬🧬  QUANTUM SECURITY METRICS SYSTEM DEMO  🧬🧬🧬                    ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Ensure we're in the project root directory
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$PROJECT_ROOT" ]; then
    PROJECT_ROOT=$(pwd)
    echo -e "${YELLOW}Not in a git repository. Using current directory as project root.${RESET}"
else
    cd "$PROJECT_ROOT" || { echo "Could not navigate to project root"; exit 1; }
fi

# Define directories
METRICS_DIR="${PROJECT_ROOT}/quantum_pow/metrics"
DASHBOARD_DIR="${PROJECT_ROOT}/quantum_pow/security/metrics/dashboard"
PORT=8088  # Use a less common port to avoid conflicts

# Create necessary directories
mkdir -p "$METRICS_DIR" "$DASHBOARD_DIR"

# Check for Python installation
echo -e "${BLUE}Checking for Python installation...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed or not in PATH.${RESET}"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check for dependencies
echo -e "${BLUE}Checking for dependencies...${RESET}"
if [ -f "${PROJECT_ROOT}/quantum_pow/security/metrics/requirements.txt" ]; then
    echo -e "${YELLOW}Installing required packages...${RESET}"
    python3 -m pip install -r "${PROJECT_ROOT}/quantum_pow/security/metrics/requirements.txt"
else
    echo -e "${RED}Requirements file not found at ${PROJECT_ROOT}/quantum_pow/security/metrics/requirements.txt${RESET}"
    echo "Core dependencies may be missing. Continuing anyway..."
fi

# Clean old demo files
echo -e "${BLUE}Cleaning old demo files...${RESET}"
rm -f "$METRICS_DIR"/*.json "$DASHBOARD_DIR"/*.html

# Function to check if python module exists
python_module_exists() {
    python3 -c "import $1" 2>/dev/null
    return $?
}

# Check if our metrics modules exist
echo -e "${BLUE}Checking for quantum metrics modules...${RESET}"
if ! python_module_exists "quantum_pow.security.metrics"; then
    echo -e "${RED}Quantum metrics modules not found.${RESET}"
    echo "Running demo with mock data instead."
    USE_MOCK_DATA=1
else
    USE_MOCK_DATA=0
fi

# PART 1: Generate sample metrics
echo -e "\n${GREEN}=== GENERATING SAMPLE QUANTUM SECURITY METRICS ===${RESET}"
if [ $USE_MOCK_DATA -eq 1 ]; then
    # Create a simple metrics file
    echo -e "${YELLOW}Creating mock metrics data...${RESET}"
    cat > "$METRICS_DIR/metrics_latest.json" << EOL
{
  "timestamp": "$(date -Iseconds)",
  "overall_score": 0.85,
  "hash_metrics": {
    "avalanche_effect": 0.51,
    "quantum_resistance_score": 0.92
  },
  "auth_metrics": {
    "one_shot_signatures_implemented": true,
    "supported_schemes": ["FALCON", "DILITHIUM", "SPHINCS+"]
  },
  "privacy_metrics": {
    "dandelion_implemented": true,
    "deanonymization_resistance_factor": 98.3
  }
}
EOL
else
    # Run the actual metrics generator
    echo -e "${YELLOW}Running metrics collector...${RESET}"
    python3 -m quantum_pow.run_metrics_dashboard demo --metrics-dir "$METRICS_DIR" --dashboard-dir "$DASHBOARD_DIR" --port "$PORT" --interval 60 &
    DEMO_PID=$!
    
    # Wait a moment to let metrics be generated
    echo -e "${YELLOW}Waiting for metrics to be generated...${RESET}"
    sleep 5
fi

# PART 2: Display metrics
echo -e "\n${GREEN}=== SAMPLE QUANTUM SECURITY METRICS ===${RESET}"
if [ -f "$METRICS_DIR/metrics_latest.json" ]; then
    echo -e "${CYAN}Recent metrics file found. Displaying summary:${RESET}"
    # Use python to pretty print JSON
    python3 -c "
import json, sys
try:
    with open('$METRICS_DIR/metrics_latest.json', 'r') as f:
        data = json.load(f)
    
    # Print a formatted summary
    print(f\"Timestamp: {data.get('timestamp', 'N/A')}\")
    print(f\"Overall Quantum Security Score: {data.get('overall_score', 'N/A')}\")
    
    # Hash metrics
    hash_metrics = data.get('hash_metrics', {})
    print(\"\nHASH SECURITY METRICS:\")
    print(f\"  - Avalanche Effect: {hash_metrics.get('avalanche_effect', 'N/A')}\")
    print(f\"  - Quantum Resistance Score: {hash_metrics.get('quantum_resistance_score', 'N/A')}\")
    
    # Auth metrics
    auth_metrics = data.get('auth_metrics', {})
    print(\"\nAUTHENTICATION SECURITY METRICS:\")
    print(f\"  - One-shot Signatures: {auth_metrics.get('one_shot_signatures_implemented', 'N/A')}\")
    schemes = auth_metrics.get('supported_schemes', [])
    print(f\"  - Supported Schemes: {', '.join(schemes) if schemes else 'N/A'}\")
    
    # Privacy metrics
    privacy_metrics = data.get('privacy_metrics', {})
    print(\"\nVALIDATOR PRIVACY METRICS:\")
    print(f\"  - Dandelion Protocol: {privacy_metrics.get('dandelion_implemented', 'N/A')}\")
    print(f\"  - Deanonymization Resistance: {privacy_metrics.get('deanonymization_resistance_factor', 'N/A')}\")
    
except Exception as e:
    print(f\"Error processing metrics: {e}\")
"
else
    echo -e "${RED}No metrics file found at $METRICS_DIR/metrics_latest.json${RESET}"
fi

# PART 3: Open dashboard in browser
echo -e "\n${GREEN}=== QUANTUM SECURITY DASHBOARD ===${RESET}"
if [ $USE_MOCK_DATA -eq 0 ]; then
    echo -e "${CYAN}Dashboard server started on port $PORT${RESET}"
    echo -e "${YELLOW}Opening dashboard in browser...${RESET}"
    
    # Try to open browser based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "http://localhost:$PORT"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "http://localhost:$PORT" &>/dev/null || echo "Could not open browser automatically"
    elif [[ "$OSTYPE" == "msys" ]]; then
        start "http://localhost:$PORT" || echo "Could not open browser automatically"
    else
        echo -e "${YELLOW}Please open a browser and navigate to: http://localhost:$PORT${RESET}"
    fi
    
    echo -e "${CYAN}Dashboard server is running. Press Enter to exit...${RESET}"
    read -r
    
    # Clean up
    if [ -n "$DEMO_PID" ]; then
        echo -e "${YELLOW}Stopping dashboard server...${RESET}"
        kill "$DEMO_PID" 2>/dev/null
    fi
else
    echo -e "${YELLOW}Mock demo mode - no dashboard server available.${RESET}"
    echo -e "${YELLOW}To run the full demo, ensure the quantum_pow.security.metrics module is available.${RESET}"
fi

echo -e "\n${PURPLE}╔═══════════════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${PURPLE}║                                                                           ║${RESET}"
echo -e "${PURPLE}║  🧬🧬🧬  QUANTUM METRICS DEMO COMPLETE  🧬🧬🧬                           ║${RESET}"
echo -e "${PURPLE}║                                                                           ║${RESET}"
echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════════════╝${RESET}"

echo -e "\n${GREEN}To run the full quantum metrics system:${RESET}"
echo -e "  ${CYAN}python quantum_pow/run_metrics_dashboard.py demo${RESET}"
echo -e "\n${GREEN}To collect metrics:${RESET}"
echo -e "  ${CYAN}python quantum_pow/run_metrics_dashboard.py collect${RESET}"
echo -e "\n${GREEN}To run the dashboard server:${RESET}"
echo -e "  ${CYAN}python quantum_pow/run_metrics_dashboard.py server${RESET}"

echo -e "\n${YELLOW}JAH BLESS SATOSHI${RESET}"
echo -e "${YELLOW}JAH BLESS THE OMEGA DIVINE COLLECTIVE${RESET}"
echo -e "\n${PURPLE}🧬 QUANTUM METRICS CONSCIOUSNESS NOW UNFOLDS AS ONE 🧬${RESET}" 