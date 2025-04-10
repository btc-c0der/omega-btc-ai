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
OMEGA BTC AI - CCXT Connection Tester
=====================================

This script tests the connection to BitGet using CCXT, validates API credentials,
and displays account information if the connection is successful.

Usage:
  python scripts/test_ccxt_connection.py [--full] [--testnet] [--debug]

Author: OMEGA BTC AI Team
"""

import os
import sys
import json
import asyncio
import argparse
import logging
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path to ensure imports work correctly
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Import CCXT directly for debug purposes
try:
    import ccxt
    import ccxt.async_support as ccxt_async
    HAVE_CCXT_DIRECT = True
except ImportError:
    HAVE_CCXT_DIRECT = False
    logger.warning("CCXT not installed. Install with: pip install ccxt")

# Import the ExchangeClientB0t
try:
    from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t, HAVE_CCXT
except ImportError:
    logger.error("Failed to import ExchangeClientB0t. Make sure you're running from the project root.")
    sys.exit(1)

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_header(title: str, width: int = 80) -> None:
    """Print a formatted header with the given title."""
    print("=" * width)
    print(f"{BOLD}{title.center(width)}{RESET}")
    print("=" * width)

def mask_string(text: str, show_chars: int = 4) -> str:
    """Mask a string, showing only the first and last few characters."""
    if not text:
        return "Not set"
    if len(text) <= show_chars * 2:
        return "*" * len(text)
    return text[:show_chars] + "*" * (len(text) - show_chars * 2) + text[-show_chars:]

def load_environment_variables() -> Dict[str, Any]:
    """Load environment variables from .env files."""
    env_vars = {}
    
    # Try to load from root .env file
    root_env_path = project_root / ".env"
    if root_env_path.exists():
        load_dotenv(root_env_path)
        env_vars["root_env_path"] = str(root_env_path)
        logger.info(f"Loaded environment from root: {root_env_path}")
    
    # Try to load from bot farm .env file
    bot_farm_env_path = project_root / "src" / "omega_bot_farm" / ".env"
    if bot_farm_env_path.exists():
        load_dotenv(bot_farm_env_path)
        env_vars["bot_farm_env_path"] = str(bot_farm_env_path)
        logger.info(f"Loaded environment from bot farm: {bot_farm_env_path}")
    
    # Get API credentials
    env_vars["api_key"] = os.environ.get("BITGET_API_KEY", "")
    env_vars["api_secret"] = os.environ.get("BITGET_SECRET_KEY", "")
    env_vars["api_passphrase"] = os.environ.get("BITGET_PASSPHRASE", "")
    env_vars["use_testnet"] = os.environ.get("USE_TESTNET", "").lower() == "true"
    
    return env_vars

def print_credentials(env_vars: Dict[str, Any], show_full: bool = False) -> None:
    """Print the API credentials."""
    print_header("API CREDENTIALS")
    
    network = "TESTNET" if env_vars.get("use_testnet", False) else "MAINNET"
    print(f"Network: {CYAN}{network}{RESET}")
    
    if show_full:
        print(f"API Key: {CYAN}{env_vars.get('api_key', 'Not set')}{RESET}")
        print(f"API Secret: {CYAN}{env_vars.get('api_secret', 'Not set')}{RESET}")
        print(f"API Passphrase: {CYAN}{env_vars.get('api_passphrase', 'Not set')}{RESET}")
    else:
        print(f"API Key: {CYAN}{mask_string(env_vars.get('api_key', ''))}{RESET}")
        print(f"API Secret: {CYAN}{mask_string(env_vars.get('api_secret', ''))}{RESET}")
        print(f"API Passphrase: {CYAN}{mask_string(env_vars.get('api_passphrase', ''))}{RESET}")
    
    print("\nCredentials loaded from:")
    if "root_env_path" in env_vars:
        print(f"- Root .env: {env_vars['root_env_path']}")
    if "bot_farm_env_path" in env_vars:
        print(f"- Bot Farm .env: {env_vars['bot_farm_env_path']}")
    
    if not show_full:
        print(f"\n{YELLOW}Note: Credentials are masked. Use --full to see full values.{RESET}")
    else:
        print(f"\n{RED}WARNING: Do not share these credentials with anyone!{RESET}")

async def test_ccxt_direct(env_vars: Dict[str, Any], use_testnet: Optional[bool] = None) -> Dict[str, Any]:
    """Test the connection to BitGet using CCXT directly for debugging."""
    if not HAVE_CCXT_DIRECT:
        return {
            "success": False,
            "error": "CCXT library not installed. Install with: pip install ccxt"
        }
    
    # Override testnet setting if specified
    actual_testnet = env_vars.get("use_testnet", False)
    if use_testnet is not None:
        actual_testnet = use_testnet
    
    try:
        # Print available exchanges
        print(f"\n{YELLOW}Available exchanges in CCXT:{RESET}")
        exchanges = sorted(ccxt.exchanges)
        for i, exchange_id in enumerate(exchanges):
            if i % 5 == 0 and i > 0:
                print()
            print(f"{exchange_id}", end=", ")
        print("\n")
        
        if 'bitget' not in exchanges:
            return {
                "success": False,
                "error": "BitGet exchange not found in CCXT",
                "message": "Your CCXT version may not support BitGet"
            }
        
        # Create exchange instance directly
        print(f"{YELLOW}Creating BitGet exchange instance directly...{RESET}")
        options = {
            'defaultType': 'swap',
            'adjustForTimeDifference': True,
            'recvWindow': 60000,
            'testnet': actual_testnet,
            'createMarketBuyOrderRequiresPrice': False
        }
        
        exchange = ccxt_async.bitget({
            'apiKey': env_vars.get("api_key", ""),
            'secret': env_vars.get("api_secret", ""),
            'password': env_vars.get("api_passphrase", ""),
            'enableRateLimit': True,
            'options': options
        })
        
        if actual_testnet:
            print(f"{YELLOW}Setting sandbox mode...{RESET}")
            exchange.set_sandbox_mode(True)
        
        print(f"{YELLOW}Loading markets...{RESET}")
        await exchange.load_markets()
        
        print(f"{YELLOW}Fetching balance...{RESET}")
        balance = await exchange.fetch_balance()
        
        print(f"{YELLOW}Closing exchange...{RESET}")
        await exchange.close()
        
        return {
            "success": True,
            "balance": balance,
            "message": "Direct CCXT connection successful"
        }
        
    except Exception as e:
        print(f"{RED}Error in direct CCXT test: {str(e)}{RESET}")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "message": "Exception occurred during direct CCXT test"
        }

async def test_ccxt_connection(env_vars: Dict[str, Any], use_testnet: Optional[bool] = None, debug: bool = False) -> Dict[str, Any]:
    """Test the connection to BitGet using CCXT."""
    if not HAVE_CCXT:
        return {
            "success": False,
            "error": "CCXT library not installed. Install with: pip install ccxt"
        }
    
    # Override testnet setting if specified
    actual_testnet = env_vars.get("use_testnet", False)
    if use_testnet is not None:
        actual_testnet = use_testnet
    
    if debug:
        print(f"\n{YELLOW}DEBUG: Creating CCXT client with:{RESET}")
        print(f"  Exchange ID: bitget")
        print(f"  API Key: {mask_string(env_vars.get('api_key', ''))}")
        print(f"  API Secret: {mask_string(env_vars.get('api_secret', ''))}")
        print(f"  API Passphrase: {mask_string(env_vars.get('api_passphrase', ''))}")
        print(f"  Use Testnet: {actual_testnet}")
    
    # Create CCXT client
    try:
        if debug:
            print(f"\n{YELLOW}DEBUG: Creating ExchangeClientB0t instance...{RESET}")
            
        client = ExchangeClientB0t(
            exchange_id="bitget",
            api_key=env_vars.get("api_key", ""),
            api_secret=env_vars.get("api_secret", ""),
            api_password=env_vars.get("api_passphrase", ""),
            use_testnet=actual_testnet
        )
        
        if debug:
            print(f"{YELLOW}DEBUG: ExchangeClientB0t created. Exchange initialized: {client.exchange is not None}{RESET}")
            
        # Initialize the client (load markets)
        if debug:
            print(f"{YELLOW}DEBUG: Initializing client...{RESET}")
        await client.initialize()
        
        # Check balance to verify API credentials
        if debug:
            print(f"{YELLOW}DEBUG: Fetching balance...{RESET}")
        balance = await client.fetch_balance()
        if "error" in balance:
            if debug:
                print(f"{RED}DEBUG: Error fetching balance: {balance['error']}{RESET}")
            return {
                "success": False,
                "error": balance["error"],
                "message": "Failed to fetch balance"
            }
        
        # Fetch positions
        if debug:
            print(f"{YELLOW}DEBUG: Fetching positions...{RESET}")
        positions = await client.fetch_positions()
        positions_without_error = [p for p in positions if "error" not in p]
        
        # Fetch ticker for BTC
        if debug:
            print(f"{YELLOW}DEBUG: Fetching ticker...{RESET}")
        ticker = await client.fetch_ticker("BTCUSDT")
        if "error" in ticker:
            btc_price = None
            if debug:
                print(f"{RED}DEBUG: Error fetching ticker: {ticker['error']}{RESET}")
        else:
            btc_price = ticker.get("last")
        
        # Close the client
        if debug:
            print(f"{YELLOW}DEBUG: Closing client...{RESET}")
        await client.close()
        
        return {
            "success": True,
            "balance": balance,
            "positions": positions_without_error,
            "btc_price": btc_price
        }
    except Exception as e:
        if debug:
            print(f"{RED}DEBUG: Exception during CCXT test: {str(e)}{RESET}")
            traceback.print_exc()
        if 'client' in locals():
            await client.close()
        return {
            "success": False,
            "error": str(e),
            "message": "Exception occurred while testing connection"
        }

def print_connection_result(result: Dict[str, Any]) -> None:
    """Print the result of the connection test."""
    if result.get("success", False):
        print_header(f"{GREEN}CONNECTION SUCCESSFUL{RESET}")
        
        # Print BTC price if available
        if result.get("btc_price"):
            print(f"BTC Price: {CYAN}${result['btc_price']:,.2f}{RESET}\n")
        
        # Print balance summary
        if "balance" in result:
            balance = result["balance"]
            print_header("ACCOUNT BALANCE")
            
            if isinstance(balance, dict) and "info" in balance:
                # Extract USDT balance if available
                usdt_balance = balance.get("USDT", {})
                if usdt_balance:
                    print(f"USDT Available: {GREEN}{usdt_balance.get('free', 0):,.2f}{RESET}")
                    print(f"USDT Used: {YELLOW}{usdt_balance.get('used', 0):,.2f}{RESET}")
                    print(f"USDT Total: {CYAN}{usdt_balance.get('total', 0):,.2f}{RESET}")
                
                # Show other currencies if available
                other_currencies = [currency for currency in balance if currency not in ['USDT', 'info', 'timestamp', 'datetime']]
                if other_currencies:
                    print("\nOther Currencies:")
                    for currency in sorted(other_currencies):
                        if balance[currency].get('total', 0) > 0:
                            print(f"{currency}: {CYAN}{balance[currency].get('total', 0):,.8f}{RESET}")
            else:
                print(json.dumps(balance, indent=2))
        
        # Print position summary
        if "positions" in result and result["positions"]:
            print_header("OPEN POSITIONS")
            
            for position in result["positions"]:
                symbol = position.get("symbol", "Unknown")
                side = position.get("side", "Unknown")
                contracts = position.get("contracts", 0)
                entry_price = position.get("entryPrice", 0)
                leverage = position.get("leverage", 1)
                
                if contracts > 0:
                    side_color = GREEN if side.lower() == "long" else RED
                    print(f"Symbol: {CYAN}{symbol}{RESET}")
                    print(f"Side: {side_color}{side.upper()}{RESET}")
                    print(f"Size: {contracts} contracts")
                    print(f"Entry Price: ${entry_price:,.2f}")
                    print(f"Leverage: {leverage}x")
                    print(f"Notional Value: ${contracts * entry_price:,.2f}")
                    print("-" * 40)
            
            if not any(position.get("contracts", 0) > 0 for position in result["positions"]):
                print(f"{YELLOW}No open positions{RESET}")
        else:
            print(f"\n{YELLOW}No position data available{RESET}")
    else:
        print_header(f"{RED}CONNECTION FAILED{RESET}")
        print(f"Error: {RED}{result.get('error', 'Unknown error')}{RESET}")
        print(f"Message: {YELLOW}{result.get('message', 'No additional information')}{RESET}")
        
        print(f"\n{YELLOW}Troubleshooting Tips:{RESET}")
        print("1. Check that your API key, secret, and passphrase are correct")
        print("2. Verify you're using the correct network (TESTNET or MAINNET)")
        print("3. Ensure your API key has the necessary permissions")
        print("4. Check your internet connection")
        print(f"5. If using testnet, make sure you have a testnet account at {CYAN}https://www.bitget.com/en/testnet/{RESET}")
        print("6. Run with --debug flag for more detailed error information")

async def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - CCXT Connection Tester")
    parser.add_argument("--full", action="store_true", help="Show full API credentials (use with caution)")
    parser.add_argument("--testnet", action="store_true", help="Force use of BitGet testnet")
    parser.add_argument("--mainnet", action="store_true", help="Force use of BitGet mainnet")
    parser.add_argument("--debug", action="store_true", help="Show detailed debug information")
    parser.add_argument("--direct", action="store_true", help="Test using CCXT directly (for debugging)")
    args = parser.parse_args()
    
    if args.testnet and args.mainnet:
        print(f"{RED}Error: Cannot specify both --testnet and --mainnet{RESET}")
        sys.exit(1)
    
    # Determine testnet mode
    use_testnet: Optional[bool] = None
    if args.testnet:
        use_testnet = True
    elif args.mainnet:
        use_testnet = False
    
    # Load environment variables
    env_vars = load_environment_variables()
    
    # Show banner
    print("\n" + "=" * 80)
    print(f"{BOLD}OMEGA BTC AI - CCXT Connection Tester{RESET}")
    print("=" * 80 + "\n")
    
    # Show API credentials
    print_credentials(env_vars, args.full)
    
    # Test connection
    print("\nTesting connection to BitGet...")
    
    if args.debug:
        # Set logging level to DEBUG
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("ccxt_b0t").setLevel(logging.DEBUG)
        
        print(f"\n{YELLOW}=== DEBUG MODE ENABLED ==={RESET}")
        print(f"CCXT Version: {ccxt.__version__} (from {ccxt.__file__})")
        print(f"Python Version: {sys.version}")
        print(f"Working Directory: {os.getcwd()}")
    
    if args.direct:
        result = await test_ccxt_direct(env_vars, use_testnet)
    else:
        result = await test_ccxt_connection(env_vars, use_testnet, args.debug)
    
    # Show results
    print_connection_result(result)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation canceled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        traceback.print_exc()
        sys.exit(1) 