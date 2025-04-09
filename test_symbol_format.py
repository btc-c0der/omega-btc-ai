#!/usr/bin/env python

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