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


# OMEGA BTC AI - Default Configuration Setup
# This script sets up the default trading configuration

echo "Setting up default trading configuration..."
echo "Symbol: BTCUSDT"
echo "Long Capital (strategic_trader): 150.0 USDT"
echo "Short Capital (fst_short): 200.0 USDT"
echo "Leverage: 11x (both long and short)"
echo "Account Limit: 1500.0 USDT"
echo "Min Free Balance: 0.0 USDT (no restrictions)"

# Run with default configuration
./run_trap_aware_traders.sh --mainnet --long-leverage 11 --short-leverage 11 --long-capital 150 --short-capital 200 --account-limit 1500 --symbol BTCUSDT --min-free-balance 0

# If you want to run the regular dual position traders directly:
# python -m omega_ai.trading.exchanges.dual_position_traders --mainnet --long-leverage 11 --short-leverage 11 --long-capital 150 --short-capital 200 --account-limit 1500 --symbol BTCUSDT
