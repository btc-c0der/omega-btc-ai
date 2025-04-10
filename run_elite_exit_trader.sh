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


# OMEGA BTC AI - Elite Exit Trader Launcher
# This script provides specialized configuration for elite exit strategies

# Color constants
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
RESET='\033[0m'

print_usage() {
    echo -e "${PURPLE}OMEGA BTC AI - Elite Exit Trader Launcher${RESET}"
    echo
    echo -e "Usage: ./run_elite_exit_trader.sh [CONFIDENCE] [SYMBOL] [LEVERAGE]"
    echo 
    echo -e "Parameters:"
    echo -e "  ${CYAN}CONFIDENCE${RESET}  - Elite exit confidence threshold (0.5-0.95)"
    echo -e "                    Higher values make exits more selective"
    echo -e "                    Recommended range: 0.6-0.9"
    echo -e "  ${CYAN}SYMBOL${RESET}      - Trading symbol (default: BTCUSDT)"
    echo -e "  ${CYAN}LEVERAGE${RESET}    - Trading leverage (default: 10)"
    echo
    echo -e "Elite exit confidence guide:"
    echo -e "  ${GREEN}0.5-0.6${RESET} - Very aggressive exits, will exit positions quickly"
    echo -e "  ${YELLOW}0.7-0.8${RESET} - Balanced approach, good for normal market conditions"
    echo -e "  ${RED}0.8-0.9${RESET} - Conservative, will only exit on strong signals"
    echo -e "  ${PURPLE}>0.9${RESET}    - Extremely selective, may rarely trigger exits"
    echo
    echo -e "Examples:"
    echo -e "  ./run_elite_exit_trader.sh 0.7        # Balanced exit strategy on BTC"
    echo -e "  ./run_elite_exit_trader.sh 0.8 ETHUSDT # Conservative exit strategy on ETH"
    echo -e "  ./run_elite_exit_trader.sh 0.65 BTCUSDT 15 # More aggressive with higher leverage"
}

if [ "$1" == "--help" ] || [ "$1" == "-h" ] || [ "$1" == "" ]; then
    print_usage
    exit 0
fi

# Set defaults
CONFIDENCE=${1:-0.7}
SYMBOL=${2:-BTCUSDT}
LEVERAGE=${3:-10}

# Validate confidence value
if (( $(echo "$CONFIDENCE < 0.5" | bc -l) )) || (( $(echo "$CONFIDENCE > 0.95" | bc -l) )); then
    echo -e "${RED}Error: Confidence threshold should be between 0.5 and 0.95${RESET}"
    echo
    print_usage
    exit 1
fi

# Set color based on confidence
if (( $(echo "$CONFIDENCE < 0.65" | bc -l) )); then
    CONF_COLOR=$GREEN
elif (( $(echo "$CONFIDENCE < 0.8" | bc -l) )); then
    CONF_COLOR=$YELLOW
elif (( $(echo "$CONFIDENCE < 0.9" | bc -l) )); then
    CONF_COLOR=$RED
else
    CONF_COLOR=$PURPLE
fi

echo -e "${PURPLE}OMEGA BTC AI - Elite Exit Trader${RESET}"
echo -e "${CYAN}Symbol: ${YELLOW}$SYMBOL${RESET}"
echo -e "${CYAN}Elite Exit Confidence: ${CONF_COLOR}$CONFIDENCE${RESET}"
echo -e "${CYAN}Leverage: ${YELLOW}${LEVERAGE}x${RESET}"
echo

# Set capital based on leverage (inverse relationship for safety)
if (( $LEVERAGE <= 5 )); then
    CAPITAL=50
elif (( $LEVERAGE <= 10 )); then
    CAPITAL=40
elif (( $LEVERAGE <= 15 )); then
    CAPITAL=30
else
    CAPITAL=20
fi

# Build command with elite exit enabled
CMD="python run_trap_aware_dual_traders.py --symbol $SYMBOL --enable-elite-exits --elite-exit-confidence $CONFIDENCE \
--long-leverage $LEVERAGE --short-leverage $LEVERAGE --long-capital $CAPITAL --short-capital $CAPITAL \
--trap-probability-threshold 0.7 --min-free-balance 100"

echo -e "${CYAN}Command to execute:${RESET}"
echo -e "$CMD"
echo

# Show the exit strategy explanation
echo -e "${PURPLE}Elite Exit Strategy Information:${RESET}"
if (( $(echo "$CONFIDENCE < 0.65" | bc -l) )); then
    echo -e "${GREEN}Aggressive Exit Strategy${RESET}"
    echo -e "- Will exit positions quickly on early profit targets"
    echo -e "- More responsive to market changes"
    echo -e "- Higher trade frequency, smaller average profits"
    echo -e "- Better for volatile markets"
elif (( $(echo "$CONFIDENCE < 0.8" | bc -l) )); then
    echo -e "${YELLOW}Balanced Exit Strategy${RESET}"
    echo -e "- Good balance between early exits and letting profits run"
    echo -e "- Suitable for most market conditions"
    echo -e "- Moderate trade frequency with balanced risk/reward"
    echo -e "- The recommended starting point"
elif (( $(echo "$CONFIDENCE < 0.9" | bc -l) )); then
    echo -e "${RED}Conservative Exit Strategy${RESET}"
    echo -e "- Lets profits run longer, tighter stop losses"
    echo -e "- Less responsive to minor market fluctuations"
    echo -e "- Lower trade frequency, larger average profits"
    echo -e "- Better for trending markets"
else
    echo -e "${PURPLE}Extremely Selective Exit Strategy${RESET}"
    echo -e "- Only exits on very strong signals"
    echo -e "- Will hold positions through significant fluctuations"
    echo -e "- Very low trade frequency, potentially larger profits"
    echo -e "- For experienced traders in strong trending markets"
fi
echo

# Ask for confirmation
read -p "Do you want to run this elite exit strategy? (y/n): " CONFIRM
if [[ $CONFIRM == "y" || $CONFIRM == "Y" ]]; then
    echo -e "${GREEN}Starting trap aware dual traders with elite exit strategy...${RESET}"
    echo
    # Execute the command
    eval $CMD
else
    echo -e "${YELLOW}Operation cancelled.${RESET}"
fi 