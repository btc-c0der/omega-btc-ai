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

import asyncio
import os
import sys
from dotenv import load_dotenv
from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders

def safe_float(value, default=0.0):
    """Safely convert value to float, handling None values."""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

async def check_positions():
    """Check current open positions in both long and short sub-accounts."""
    # Load environment variables
    load_dotenv()
    
    # Set Redis host to localhost instead of 'redis'
    os.environ['REDIS_HOST'] = 'localhost'
    
    # Get API credentials from environment
    api_key = os.getenv('BITGET_API_KEY', '')
    secret_key = os.getenv('BITGET_SECRET_KEY', '')
    passphrase = os.getenv('BITGET_PASSPHRASE', '')
    
    # Get sub-account names
    long_sub_account = os.getenv('STRATEGIC_SUB_ACCOUNT_NAME', '')
    short_sub_account = "fst_short"  # Default from the code
    
    print(f"Checking positions with credentials from environment variables")
    if api_key:
        print(f"API Key: {api_key[:5]}...{api_key[-5:]}")
    else:
        print("API Key not found in environment")
    print(f"Long sub-account: {long_sub_account}")
    print(f"Short sub-account: {short_sub_account}")
    
    # Use testnet based on environment
    use_testnet = os.getenv('USE_TESTNET', 'false').lower() == 'true'
    
    # Initialize dual traders
    dual_traders = BitGetDualPositionTraders(
        use_testnet=use_testnet,
        long_capital=float(os.getenv('INITIAL_CAPITAL', '24.0')),
        short_capital=float(os.getenv('INITIAL_CAPITAL', '24.0')),
        symbol=os.getenv('TRADING_SYMBOL', 'BTCUSDT').split('_')[0],
        api_key=api_key,
        secret_key=secret_key,
        passphrase=passphrase,
        long_leverage=int(os.getenv('MAX_LEVERAGE', '11')),
        short_leverage=int(os.getenv('MAX_LEVERAGE', '11')),
        long_sub_account=long_sub_account,
        short_sub_account=short_sub_account
    )
    
    try:
        # Initialize traders
        await dual_traders.initialize()
        
        # Get account balance
        await dual_traders.check_account_limit()
        
        # Get positions
        long_positions, long_pnl = await dual_traders._get_trader_metrics(dual_traders.long_trader)
        short_positions, short_pnl = await dual_traders._get_trader_metrics(dual_traders.short_trader)
        
        # Print summary
        print("\n====== POSITION SUMMARY ======")
        print(f"Long positions: {len(long_positions)}")
        print(f"Short positions: {len(short_positions)}")
        print(f"Long PnL: {long_pnl:.2f} USDT")
        print(f"Short PnL: {short_pnl:.2f} USDT")
        print(f"Total PnL: {(long_pnl + short_pnl):.2f} USDT")
        
        # Print long position details
        if long_positions:
            print("\n====== LONG POSITIONS ======")
            for i, pos in enumerate(long_positions):
                side = pos.get('side', 'UNKNOWN').upper()
                size = safe_float(pos.get('contracts', 0))
                price = safe_float(pos.get('entryPrice', 0))
                unreal_pnl = safe_float(pos.get('unrealizedPnl', 0))
                real_pnl = safe_float(pos.get('realizedPnl', 0))
                
                print(f"Position #{i+1}")
                print(f"  Side: {side}")
                print(f"  Size: {size:.4f}")
                print(f"  Entry Price: {price:.2f} USD")
                print(f"  Unrealized PnL: {unreal_pnl:+.2f}")
                print(f"  Realized PnL: {real_pnl:+.2f}")
                print()
        
        # Print short position details
        if short_positions:
            print("\n====== SHORT POSITIONS ======")
            for i, pos in enumerate(short_positions):
                side = pos.get('side', 'UNKNOWN').upper()
                size = safe_float(pos.get('contracts', 0))
                price = safe_float(pos.get('entryPrice', 0))
                unreal_pnl = safe_float(pos.get('unrealizedPnl', 0))
                real_pnl = safe_float(pos.get('realizedPnl', 0))
                
                print(f"Position #{i+1}")
                print(f"  Side: {side}")
                print(f"  Size: {size:.4f}")
                print(f"  Entry Price: {price:.2f} USD")
                print(f"  Unrealized PnL: {unreal_pnl:+.2f}")
                print(f"  Realized PnL: {real_pnl:+.2f}")
                print()
                
    except Exception as e:
        print(f"Error checking positions: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Safely close connections
        if hasattr(dual_traders, 'long_trader') and dual_traders.long_trader:
            for name, trader in dual_traders.long_trader.traders.items():
                if hasattr(trader, 'exchange') and hasattr(trader.exchange, 'close'):
                    await trader.exchange.close()
        
        if hasattr(dual_traders, 'short_trader') and dual_traders.short_trader:
            for name, trader in dual_traders.short_trader.traders.items():
                if hasattr(trader, 'exchange') and hasattr(trader.exchange, 'close'):
                    await trader.exchange.close()

if __name__ == "__main__":
    asyncio.run(check_positions()) 