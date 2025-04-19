#!/usr/bin/env python3

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

"""
OMEGA BTC AI - Simple Position Check
===================================

A simple script to check BitGet positions using ccxt library.
"""

import os
import sys
import asyncio
import argparse
import ccxt.async_support as ccxt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_positions(api_key, api_secret, passphrase):
    """Check positions using provided API credentials"""
    # Initialize BitGet client
    exchange = ccxt.bitget({
        'apiKey': api_key,
        'secret': api_secret,
        'password': passphrase,
        'enableRateLimit': True
    })
    
    try:
        # Fetch positions
        positions = await exchange.fetch_positions()
        
        if not positions:
            print("\nNo open positions found.")
            return
        
        # Display positions
        print("\nOpen Positions:")
        print("=" * 80)
        print(f"{'Symbol':<15} {'Side':<8} {'Size':<12} {'Entry Price':<15} {'Leverage':<10} {'PnL':<15}")
        print("-" * 80)
        
        for position in positions:
            # Skip positions with zero size
            contracts = position.get('contracts', 0)
            if not contracts or float(str(contracts)) <= 0:
                continue
                
            symbol = position.get('symbol', 'N/A')
            side = position.get('side', 'N/A')
            size = float(str(contracts))
            
            entry_price = position.get('entryPrice', 0)
            entry_price = float(str(entry_price)) if entry_price else 0
            
            leverage = position.get('leverage', 0)
            leverage = float(str(leverage)) if leverage else 0
            
            pnl = position.get('unrealizedPnl', 0)
            pnl = float(str(pnl)) if pnl else 0
            
            print(f"{symbol:<15} {side:<8} {size:<12.5f} {entry_price:<15.5f} {leverage:<10.1f} {pnl:<15.2f}")
        
        print("=" * 80)
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Close exchange connection
        await exchange.close()

async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Check open positions on BitGet")
    parser.add_argument("--api-key", type=str, help="BitGet API key")
    parser.add_argument("--api-secret", type=str, help="BitGet API secret")
    parser.add_argument("--passphrase", type=str, help="BitGet API passphrase")
    args = parser.parse_args()
    
    # Get API credentials from arguments or environment variables
    api_key = args.api_key or os.environ.get('BITGET_API_KEY')
    api_secret = args.api_secret or os.environ.get('BITGET_SECRET_KEY')
    passphrase = args.passphrase or os.environ.get('BITGET_PASSPHRASE')
    
    if not all([api_key, api_secret, passphrase]):
        print("Error: API credentials not found in arguments or environment variables")
        print("Please provide credentials via command-line arguments or set environment variables:")
        print("  BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE")
        return
    
    # Check positions
    await check_positions(api_key, api_secret, passphrase)

if __name__ == "__main__":
    asyncio.run(main()) 