#!/bin/bash

# OMEGA BTC AI - Trap Aware Dual Traders Preset Launcher
# This script provides preset configurations for running the trap aware dual traders

# Color constants
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
RESET='\033[0m'

print_usage() {
    echo -e "${CYAN}OMEGA BTC AI - Trap Aware Dual Traders Preset Launcher${RESET}"
    echo
    echo -e "Usage: ./run_trap_aware_preset.sh [PRESET] [SYMBOL]"
    echo 
    echo -e "Available presets:"
    echo -e "  ${GREEN}conservative${RESET}  - Low risk, low capital, trap protection enabled"
    echo -e "  ${YELLOW}balanced${RESET}     - Medium risk, medium capital, trap protection enabled"
    echo -e "  ${RED}aggressive${RESET}    - High risk, high capital, higher leverage"
    echo -e "  ${BLUE}elite-exits${RESET}  - Enables elite exit strategy with high confidence"
    echo -e "  ${CYAN}no-protection${RESET} - Runs without trap protection features"
    echo -e "  ${CYAN}testnet${RESET}      - Runs on testnet with conservative settings"
    echo
    echo -e "If SYMBOL is not provided, BTCUSDT will be used by default."
    echo
    echo -e "Examples:"
    echo -e "  ./run_trap_aware_preset.sh conservative"
    echo -e "  ./run_trap_aware_preset.sh balanced ETHUSDT"
    echo -e "  ./run_trap_aware_preset.sh elite-exits"
}

if [ "$1" == "--help" ] || [ "$1" == "-h" ] || [ "$1" == "" ]; then
    print_usage
    exit 0
fi

# Set defaults
PRESET=$1
SYMBOL=${2:-BTCUSDT}

echo -e "${CYAN}Running OMEGA BTC AI Trap Aware Dual Traders with preset: ${YELLOW}$PRESET${RESET}"
echo -e "${CYAN}Trading symbol: ${YELLOW}$SYMBOL${RESET}"
echo

# Build base command
BASE_CMD="python run_trap_aware_dual_traders.py --symbol $SYMBOL"

# Apply preset configurations
case "$PRESET" in
    "conservative")
        echo -e "${GREEN}Using conservative preset:${RESET}"
        echo -e "- Lower capital allocation"
        echo -e "- Lower leverage (5x)"
        echo -e "- Trap protection enabled"
        echo -e "- Higher minimum balance requirement"
        echo
        PARAMS="--long-capital 20 --short-capital 20 --long-leverage 5 --short-leverage 5 --trap-probability-threshold 0.6 --min-free-balance 200"
        ;;
        
    "balanced")
        echo -e "${YELLOW}Using balanced preset:${RESET}"
        echo -e "- Medium capital allocation"
        echo -e "- Medium leverage (10x)"
        echo -e "- Trap protection enabled"
        echo -e "- Standard minimum balance"
        echo
        PARAMS="--long-capital 40 --short-capital 40 --long-leverage 10 --short-leverage 10 --trap-probability-threshold 0.7 --min-free-balance 100"
        ;;
        
    "aggressive")
        echo -e "${RED}Using aggressive preset:${RESET}"
        echo -e "- Higher capital allocation"
        echo -e "- Higher leverage (20x)"
        echo -e "- Less sensitive trap protection"
        echo -e "- Lower minimum balance requirement"
        echo
        PARAMS="--long-capital 60 --short-capital 60 --long-leverage 20 --short-leverage 20 --trap-probability-threshold 0.8 --min-free-balance 50"
        ;;
        
    "elite-exits")
        echo -e "${BLUE}Using elite exits preset:${RESET}"
        echo -e "- Elite exit strategy enabled"
        echo -e "- High confidence threshold (0.8)"
        echo -e "- Medium capital allocation"
        echo -e "- Medium leverage (10x)"
        echo -e "- Trap protection enabled"
        echo
        PARAMS="--long-capital 40 --short-capital 40 --long-leverage 10 --short-leverage 10 --enable-elite-exits --elite-exit-confidence 0.8 --trap-probability-threshold 0.7 --min-free-balance 100"
        ;;
        
    "no-protection")
        echo -e "${CYAN}Using no protection preset:${RESET}"
        echo -e "- Trap protection disabled"
        echo -e "- Medium capital allocation"
        echo -e "- Medium leverage (10x)"
        echo -e "- No elite exits"
        echo
        PARAMS="--long-capital 40 --short-capital 40 --long-leverage 10 --short-leverage 10 --no-trap-protection --min-free-balance 100"
        ;;
        
    "testnet")
        echo -e "${CYAN}Using testnet preset:${RESET}"
        echo -e "- Running on testnet"
        echo -e "- Conservative settings"
        echo -e "- Lower capital allocation"
        echo -e "- Lower leverage (5x)"
        echo -e "- Trap protection enabled"
        echo
        PARAMS="--testnet --long-capital 20 --short-capital 20 --long-leverage 5 --short-leverage 5 --trap-probability-threshold 0.6 --min-free-balance 20"
        ;;
        
    *)
        echo -e "${RED}Unknown preset: $PRESET${RESET}"
        echo
        print_usage
        exit 1
        ;;
esac

# Build final command
CMD="$BASE_CMD $PARAMS"

echo -e "${CYAN}Command to execute:${RESET}"
echo -e "$CMD"
echo

# Ask for confirmation
read -p "Do you want to run this configuration? (y/n): " CONFIRM
if [[ $CONFIRM == "y" || $CONFIRM == "Y" ]]; then
    echo -e "${GREEN}Starting trap aware dual traders...${RESET}"
    echo
    # Execute the command
    eval $CMD
else
    echo -e "${YELLOW}Operation cancelled.${RESET}"
fi 