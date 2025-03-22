#!/usr/bin/env python
"""
Trap-Aware Dual Position Traders Launcher

This script starts the OMEGA BTC AI Trap-Aware Dual Position Traders system.
This enhanced version includes market maker trap detection functionality 
and elite exit strategies.

Usage:
    python run_trap_aware_dual_traders.py [--min-free-balance BALANCE] [--account-max MAX]
                                        [--trap-probability-threshold PROB] [--enable-elite-exits]

Arguments:
    --min-free-balance: Minimum free USDT balance required (default: 100)
    --account-max: Maximum total account value in USDT (default: 10000.0)
    --trap-probability-threshold: Threshold for considering trap probability (default: 0.7)
    --trap-alert-threshold: Threshold for sending trap alerts (default: 0.8)
    --enable-elite-exits: Enable elite exit strategies (default: False)
    --elite-exit-confidence: Minimum confidence required for elite exit signals (default: 0.7)
"""

import asyncio
import argparse
import os
import sys
from dotenv import load_dotenv

async def run_trap_aware_dual_traders(args):
    """
    Run the TrapAwareDualTraders with modified account limit checking.
    
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
    
    print(f"\n===== STARTING OMEGA BTC AI TRAP-AWARE DUAL POSITION TRADERS =====")
    print(f"Using minimum free balance limit: {args.min_free_balance} USDT")
    print(f"Using account maximum limit: {args.account_max} USDT")
    print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
    print(f"Long sub-account: {long_sub_account}")
    print(f"Short sub-account: {short_sub_account}")
    print(f"Trap probability threshold: {args.trap_probability_threshold}")
    print(f"Trap alert threshold: {args.trap_alert_threshold}")
    print(f"Elite exits enabled: {args.enable_elite_exits}")
    if args.enable_elite_exits:
        print(f"Elite exit confidence: {args.elite_exit_confidence}\n")
    
    # Import the TrapAwareDualTraders class
    from omega_ai.trading.strategies.trap_aware_dual_traders import TrapAwareDualTraders
    
    # Define the modified class with free balance checking
    class ModifiedTrapAwareDualTraders(TrapAwareDualTraders):
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
    
    # Initialize trap-aware dual traders with the modified class
    dual_traders = ModifiedTrapAwareDualTraders(
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
        short_sub_account=short_sub_account,
        account_limit=args.min_free_balance,  # Use minimum free balance as limit
        trap_probability_threshold=args.trap_probability_threshold,
        trap_alert_threshold=args.trap_alert_threshold,
        enable_trap_protection=True,
        enable_elite_exits=args.enable_elite_exits,
        elite_exit_confidence=args.elite_exit_confidence
    )
    
    try:
        # Initialize traders
        await dual_traders.initialize()
        
        # Check account limit
        limit_ok = await dual_traders.check_account_limit()
        
        if limit_ok:
            print(f"\n✅ Account limit check passed, starting trap-aware dual position trading...")
            # Start trading
            await dual_traders.start_trading()
        else:
            print(f"\n❌ Account limit check failed, will not start trading")
            
    except KeyboardInterrupt:
        print("\n🛑 Received keyboard interrupt, shutting down gracefully...")
    except Exception as e:
        print(f"\n⚠️ Error in trap-aware dual position traders: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if hasattr(dual_traders, 'stop_trading'):
            await dual_traders.stop_trading()
        print("\n👋 Trap-aware dual position traders system shutdown complete")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Trap-Aware Dual Position Traders')
    parser.add_argument('--min-free-balance', type=float, default=100.0,
                      help='Minimum required free balance in USDT (default: 100.0)')
    parser.add_argument('--account-max', type=float, default=10000.0,
                      help='Maximum total account value in USDT (default: 10000.0)')
    parser.add_argument('--trap-probability-threshold', type=float, default=0.7,
                      help='Threshold for considering trap probability (default: 0.7)')
    parser.add_argument('--trap-alert-threshold', type=float, default=0.8,
                      help='Threshold for sending trap alerts (default: 0.8)')
    parser.add_argument('--enable-elite-exits', action='store_true',
                      help='Enable elite exit strategies')
    parser.add_argument('--elite-exit-confidence', type=float, default=0.7,
                      help='Minimum confidence required for elite exit signals (default: 0.7)')
    
    return parser.parse_args()

if __name__ == "__main__":
    # Fix the module import path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    args = parse_args()
    asyncio.run(run_trap_aware_dual_traders(args)) 