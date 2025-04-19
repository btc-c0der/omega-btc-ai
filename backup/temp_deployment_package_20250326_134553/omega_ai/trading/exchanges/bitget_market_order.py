
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
OMEGA BTC AI - BitGet Market Order Executor
===========================================

This script provides a simple way to execute market orders on BitGet exchange.
It can be used to quickly place buy or sell orders for testing or manual trading.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import argparse
import os
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class BitGetOrderExecutor:
    """Simple utility for executing market orders on BitGet."""
    
    def __init__(self, 
                api_key: str = "", 
                secret_key: str = "", 
                passphrase: str = "",
                use_testnet: bool = True,
                sub_account: str = ""):
        """
        Initialize the BitGet order executor.
        
        Args:
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_testnet: Whether to use testnet (default: True)
            sub_account: Sub-account name to use for trading (optional)
        """
        # Look for API credentials in environment variables if not provided
        self.api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = secret_key or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Set sub-account if provided, or try to get from environment
        self.sub_account = sub_account or os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
        
        # Initialize CCXT instance
        self.exchange = BitGetCCXT(
            api_key=self.api_key,
            secret_key=self.secret_key,
            passphrase=self.passphrase,
            use_testnet=use_testnet,
            sub_account=self.sub_account
        )
        
        # Log API credentials status
        if not self.api_key or not self.secret_key or not self.passphrase:
            logger.warning(f"{YELLOW}One or more API credentials are missing. API authentication will fail.{RESET}")
        else:
            logger.info(f"{GREEN}API credentials loaded successfully.{RESET}")
            logger.info(f"{CYAN}Using {'TESTNET' if use_testnet else 'MAINNET'} environment.{RESET}")
            
        if self.sub_account:
            logger.info(f"{CYAN}Using sub-account: {self.sub_account}{RESET}")
    
    async def initialize(self):
        """Initialize the exchange connection."""
        await self.exchange.initialize()
    
    async def place_market_order(self, 
                          symbol: str = "BTCUSDT", 
                          size: str = "0.001",
                          side: str = "buy") -> Dict[str, Any]:
        """
        Place a market order on BitGet.
        
        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            size: Order size
            side: Order side ("buy" or "sell")
            
        Returns:
            Response from the BitGet API
        """
        try:
            # Format symbol for CCXT
            formatted_symbol = f"{symbol}/USDT:USDT"
            
            # Convert size to float
            amount = float(size)
            
            # Place the order
            order = await self.exchange.place_order(
                symbol=formatted_symbol,
                side=side,
                amount=amount,
                order_type="market"
            )
            
            logger.info(f"{GREEN}Order placed successfully!{RESET}")
            logger.info(f"{GREEN}Order ID: {order.get('id')}{RESET}")
            
            return order
            
        except Exception as e:
            logger.error(f"{RED}Error placing order: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return {"error": str(e)}
    
    async def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance from BitGet.
        
        Returns:
            Account balance information
        """
        try:
            balance = await self.exchange.get_balance()
            
            # Format and display balance information
            if 'USDT' in balance:
                usdt_balance = balance['USDT']
                logger.info(f"{CYAN}USDT Balance:{RESET}")
                logger.info(f"{CYAN}  Available: {usdt_balance.get('free', '0')}{RESET}")
                logger.info(f"{CYAN}  Total: {usdt_balance.get('total', '0')}{RESET}")
            
            return balance
            
        except Exception as e:
            logger.error(f"{RED}Error retrieving account balance: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return {"error": str(e)}
    
    async def get_positions(self, symbol: str = "BTCUSDT") -> List[Dict[str, Any]]:
        """
        Get current positions for a symbol.
        
        Args:
            symbol: Trading symbol (e.g., "BTCUSDT")
            
        Returns:
            List of current positions information
        """
        try:
            # Format symbol for CCXT
            formatted_symbol = f"{symbol}/USDT:USDT"
            
            positions = await self.exchange.get_positions(formatted_symbol)
            
            # Format and display position information
            for position in positions:
                if position['symbol'] == formatted_symbol:
                    side = position.get('side', 'UNKNOWN')
                    size = position.get('contracts', '0')
                    avg_price = position.get('entryPrice', '0')
                    unrealized_pnl = position.get('unrealizedPnl', '0')
                    
                    logger.info(f"{CYAN}Position: {side} {size} {symbol} @ {avg_price}{RESET}")
                    logger.info(f"{CYAN}  Unrealized PnL: {unrealized_pnl}{RESET}")
            
            return positions
            
        except Exception as e:
            logger.error(f"{RED}Error retrieving positions: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return []
    
    async def close(self):
        """Close the exchange connection."""
        await self.exchange.close()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='BitGet Market Order Executor')
    
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--size', type=str, default='0.001',
                      help='Order size (default: 0.001)')
    parser.add_argument('--side', type=str, choices=['buy', 'sell'], default='buy',
                      help='Order side: buy or sell (default: buy)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default behavior)')
    parser.add_argument('--mainnet', action='store_true',
                      help='Use mainnet (overrides testnet)')
    parser.add_argument('--api-key', type=str, default='',
                      help='BitGet API key (optional, can use environment variables)')
    parser.add_argument('--secret-key', type=str, default='',
                      help='BitGet secret key (optional, can use environment variables)')
    parser.add_argument('--passphrase', type=str, default='',
                      help='BitGet API passphrase (optional, can use environment variables)')
    parser.add_argument('--check-balance', action='store_true',
                      help='Check account balance before placing order')
    parser.add_argument('--check-positions', action='store_true',
                      help='Check current positions after placing order')
    parser.add_argument('--dry-run', action='store_true',
                      help='Simulate order without actually placing it')
    parser.add_argument('--sub-account', type=str, default='',
                      help='Sub-account name to use for trading (e.g., strategic_trader)')
    
    return parser.parse_args()

async def main():
    """Main entry point for the script."""
    # Load environment variables from .env file
    try:
        # Try to load from project root .env
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
        env_path = os.path.join(project_root, '.env')
        
        if os.path.exists(env_path):
            load_dotenv(env_path)
            logger.info(f"{GREEN}Loaded environment from {env_path}{RESET}")
            
            # Log which credentials were found (safely)
            if 'BITGET_API_KEY' in os.environ:
                api_key = os.environ['BITGET_API_KEY']
                logger.info(f"{CYAN}Found BITGET_API_KEY: {api_key[:5]}...{api_key[-3:] if len(api_key) > 5 else ''}{RESET}")
            if 'BITGET_SECRET_KEY' in os.environ:
                logger.info(f"{CYAN}Found BITGET_SECRET_KEY with length: {len(os.environ['BITGET_SECRET_KEY'])}{RESET}")
            if 'BITGET_PASSPHRASE' in os.environ:
                logger.info(f"{CYAN}Found BITGET_PASSPHRASE with length: {len(os.environ['BITGET_PASSPHRASE'])}{RESET}")
                
            # Check for testnet credentials too
            if 'BITGET_TESTNET_API_KEY' in os.environ:
                testnet_api_key = os.environ['BITGET_TESTNET_API_KEY']
                logger.info(f"{CYAN}Found BITGET_TESTNET_API_KEY: {testnet_api_key[:5]}...{testnet_api_key[-3:] if len(testnet_api_key) > 5 else ''}{RESET}")
            if 'BITGET_TESTNET_SECRET_KEY' in os.environ:
                logger.info(f"{CYAN}Found BITGET_TESTNET_SECRET_KEY with length: {len(os.environ['BITGET_TESTNET_SECRET_KEY'])}{RESET}")
            if 'BITGET_TESTNET_PASSPHRASE' in os.environ:
                logger.info(f"{CYAN}Found BITGET_TESTNET_PASSPHRASE with length: {len(os.environ['BITGET_TESTNET_PASSPHRASE'])}{RESET}")
                
            # Check for sub-account config
            if 'STRATEGIC_SUB_ACCOUNT_NAME' in os.environ:
                logger.info(f"{CYAN}Found STRATEGIC_SUB_ACCOUNT_NAME: {os.environ['STRATEGIC_SUB_ACCOUNT_NAME']}{RESET}")
        else:
            logger.warning(f"{YELLOW}No .env file found at {env_path}, using system environment variables{RESET}")
    except Exception as e:
        logger.error(f"{RED}Error loading .env file: {str(e)}{RESET}")
    
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    # Create order executor
    executor = BitGetOrderExecutor(
        api_key=args.api_key,
        secret_key=args.secret_key,
        passphrase=args.passphrase,
        use_testnet=use_testnet,
        sub_account=args.sub_account
    )
    
    try:
        # Initialize the exchange
        await executor.initialize()
        
        # Check balance if requested
        if args.check_balance:
            print(f"{BLUE}Checking account balance...{RESET}")
            balance_response = await executor.get_account_balance()
            print(f"{CYAN}Balance response: {balance_response}{RESET}")
        
        # Place order unless dry run
        if not args.dry_run:
            print(f"{YELLOW}Placing {'BUY' if args.side == 'buy' else 'SELL'} order for {args.size} {args.symbol}...{RESET}")
            order_response = await executor.place_market_order(
                symbol=args.symbol,
                size=args.size,
                side=args.side
            )
            print(f"{MAGENTA}Order response: {order_response}{RESET}")
        else:
            print(f"{YELLOW}DRY RUN: Would place {'BUY' if args.side == 'buy' else 'SELL'} order for {args.size} {args.symbol}{RESET}")
        
        # Check positions if requested
        if args.check_positions:
            print(f"{BLUE}Checking positions for {args.symbol}...{RESET}")
            positions_response = await executor.get_positions(args.symbol)
            print(f"{CYAN}Positions response: {positions_response}{RESET}")
            
    except Exception as e:
        logger.error(f"{RED}Error in main: {str(e)}{RESET}")
    finally:
        await executor.close()

if __name__ == "__main__":
    print(f"{GREEN}BitGet Market Order Executor{RESET}")
    print(f"{CYAN}Use --help for available options{RESET}")
    asyncio.run(main()) 