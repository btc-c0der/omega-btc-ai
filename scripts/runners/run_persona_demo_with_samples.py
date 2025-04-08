#!/usr/bin/env python3
"""
OMEGA BTC AI - Persona-Based Exit Strategy Demo with Sample Positions
=====================================================================

This script runs the Persona-Enhanced RastaBitgetMonitor with sample positions
for demonstration purposes when no real positions are found.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import asyncio
import logging
import argparse
from typing import Dict, Any, List

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from scripts.integrate_persona_to_rastamon import PersonaEnhancedRastaBitgetMonitor, parse_arguments

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('persona_demo')

class DemoPersonaEnhancedMonitor(PersonaEnhancedRastaBitgetMonitor):
    """
    Enhanced monitor that uses sample positions for demonstration purposes.
    """
    
    async def get_positions(self) -> List[Dict[str, Any]]:
        """
        Override to return sample positions if no real positions are found.
        """
        # First try to get real positions
        real_positions = await super().get_positions()
        
        if real_positions:
            return real_positions
        
        # If no real positions, return sample positions
        logger.info("No real positions found, using sample positions for demonstration")
        
        sample_positions = []
        
        # Sample position 1: BTC long with profit
        btc_price = 47250  # Current BTC price (sample)
        btc_entry = 45000  # Entry price
        btc_position = {
            'symbol': 'BTCUSDT',
            'side': 'long',
            'total': 0.05,  # Position size in BTC
            'averageOpenPrice': btc_entry,
            'marketPrice': btc_price,
            'unrealizedPL': 0.05 * (btc_price - btc_entry),  # Unrealized profit/loss
            'leverage': 10,
            'liquidationPrice': 40500,
            'marginMode': 'cross',
            'notional': 0.05 * btc_price,
        }
        sample_positions.append(btc_position)
        
        # Sample position 2: ETH long with loss
        eth_price = 2850  # Current ETH price (sample)
        eth_entry = 3000  # Entry price
        eth_position = {
            'symbol': 'ETHUSDT',
            'side': 'long',
            'total': 0.5,  # Position size in ETH
            'averageOpenPrice': eth_entry, 
            'marketPrice': eth_price,
            'unrealizedPL': 0.5 * (eth_price - eth_entry),  # Unrealized profit/loss
            'leverage': 10,
            'liquidationPrice': 2700,
            'marginMode': 'cross',
            'notional': 0.5 * eth_price,
        }
        sample_positions.append(eth_position)
        
        # Sample position 3: SOL short with profit
        sol_price = 112.8  # Current SOL price (sample)
        sol_entry = 120  # Entry price
        sol_position = {
            'symbol': 'SOLUSDT',
            'side': 'short',
            'total': 2,  # Position size in SOL
            'averageOpenPrice': sol_entry,
            'marketPrice': sol_price,
            'unrealizedPL': 2 * (sol_entry - sol_price),  # Unrealized profit/loss
            'leverage': 5,
            'liquidationPrice': 126,
            'marginMode': 'cross',
            'notional': 2 * sol_price,
        }
        sample_positions.append(sol_position)
        
        # Sample position 4: DOGE short with big loss
        doge_price = 0.14  # Current DOGE price (sample) 
        doge_entry = 0.12  # Entry price
        doge_position = {
            'symbol': 'DOGEUSDT',
            'side': 'short',
            'total': 1000,  # Position size in DOGE
            'averageOpenPrice': doge_entry,
            'marketPrice': doge_price,
            'unrealizedPL': 1000 * (doge_entry - doge_price),  # Unrealized profit/loss
            'leverage': 3,
            'liquidationPrice': 0.15,
            'marginMode': 'cross',
            'notional': 1000 * doge_price,
        }
        sample_positions.append(doge_position)
        
        # Update positions dictionary
        positions_dict = {}
        for pos in sample_positions:
            symbol = pos.get('symbol', '')
            positions_dict[symbol] = pos
        
        self.positions = positions_dict
        return sample_positions

async def main():
    """Main function."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Get API credentials
    api_key = args.api_key or os.environ.get("BITGET_API_KEY", "")
    api_secret = args.api_secret or os.environ.get("BITGET_SECRET_KEY", "")
    passphrase = args.passphrase or os.environ.get("BITGET_PASSPHRASE", "")
    
    if not all([api_key, api_secret, passphrase]):
        print("Error: API credentials are required")
        print("Please provide them as command line arguments or set environment variables:")
        print("  BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE")
        return
    
    print("\nStarting OMEGA PERSONA-BASED EXIT STRATEGY DEMO with sample positions...")
    print("(Will use real positions if available, otherwise demo positions)")
    print("\nConnecting to BitGet...")
    
    # Initialize the demo monitor
    monitor = DemoPersonaEnhancedMonitor(
        api_key=api_key,
        api_secret=api_secret,
        passphrase=passphrase,
        interval=args.interval,
        use_color=not args.no_color,
        debug_mode=args.debug,
        enable_advanced_exits=not args.disable_advanced_exits,
        fee_coverage_threshold=args.fee_coverage,
        show_complementary=not args.disable_complementary,
        show_all_fib_levels=not args.disable_fib_levels,
        enable_persona_exits=not args.disable_persona_exits,
        min_persona_confidence=args.min_persona_confidence
    )
    
    try:
        # Start monitoring
        await monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\nExiting demo...")
    finally:
        monitor.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...") 