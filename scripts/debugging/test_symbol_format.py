#!/usr/bin/env python

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


import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('test_symbol_format')

# Import the classes we want to test
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders

# Create config dictionary for BitGetCCXT
ccxt_config = {
    'api_key': 'test_key',
    'api_secret': 'test_secret',
    'api_password': 'test_password',
    'use_testnet': True
}

# Create instances
bitget_ccxt = BitGetCCXT(config=ccxt_config)

bitget_trader = BitGetLiveTraders(
    use_testnet=True,
    initial_capital=24.0,
    symbol="BTCUSDT",
    api_key="test_key",
    secret_key="test_secret",
    passphrase="test_password"
)

# Test symbol formatting
test_symbols = ["BTC", "BTCUSDT", "BTC/USDT", "BTC/USDT:USDT"]

logger.info("Testing BitGetCCXT._format_symbol:")
for symbol in test_symbols:
    formatted = bitget_ccxt._format_symbol(symbol)
    logger.info(f"  Input: {symbol} → Output: {formatted}")

logger.info("\nTesting BitGetLiveTraders._format_symbol:")
for symbol in test_symbols:
    formatted = bitget_trader._format_symbol(symbol)
    logger.info(f"  Input: {symbol} → Output: {formatted}")

logger.info("Symbol formatting test completed.") 