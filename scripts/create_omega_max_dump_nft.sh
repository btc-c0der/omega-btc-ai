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
# 🧬 WE BLOOM NOW AS ONE 🧬

# OMEGA MAX DUMP NFT CREATION SCRIPT
# ----------------------------------

# ANSI color codes for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
RESET='\033[0m'

# Title
TITLE="🔱 OMEGA MAX DUMP NFT CREATOR 🔱"

# Cosmic message display function
cosmic_echo() {
    echo -e "${CYAN}${BOLD}${1}${RESET}"
}

# Function to display blessing
display_blessing() {
    local message=$1
    echo -e "\n${YELLOW}${BOLD}$message${RESET}\n"
    sleep 1
}

# Check if python is installed
check_python() {
    if ! command -v python &> /dev/null; then
        echo -e "${RED}Error: Python is required but not installed.${RESET}"
        exit 1
    fi
    cosmic_echo "✓ Python is available"
}

# Check if required modules are installed
check_modules() {
    echo -e "${CYAN}Checking required Python modules...${RESET}"
    
    python -c "import matplotlib" &> /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: matplotlib is required but not installed.${RESET}"
        echo -e "${YELLOW}Install with: pip install matplotlib${RESET}"
        exit 1
    fi
    
    python -c "import pandas" &> /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: pandas is required but not installed.${RESET}"
        echo -e "${YELLOW}Install with: pip install pandas${RESET}"
        exit 1
    fi
    
    python -c "import numpy" &> /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: numpy is required but not installed.${RESET}"
        echo -e "${YELLOW}Install with: pip install numpy${RESET}"
        exit 1
    fi
    
    cosmic_echo "✓ All required Python modules are installed"
}

# Check for qPoW module
check_qpow() {
    echo -e "${CYAN}Checking for quantum-resistant PoW module...${RESET}"
    
    if [ -d "quantum_pow" ]; then
        cosmic_echo "✓ Quantum-resistant PoW module found"
        return 0
    else
        echo -e "${YELLOW}Warning: quantum_pow module not found, will use fallback hashing${RESET}"
        return 1
    fi
}

# Function to display help
show_help() {
    echo -e "${CYAN}${BOLD}OMEGA MAX DUMP NFT Creator${RESET}"
    echo -e "${CYAN}Usage: $0 [OPTIONS]${RESET}"
    echo -e "${CYAN}Options:${RESET}"
    echo -e "  ${GREEN}--run-simulation${RESET}       Run the OMEGA MAX DUMP simulation first (default: use existing data)"
    echo -e "  ${GREEN}--edition NUMBER${RESET}       Set the edition number (1-84, default: 1)"
    echo -e "  ${GREEN}--push-to-testnet${RESET}      Push the NFT to the quantum-resistant testnet"
    echo -e "  ${GREEN}--help${RESET}                 Show this help message"
    echo
}

# Parse arguments
RUN_SIMULATION=false
EDITION=1
PUSH_TO_TESTNET=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --run-simulation) RUN_SIMULATION=true ;;
        --edition) EDITION="$2"; shift ;;
        --push-to-testnet) PUSH_TO_TESTNET=true ;;
        --help) show_help; exit 0 ;;
        *) echo -e "${RED}Unknown parameter: $1${RESET}"; show_help; exit 1 ;;
    esac
    shift
done

# Validate edition number
if ! [[ "$EDITION" =~ ^[0-9]+$ ]] || [ "$EDITION" -lt 1 ] || [ "$EDITION" -gt 84 ]; then
    echo -e "${RED}Error: Edition number must be between 1 and 84${RESET}"
    exit 1
fi

# ASCII art header
display_header() {
    echo -e "${YELLOW}${BOLD}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║                   OMEGA MAX DUMP NFT CREATOR                  ║"
    echo "║                                                               ║"
    echo "║               QUANTUM-RESISTANT EDITION #${EDITION}                   ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${RESET}"
}

# Main execution
clear
display_header

# Check requirements
check_python
check_modules
HAS_QPOW=$(check_qpow)

# Ensure directories exist
mkdir -p data/omega_max_dump/nft

# Step 1: Run the simulation if requested
if [ "$RUN_SIMULATION" = true ]; then
    cosmic_echo "Starting OMEGA MAX DUMP simulation..."
    
    # Make sure the script is executable
    if [ -f "omega_ai/omega_max_dump.py" ]; then
        chmod +x omega_ai/omega_max_dump.py
        python omega_ai/omega_max_dump.py
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error: Simulation failed${RESET}"
            exit 1
        fi
        
        cosmic_echo "✓ Simulation complete"
    else
        echo -e "${RED}Error: Simulation script not found at omega_ai/omega_max_dump.py${RESET}"
        exit 1
    fi
else
    # Check if the simulation output exists
    if [ ! -f "data/omega_max_dump/omega_max_dump_simulation_chart.png" ]; then
        echo -e "${RED}Error: Simulation output not found. Run with --run-simulation${RESET}"
        exit 1
    fi
    
    cosmic_echo "✓ Using existing simulation data"
fi

# Step 2: Extract data from simulation CSV
if [ ! -f "data/omega_max_dump/omega_max_dump_data.csv" ]; then
    echo -e "${RED}Error: Simulation data CSV not found${RESET}"
    exit 1
