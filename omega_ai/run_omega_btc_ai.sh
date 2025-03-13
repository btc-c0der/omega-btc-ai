#!/bin/bash

# Navigate to the omega_ai directory
cd "$(dirname "$0")"

# Start the dashboard in the background
echo "Starting the OMEGA BTC AI Dashboard..."
python omega_ai/visualization/omega_dashboard.py &

# Start the BtcFuturesTrader with the OmegaSuggestionsModule
echo "Starting the BTC Futures Trading Simulation..."
python omega_ai/trading/btc_futures_trader.py