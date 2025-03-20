#!/usr/bin/env python3
"""
OMEGA BTC AI - Fibonacci Bot Runner
==================================

This script runs the Fibonacci trading bot with the strategic profile.
It provides a simple way to launch the trading bot with command line arguments.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import argparse
import asyncio
import logging
from typing import Optional

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
from omega_ai.trading.exchanges.fibonacci_trader_integration import run_standalone_fibonacci_trader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('fibonacci_bot.log')
    ]
)
logger = logging.getLogger(__name__)

async def main(args: argparse.Namespace) -> None:
    """Run the Fibonacci trading bot with the provided arguments."""
    try:
        # Get API credentials from environment variables if not provided
        api_key = args.api_key or os.environ.get(
            "BITGET_TESTNET_API_KEY" if args.testnet else "BITGET_API_KEY", "")
        api_secret = args.api_secret or os.environ.get(
            "BITGET_TESTNET_SECRET_KEY" if args.testnet else "BITGET_SECRET_KEY", "")
        passphrase = args.passphrase or os.environ.get(
            "BITGET_TESTNET_PASSPHRASE" if args.testnet else "BITGET_PASSPHRASE", "")
        
        if not all([api_key, api_secret, passphrase]):
            logger.error("API credentials are required. Either provide them as arguments or set environment variables.")
            return
        
        # Run the Fibonacci trader
        await run_standalone_fibonacci_trader(
            symbol=args.symbol,
            profile_type=args.profile,
            use_testnet=args.testnet,
            initial_capital=args.capital,
            leverage=args.leverage,
            api_key=api_key,
            api_secret=api_secret,
            passphrase=passphrase
        )
    
    except KeyboardInterrupt:
        logger.info("Trading bot stopped by user")
    except Exception as e:
        logger.error(f"Error running Fibonacci trading bot: {str(e)}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the Fibonacci trading bot")
    parser.add_argument("--symbol", type=str, default="BTCUSDT", help="Trading symbol (default: BTCUSDT)")
    parser.add_argument("--profile", type=str, default="strategic", 
                        choices=["strategic", "aggressive", "newbie", "scalper"],
                        help="Trader profile type (default: strategic)")
    parser.add_argument("--testnet", action="store_true", help="Use testnet instead of mainnet")
    parser.add_argument("--capital", type=float, default=1000.0, help="Initial capital (default: 1000.0)")
    parser.add_argument("--leverage", type=int, default=3, help="Trading leverage (default: 3)")
    parser.add_argument("--api-key", type=str, help="BitGet API key (optional, can use environment variable)")
    parser.add_argument("--api-secret", type=str, help="BitGet API secret (optional, can use environment variable)")
    parser.add_argument("--passphrase", type=str, help="BitGet API passphrase (optional, can use environment variable)")
    
    args = parser.parse_args()
    
    # Run the main function
    asyncio.run(main(args)) 