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
OMEGA BTC AI - BitGet API Credentials Verification Tool
This script verifies that your BitGet API credentials are working correctly.
"""

import os
import sys
import asyncio
import traceback
import json
from datetime import datetime

# Try to import the BitGetCCXT client
try:
    from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
except ImportError:
    print("Error: Could not import BitGetCCXT. Make sure the OMEGA BTC AI package is installed.")
    sys.exit(1)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

async def verify_credentials(use_testnet=False, sub_account=""):
    """Verify BitGet API credentials and fetch account information."""
    print(f"{CYAN}======================================================{RESET}")
    print(f"{CYAN}= OMEGA BTC AI - BitGet API Credentials Verifier     ={RESET}")
    print(f"{CYAN}======================================================{RESET}")
    print(f"{CYAN}Mode: {'Testnet' if use_testnet else 'Mainnet'}{RESET}")
    if sub_account:
        print(f"{CYAN}Sub-account: {sub_account}{RESET}")
    print(f"{CYAN}======================================================{RESET}")
    
    # Look for API credentials in environment variables
    api_key = os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
    secret_key = os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
    passphrase = os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
    
    # Check if credentials are available
    if not api_key or not secret_key or not passphrase:
        print(f"{RED}Error: Missing API credentials. Please set the following environment variables:{RESET}")
        print(f"  - {'BITGET_TESTNET_API_KEY' if use_testnet else 'BITGET_API_KEY'}")
        print(f"  - {'BITGET_TESTNET_SECRET_KEY' if use_testnet else 'BITGET_SECRET_KEY'}")
        print(f"  - {'BITGET_TESTNET_PASSPHRASE' if use_testnet else 'BITGET_PASSPHRASE'}")
        return False
    
    try:
        print(f"{YELLOW}Initializing BitGet client...{RESET}")
        # Initialize BitGet client
        bg = BitGetCCXT(
            api_key=api_key,
            api_secret=secret_key,
            password=passphrase,
            use_testnet=use_testnet,
            sub_account=sub_account
        )
        
        print(f"{YELLOW}Connecting to BitGet API...{RESET}")
        
        # Check if API key is valid by fetching account info
        print(f"{YELLOW}Fetching account balance...{RESET}")
        balance = await bg.get_balance()
        
        if not balance:
            print(f"{RED}Error: Failed to retrieve account balance. API credentials may be invalid.{RESET}")
            return False
        
        print(f"{GREEN}SUCCESS: API credentials verified!{RESET}")
        print(f"{CYAN}Account Balance:{RESET}")
        
        # Print balance details
        for currency, details in balance.items():
            free = float(details.get('free', 0))
            used = float(details.get('used', 0))
            total = float(details.get('total', 0))
            
            if total > 0:
                print(f"  {currency}: Total={total:.8f}, Free={free:.8f}, Used={used:.8f}")
        
        # Try to fetch positions
        print(f"\n{YELLOW}Fetching positions...{RESET}")
        try:
            positions = await bg.get_positions("BTC/USDT:USDT")
            
            if positions:
                print(f"{GREEN}Active positions found:{RESET}")
                for pos in positions:
                    side = pos.get('side', 'UNKNOWN')
                    size = float(pos.get('contracts', 0))
                    entry = float(pos.get('entryPrice', 0))
                    pnl = float(pos.get('unrealizedPnl', 0))
                    leverage = pos.get('leverage', 'UNKNOWN')
                    
                    print(f"  {side.upper()}: {size} contracts @ ${entry:.2f} | PnL: ${pnl:.2f} | Leverage: {leverage}x")
            else:
                print(f"{YELLOW}No active positions found.{RESET}")
                
        except Exception as e:
            print(f"{RED}Error fetching positions: {str(e)}{RESET}")
        
        return True
        
    except Exception as e:
        print(f"{RED}ERROR: {str(e)}{RESET}")
        print(f"{RED}Traceback: {traceback.format_exc()}{RESET}")
        return False

async def verify_both_sub_accounts():
    """Verify credentials for both long and short sub-accounts."""
    print(f"{CYAN}======================================================{RESET}")
    print(f"{CYAN}= OMEGA BTC AI - Dual Trader Sub-account Verifier    ={RESET}")
    print(f"{CYAN}======================================================{RESET}")
    
    # Get sub-account names
    strategic_sub_account = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
    short_sub_account = "fst_short"  # Default short sub-account name
    
    # Use testnet?
    use_testnet = "BITGET_TESTNET_API_KEY" in os.environ
    
    # Verify strategic (long) sub-account
    print(f"\n{CYAN}Verifying LONG trader sub-account ({strategic_sub_account or 'default'})...{RESET}")
    long_ok = await verify_credentials(use_testnet, strategic_sub_account)
    
    # Verify short sub-account
    print(f"\n{CYAN}Verifying SHORT trader sub-account ({short_sub_account})...{RESET}")
    short_ok = await verify_credentials(use_testnet, short_sub_account)
    
    # Summary
    print(f"\n{CYAN}======================================================{RESET}")
    print(f"{CYAN}= Verification Summary                               ={RESET}")
    print(f"{CYAN}======================================================{RESET}")
    print(f"Long trader sub-account ({strategic_sub_account or 'default'}): {GREEN+'PASS'+RESET if long_ok else RED+'FAIL'+RESET}")
    print(f"Short trader sub-account ({short_sub_account}): {GREEN+'PASS'+RESET if short_ok else RED+'FAIL'+RESET}")
    
    if long_ok and short_ok:
        print(f"\n{GREEN}All sub-accounts verified successfully!{RESET}")
        print(f"{GREEN}Your dual trader setup should work correctly.{RESET}")
        return True
    else:
        print(f"\n{RED}One or more sub-accounts failed verification.{RESET}")
        print(f"{RED}Please check your API credentials and sub-account settings.{RESET}")
        return False

if __name__ == "__main__":
    # Run the verification
    if len(sys.argv) > 1 and sys.argv[1] == "--both":
        asyncio.run(verify_both_sub_accounts())
    else:
        # Default to mainnet if not specified
        use_testnet = "--testnet" in sys.argv
        
        # Get sub-account if specified
        sub_account = ""
        for arg in sys.argv:
            if arg.startswith("--sub-account="):
                sub_account = arg.split("=")[1]
                
        asyncio.run(verify_credentials(use_testnet, sub_account)) 