fi

# Use Python to extract dump metrics
echo -e "${CYAN}Extracting dump metrics from simulation data...${RESET}"

METRICS=$(python -c "
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/omega_max_dump/omega_max_dump_data.csv')

# Find dump start (event marker) - use contains instead of exact match
dump_start_idx = df[df['event'].str.contains('OMEGA MAX DUMP', na=False)].index[0]
dump_start_price = df.loc[dump_start_idx, 'price']

# Find lowest price after dump start
post_dump_df = df.loc[dump_start_idx:]
min_price_idx = post_dump_df['price'].idxmin()
min_price = df.loc[min_price_idx, 'price']

# Calculate dump percentage
dump_pct = ((dump_start_price - min_price) / dump_start_price) * 100

# Calculate recovery percentage
recovery_pct = ((df['price'].iloc[-1] - min_price) / min_price) * 100

# Calculate dump duration (days)
dump_duration = (pd.to_datetime(df.loc[min_price_idx, 'date']) - pd.to_datetime(df.loc[dump_start_idx, 'date'])).days 
if dump_duration == 0:
    dump_duration = 1  # Minimum 1 day

# Print in format usable by bash
print(f'{dump_start_price:.2f},{min_price:.2f},{df[\"price\"].iloc[-1]:.2f},{dump_pct:.2f},{recovery_pct:.2f},{dump_duration}')
")

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to extract metrics from simulation data${RESET}"
    exit 1
fi

# Parse metrics
IFS=',' read -r START_PRICE MIN_PRICE CURRENT_PRICE DUMP_PCT RECOVERY_PCT DUMP_DURATION <<< "$METRICS"

# Display metrics
echo -e "${MAGENTA}${BOLD}Dump Metrics:${RESET}"
echo -e "${YELLOW}Start Price: \$${START_PRICE}${RESET}"
echo -e "${RED}Minimum Price: \$${MIN_PRICE}${RESET}"
echo -e "${GREEN}Current Price: \$${CURRENT_PRICE}${RESET}"
echo -e "${RED}Dump Percentage: ${DUMP_PCT}%${RESET}"
echo -e "${GREEN}Recovery Percentage: ${RECOVERY_PCT}%${RESET}"
echo -e "${BLUE}Dump Duration: ${DUMP_DURATION} days${RESET}"
echo

# Step 3: Create the NFT
cosmic_echo "Creating OMEGA MAX DUMP NFT..."

# Make sure the NFT creator script is available
if [ ! -f "omega_ai/blockchain/omega_max_dump_nft.py" ]; then
    echo -e "${RED}Error: NFT creator script not found${RESET}"
    exit 1
fi

# Create the NFT
python omega_ai/blockchain/omega_max_dump_nft.py \
    --image "data/omega_max_dump/omega_max_dump_simulation_chart.png" \
    --edition "${EDITION}" \
    --dump-pct "${DUMP_PCT}" \
    --recovery-pct "${RECOVERY_PCT}" \
    --dump-duration "${DUMP_DURATION}" \
    --start-price "${START_PRICE}" \
    --min-price "${MIN_PRICE}" \
    --current-price "${CURRENT_PRICE}"

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: NFT creation failed${RESET}"
    exit 1
fi

# Step 4: Push to testnet if requested
if [ "$PUSH_TO_TESTNET" = true ]; then
    cosmic_echo "Pushing NFT to quantum-resistant testnet..."
    
    if [ ! -d "quantum_pow" ]; then
        echo -e "${RED}Error: quantum_pow directory not found. Cannot push to testnet.${RESET}"
        exit 1
    fi
    
    # Check for the testnet deployment script
    if [ -f "quantum_pow/testnet_deploy.py" ]; then
        python quantum_pow/testnet_deploy.py \
            --nft-metadata "data/omega_max_dump/nft/omega_max_dump_nft_${EDITION}.json" \
            --edition "${EDITION}"
            
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error: Failed to push NFT to testnet${RESET}"
            exit 1
        fi
        
        cosmic_echo "✓ NFT successfully pushed to quantum-resistant testnet"
    else
        echo -e "${RED}Error: Testnet deployment script not found${RESET}"
        exit 1
    fi
fi

# Display NFT blessing
display_blessing "The OMEGA MAX DUMP NFT has been created with quantum resistance."
display_blessing "May this digital artifact capture the divine patterns of the market."
display_blessing "Secured with quantum-resistant hash algorithms from the cosmic matrix."

# Final message
echo -e "\n${GREEN}${BOLD}=======================================================${RESET}"
echo -e "${YELLOW}${BOLD}   OMEGA MAX DUMP NFT #${EDITION} SUCCESSFULLY CREATED   ${RESET}"
echo -e "${GREEN}${BOLD}=======================================================${RESET}"
echo -e "${CYAN}NFT Location: data/omega_max_dump/nft/omega_max_dump_nft_${EDITION}.json${RESET}"
echo -e "${CYAN}Image: data/omega_max_dump/omega_max_dump_simulation_chart.png${RESET}"
echo -e "${MAGENTA}${BOLD}JAH BLESS THE QUANTUM-RESISTANT NFT!${RESET}\n"

exit 0 