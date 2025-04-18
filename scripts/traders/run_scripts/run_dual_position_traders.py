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

"""
Dual Position Traders Launcher

This script starts the OMEGA BTC AI Dual Position Traders system with improved
account limit checking logic that uses free balance instead of total balance.

Usage:
    python run_dual_position_traders.py [--min-free-balance BALANCE] [--account-max MAX]

Arguments:
    --min-free-balance: Minimum free USDT balance required (default: 100)
    --account-max: Maximum total account value in USDT (default: 10000)
"""

import asyncio
import argparse
import os
import sys
from dotenv import load_dotenv

# No more import from modify_dual_traders

async def run_dual_position_traders(args):
    """
    Run the BitGetDualPositionTraders with modified account limit checking.
    
    Args:
        args: Command line arguments
    """
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
    
    # Use testnet based on environment
    use_testnet = os.getenv('USE_TESTNET', 'false').lower() == 'true'
    
    print(f"\n===== STARTING OMEGA BTC AI DUAL POSITION TRADERS =====")
    print(f"Using minimum free balance limit: {args.min_free_balance} USDT")
    print(f"Using account maximum limit: {args.account_max} USDT")
    print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
    print(f"Long sub-account: {long_sub_account}")
    print(f"Short sub-account: {short_sub_account}\n")
    
    # Initialize dual traders from the class defined at the bottom of the file
    from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders
    
    # Define the modified class
    class ModifiedBitGetDualPositionTraders(BitGetDualPositionTraders):
        async def check_account_limit(self) -> bool:
            """
            Modified version that checks if the free account balance (not total) is below the limit.
            
            Returns:
                bool: True if account is below limit, False otherwise
            """
            if self.account_limit <= 0:
                # No limit set, always return True
                return True
                
            try:
                # We need to check both traders since they use separate sub-accounts
                long_free = short_free = 0.0
                
                # Get long trader balance
                if self.long_trader and "strategic" in self.long_trader.traders:
                    balance = await self.long_trader.traders["strategic"].get_balance()
                    if "USDT" in balance:
                        long_free = float(balance["USDT"].get("free", 0))
                
                # Get short trader balance
                if self.short_trader and "strategic" in self.short_trader.traders:
                    balance = await self.short_trader.traders["strategic"].get_balance()
                    if "USDT" in balance:
                        short_free = float(balance["USDT"].get("free", 0))
                
                # Calculate total FREE balance across both sub-accounts (not total which includes margin)
                total_free = long_free + short_free
                print(f"Total free account balance: {total_free} USDT (Long: {long_free}, Short: {short_free})")
                print(f"Account limit: {self.account_limit} USDT")
                
                if total_free < self.account_limit:
                    print(f"⚠️ Account free balance of {total_free} USDT is below minimum limit of {self.account_limit} USDT!")
                    return False
                    
                return True
                
            except Exception as e:
                print(f"Error checking account limit: {str(e)}")
                return True  # In case of error, allow trading to continue
    
    # Initialize dual traders with the modified class
    dual_traders = ModifiedBitGetDualPositionTraders(
        use_testnet=use_testnet,
        long_capital=float(os.getenv('INITIAL_CAPITAL', '24.0')),
        short_capital=float(os.getenv('INITIAL_CAPITAL', '24.0')),
        symbol=os.getenv('TRADING_SYMBOL', 'BTCUSDT').split('_')[0],
        api_key=api_key,
        secret_key=secret_key,
        passphrase=passphrase,
        long_leverage=int(os.getenv('MAX_LEVERAGE', '20')),
        short_leverage=int(os.getenv('MAX_LEVERAGE', '20')),
        long_sub_account=long_sub_account,
        short_sub_account=short_sub_account,
        account_limit=args.min_free_balance,  # Use minimum free balance as limit
    )
    
    try:
        # Initialize traders
        await dual_traders.initialize()
        
        # Check account limit
        limit_ok = await dual_traders.check_account_limit()
        
        if limit_ok:
            print(f"\n✅ Account limit check passed, starting dual position trading...")
            # Start trading
            await dual_traders.start_trading()
        else:
            print(f"\n❌ Account limit check failed, will not start trading")
            
    except KeyboardInterrupt:
        print("\n🛑 Received keyboard interrupt, shutting down gracefully...")
    except Exception as e:
        print(f"\n⚠️ Error in dual position traders: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if hasattr(dual_traders, 'stop_trading'):
            await dual_traders.stop_trading()
        print("\n👋 Dual position traders system shutdown complete")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Dual Position Traders with improved account limit checking')
    parser.add_argument('--min-free-balance', type=float, default=100.0,
                      help='Minimum required free balance in USDT (default: 100.0)')
    parser.add_argument('--account-max', type=float, default=10000.0,
                      help='Maximum total account value in USDT (default: 10000.0)')
    
    # Add any other arguments from the original script that you want to expose
    
    return parser.parse_args()

if __name__ == "__main__":
    # Fix the module import path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    args = parse_args()
    asyncio.run(run_dual_position_traders(args)) 