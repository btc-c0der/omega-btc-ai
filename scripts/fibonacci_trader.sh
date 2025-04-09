#!/bin/bash

# ==================================================
# OMEGA BTC AI - Fibonacci Trader Shell Wrapper
# ==================================================
# This script provides a convenient wrapper for running
# the Fibonacci trading bot with different profiles.

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Help message
function show_help {
    echo "========================================================"
    echo "OMEGA BTC AI - Fibonacci Trader"
    echo "========================================================"
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --profile <profile>  Trader profile type (strategic, aggressive, newbie, scalper)"
    echo "  --symbol <symbol>    Trading symbol (default: BTCUSDT)"
    echo "  --live               Use live trading (default: testnet)"
    echo "  --capital <amount>   Initial capital amount (default: 1000.0)"
    echo "  --leverage <value>   Trading leverage (default: 3)"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --profile strategic                  # Run with strategic profile on testnet"
    echo "  $0 --profile aggressive --symbol ETHUSDT # Run with aggressive profile for ETH"
    echo "  $0 --profile scalper --live            # Run with scalper profile on mainnet"
    echo "========================================================"
}

# Default values
PROFILE="strategic"
SYMBOL="BTCUSDT"
TESTNET="--testnet"
CAPITAL="1000.0"
LEVERAGE="3"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile)
            PROFILE="$2"
            shift 2
            ;;
        --symbol)
            SYMBOL="$2"
            shift 2
            ;;
        --live)
            TESTNET=""
            shift
            ;;
        --capital)
            CAPITAL="$2"
            shift 2
            ;;
        --leverage)
            LEVERAGE="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Error: Unknown option $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate profile
if [[ ! "$PROFILE" =~ ^(strategic|aggressive|newbie|scalper)$ ]]; then
    echo "Error: Invalid profile '$PROFILE'"
    echo "Valid profiles: strategic, aggressive, newbie, scalper"
    exit 1
fi

# Check for API credentials
if [[ -z "$TESTNET" ]]; then
    # Live mode - check for live API keys
    if [[ -z "$BITGET_API_KEY" || -z "$BITGET_SECRET_KEY" || -z "$BITGET_PASSPHRASE" ]]; then
        echo "Error: Live trading requires environment variables to be set:"
        echo "  BITGET_API_KEY, BITGET_SECRET_KEY, BITGET_PASSPHRASE"
        exit 1
    fi
    echo "⚠️  WARNING: Using LIVE trading mode with real funds! ⚠️"
    read -p "Are you sure you want to continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
else
    # Testnet mode - check for testnet API keys
    if [[ -z "$BITGET_TESTNET_API_KEY" || -z "$BITGET_TESTNET_SECRET_KEY" || -z "$BITGET_TESTNET_PASSPHRASE" ]]; then
        echo "Error: Testnet trading requires environment variables to be set:"
        echo "  BITGET_TESTNET_API_KEY, BITGET_TESTNET_SECRET_KEY, BITGET_TESTNET_PASSPHRASE"
        exit 1
    fi
    echo "Using TEST trading mode with simulated funds."
fi

# Run the bot
echo "========================================================"
echo "OMEGA BTC AI - Starting Fibonacci Trader"
echo "========================================================"
echo "Profile: $PROFILE"
echo "Symbol: $SYMBOL"
echo "Mode: ${TESTNET:+Testnet}${TESTNET:-Live}"
echo "Capital: $CAPITAL"
echo "Leverage: $LEVERAGE"
echo "========================================================"

# Set log file
LOG_FILE="$PROJECT_ROOT/logs/fibonacci_${PROFILE}_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$PROJECT_ROOT/logs"

# Create command with arguments
CMD="$SCRIPT_DIR/run_fibonacci_bot.py --profile $PROFILE --symbol $SYMBOL --capital $CAPITAL --leverage $LEVERAGE $TESTNET"

# Run the bot
echo "Starting bot with command: $CMD"
echo "Logging to: $LOG_FILE"
echo "Press Ctrl+C to stop the bot"
echo 

# Execute the command
$CMD 2>&1 | tee "$LOG_FILE" 