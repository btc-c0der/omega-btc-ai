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
OMEGA BTC AI - Position Checker
==============================

A simple script to check BitGet positions using .env variables.
"""

import sys
import os
import asyncio
import ccxt.async_support as ccxt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_SECRET_KEY = os.getenv('BITGET_SECRET_KEY')
BITGET_PASSPHRASE = os.getenv('BITGET_PASSPHRASE')

async def main():
    # Check if credentials are set
    if not all([BITGET_API_KEY, BITGET_SECRET_KEY, BITGET_PASSPHRASE]):
        print("Error: API credentials not found in .env file")
        print("Please make sure your .env file contains BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE")
        return
    
    print("Connecting to BitGet exchange...")
    
    # Initialize BitGet client
    exchange = ccxt.bitget({
        'apiKey': BITGET_API_KEY,
        'secret': BITGET_SECRET_KEY,
        'password': BITGET_PASSPHRASE,
        'enableRateLimit': True
    })
    
    try:
        # Fetch positions
        print("Fetching positions...")
        positions = await exchange.fetch_positions()
        
        if not positions:
            print("\nNo open positions found.")
            return
        
        # Display positions
        print("\nOpen Positions:")
        print("=" * 80)
        print(f"{'Symbol':<15} {'Side':<8} {'Size':<12} {'Entry Price':<15} {'Leverage':<10} {'PnL':<15}")
        print("-" * 80)
        
        active_positions = False
        
        for position in positions:
            # Skip positions with zero size
            contracts = position.get('contracts', 0)
            if not contracts or float(str(contracts)) <= 0:
                continue
            
            active_positions = True    
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
        
        if not active_positions:
            print("No active positions with non-zero size found.")
            
        print("=" * 80)
        
        # Instructions for adjusting leverage
        print("\nTo adjust leverage on a position:")
        print("1. Go to the BitGet interface")
        print("2. Find the position you want to adjust")
        print("3. Click on the leverage setting")
        print("4. Enter your desired leverage (11x)")
        print("5. Save the changes")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Close exchange connection
        await exchange.close()

if __name__ == "__main__":
    asyncio.run(main()) 