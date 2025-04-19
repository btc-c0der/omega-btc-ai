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
Test script to validate the get_positions method.
"""

import os
import sys
import time
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader

def main():
    """Main entry point for the test script."""
    print("Testing BitGet get_positions method with sub-account...")
    
    # Get API credentials from environment variables
    api_key = os.environ.get("BITGET_API_KEY", "")
    secret_key = os.environ.get("BITGET_SECRET_KEY", "")
    passphrase = os.environ.get("BITGET_PASSPHRASE", "")
    
    # Verify API credentials are available
    if not api_key or not secret_key or not passphrase:
        print("Error: API credentials are missing. Please set environment variables.")
        return
    
    print(f"Using API key: {api_key[:5]}...")
    
    # Create trader with sub-account name
    sub_account_name = "sub_7739509698" 
    
    trader = BitGetTrader(
        profile_type="strategic",
        api_key=api_key,
        secret_key=secret_key,
        passphrase=passphrase,
        use_testnet=False,  # Use mainnet
        sub_account_name=sub_account_name
    )
    
    print(f"Trader initialized with sub-account: {sub_account_name}")
    
    # Test get_positions method
    print("Testing get_positions for BTCUSDT...")
    positions = trader.get_positions("BTCUSDT")
    
    if positions:
        print(f"Successfully retrieved {len(positions)} positions:")
        for position in positions:
            print(f"- Symbol: {position.get('symbol', 'Unknown')}")
            print(f"  Side: {position.get('holdSide', 'Unknown')}")
            print(f"  Size: {position.get('total', '0')}")
            print(f"  Entry Price: {position.get('averageOpenPrice', '0')}")
            print(f"  Mark Price: {position.get('marketPrice', '0')}")
            print(f"  Unrealized PnL: {position.get('unrealizedPL', '0')}")
    else:
        print("No positions found or error retrieving positions.")
    
    # Test get all positions method
    print("\nTesting get_positions with no symbol (all positions)...")
    all_positions = trader.get_positions()
    
    if all_positions:
        print(f"Successfully retrieved {len(all_positions)} positions:")
        for position in all_positions:
            print(f"- Symbol: {position.get('symbol', 'Unknown')}")
    else:
        print("No positions found or error retrieving positions.")

if __name__ == "__main__":
    main() 