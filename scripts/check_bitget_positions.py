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
OMEGA BTC AI - BitGet Position Checker
======================================

This script directly queries the BitGet API to check open positions.
"""

import os
import sys
import asyncio
import ccxt.async_support as ccxt
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ANSI color codes for prettier output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def log_color(message, color=GREEN):
    """Print a colorized message."""
    print(f"{color}{message}{RESET}")

async def check_bitget_positions():
    """Check open positions on BitGet API."""
    # Get API credentials from environment variables
    api_key = os.getenv('BITGET_API_KEY')
    api_secret = os.getenv('BITGET_SECRET_KEY')
    api_passphrase = os.getenv('BITGET_PASSPHRASE')
    
    if not all([api_key, api_secret, api_passphrase]):
        log_color("BitGet API credentials not found. Please check your .env file.", RED)
        return
    
    # Safely access first and last 4 characters of API key
    key_preview = f"{api_key[:4]}...{api_key[-4:]}" if api_key and len(api_key) >= 8 else "INVALID_KEY"
    log_color(f"Connecting to BitGet with API key: {key_preview}", BLUE)
    
    # Initialize BitGet client
    exchange = ccxt.bitget({
        'apiKey': api_key,
        'secret': api_secret,
        'password': api_passphrase,
        'enableRateLimit': True
    })
    
    try:
        # Fetch positions
        log_color("Fetching positions from BitGet...", BLUE)
        positions = await exchange.fetch_positions()
        
        # Filter for active positions (non-zero size)
        active_positions = [p for p in positions if p.get('contracts', 0) and float(str(p.get('contracts', 0))) > 0]
        
        log_color(f"\n==== BITGET OPEN POSITIONS ====", CYAN)
        log_color(f"Total open positions: {len(active_positions)}", BLUE)
        
        # Display position details
        if active_positions:
            log_color(f"\n{'Symbol':<20} {'Side':<8} {'Size':<12} {'Entry Price':<15} {'Leverage':<10} {'PnL':<15}", YELLOW)
            log_color(f"{'-'*80}", YELLOW)
            
            total_pnl = 0
            
            for pos in active_positions:
                symbol = pos.get('symbol', 'N/A')
                side = pos.get('side', 'N/A')
                size = float(str(pos.get('contracts', 0)))
                entry_price = float(str(pos.get('entryPrice', 0)))
                leverage = float(str(pos.get('leverage', 0)))
                unrealized_pnl = float(str(pos.get('unrealizedPnl', 0)))
                total_pnl += unrealized_pnl
                
                # Safely handle None values for side
                side_str = str(side).upper() if side else "UNKNOWN"
                color = GREEN if side_str == 'LONG' else RED
                pnl_color = GREEN if unrealized_pnl >= 0 else RED
                
                log_color(
                    f"{symbol:<20} {side:<8} {size:<12.5f} {entry_price:<15.2f} {leverage:<10.1f} {unrealized_pnl:<15.2f}",
                    color
                )
            
            log_color(f"{'-'*80}", YELLOW)
            log_color(f"Total Unrealized PnL: {total_pnl:.2f} USDT", GREEN if total_pnl >= 0 else RED)
            
            # Compare with Redis data
            log_color(f"\n==== COMPARISON ====", CYAN)
            log_color(f"Redis showed 53 positions", YELLOW)
            log_color(f"BitGet API shows {len(active_positions)} actual open positions", 
                     GREEN if len(active_positions) > 0 else RED)
            
            if len(active_positions) != 53:
                log_color("Discrepancy between Redis and BitGet API!", YELLOW)
                log_color("This could be because:", BLUE)
                log_color("1. Some positions stored in Redis have been closed", BLUE)
                log_color("2. Redis contains simulated/test positions", BLUE)
                log_color("3. Redis contains historical position data", BLUE)
        else:
            log_color("No open positions found on BitGet.", YELLOW)
    
    except Exception as e:
        log_color(f"Error fetching positions: {e}", RED)
    
    finally:
        # Close exchange connection
        await exchange.close()

async def main():
    """Main function."""
    log_color("\n====== OMEGA BTC AI - BITGET POSITION CHECKER ======", CYAN)
    await check_bitget_positions()

if __name__ == "__main__":
    asyncio.run(main()) 