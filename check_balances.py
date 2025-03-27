#!/usr/bin/env python
import asyncio
import os
import sys
from dotenv import load_dotenv
from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders

async def check_balances():
    """Check current account balances in both long and short sub-accounts."""
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
    
    print(f"Checking balances with credentials from environment variables")
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
        short_sub_account=short_sub_account,
        account_limit=0.0  # Disable account limit for checking
    )
    
    try:
        # Initialize traders
        await dual_traders.initialize()
        
        # Get long trader balance
        long_balance = {}
        if dual_traders.long_trader and "strategic" in dual_traders.long_trader.traders:
            long_balance = await dual_traders.long_trader.traders["strategic"].get_balance()
        
        # Get short trader balance
        short_balance = {}
        if dual_traders.short_trader and "strategic" in dual_traders.short_trader.traders:
            short_balance = await dual_traders.short_trader.traders["strategic"].get_balance()
        
        # Print long sub-account balance details
        print("\n====== LONG SUB-ACCOUNT BALANCE ======")
        if "USDT" in long_balance:
            print(f"Total: {float(long_balance['USDT'].get('total', 0)):.2f} USDT")
            print(f"Free: {float(long_balance['USDT'].get('free', 0)):.2f} USDT")
            print(f"Used: {float(long_balance['USDT'].get('used', 0)):.2f} USDT")
        else:
            print("No USDT balance found")
        
        # Print short sub-account balance details
        print("\n====== SHORT SUB-ACCOUNT BALANCE ======")
        if "USDT" in short_balance:
            print(f"Total: {float(short_balance['USDT'].get('total', 0)):.2f} USDT")
            print(f"Free: {float(short_balance['USDT'].get('free', 0)):.2f} USDT")
            print(f"Used: {float(short_balance['USDT'].get('used', 0)):.2f} USDT")
        else:
            print("No USDT balance found")
        
        # Print combined details
        print("\n====== COMBINED BALANCE ======")
        long_total = float(long_balance.get("USDT", {}).get('total', 0))
        short_total = float(short_balance.get("USDT", {}).get('total', 0))
        total_balance = long_total + short_total
        print(f"Long sub-account: {long_total:.2f} USDT")
        print(f"Short sub-account: {short_total:.2f} USDT")
        print(f"Combined total: {total_balance:.2f} USDT")
        
    except Exception as e:
        print(f"Error checking balances: {str(e)}")
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
    asyncio.run(check_balances()) 