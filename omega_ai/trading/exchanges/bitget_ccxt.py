"""
OMEGA BTC AI - BitGet CCXT Implementation
=======================================

This module implements CCXT-based trading functionality for BitGet,
providing a robust and standardized interface for market operations.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import ccxt.async_support as ccxt_async
import ccxt.pro as ccxt_pro
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import traceback
from uuid import uuid4

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

class BitGetCCXT:
    """CCXT-based implementation for BitGet trading."""
    
    def __init__(self, 
                 api_key: str = "", 
                 secret_key: str = "", 
                 passphrase: str = "",
                 use_testnet: bool = True,
                 sub_account: str = ""):
        """
        Initialize the BitGet CCXT implementation.
        
        Args:
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            use_testnet: Whether to use testnet (default: True)
            sub_account: Sub-account name to use for trading (optional)
        """
        self.use_testnet = use_testnet
        self.sub_account = sub_account
        
        # Initialize CCXT instances
        self.exchange = getattr(ccxt_async, 'bitget')({
            'apiKey': api_key,
            'secret': secret_key,
            'password': passphrase,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'recvWindow': 60000,
                'testnet': use_testnet
            }
        })
        
        # Initialize Pro version for websocket support
        self.exchange_pro = getattr(ccxt_pro, 'bitget')({
            'apiKey': api_key,
            'secret': secret_key,
            'password': passphrase,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'recvWindow': 60000,
                'testnet': use_testnet
            }
        })
        
        # Position side mapping
        self.position_side_map = {
            "buy": {"open": "long", "close": "short"},
            "sell": {"open": "short", "close": "long"}
        }
        
        logger.info(f"{GREEN}Initialized BitGet CCXT with {'TESTNET' if use_testnet else 'MAINNET'}{RESET}")
        
    def _format_symbol(self, symbol: str) -> str:
        """Format symbol for BitGet futures trading."""
        if not symbol:
            logger.warning(f"{YELLOW}Empty or None symbol provided, using default BTCUSDT{RESET}")
            return "BTC/USDT:USDT"
            
        # Remove any existing formatting
        base = symbol.replace('USDT', '').replace('/', '').replace(':', '')
        # Format for BitGet futures: BTC/USDT:USDT
        formatted = f"{base}/USDT:USDT"
        logger.debug(f"{CYAN}Formatted symbol: {formatted} (from {symbol}){RESET}")
        return formatted
        
    async def initialize(self):
        """Initialize the exchange connection and load markets."""
        try:
            await self.exchange.load_markets()
            logger.info(f"{GREEN}Markets loaded successfully{RESET}")
            
            # Get current position mode
            try:
                mode = await self.exchange.fetch_position_mode()
                self.is_hedge_mode = mode.get('hedged', False)  # Default to one-way mode if can't determine
                logger.info(f"{GREEN}Current position mode: {'hedge' if self.is_hedge_mode else 'one-way'}{RESET}")
            except Exception as e:
                logger.warning(f"{YELLOW}Could not fetch position mode: {str(e)}{RESET}")
                logger.warning(f"{YELLOW}Will proceed with one-way mode{RESET}")
                self.is_hedge_mode = False
            
        except Exception as e:
            logger.error(f"{RED}Error initializing exchange: {str(e)}{RESET}")
            raise
            
    async def set_hedge_mode(self):
        """Set up hedge mode for the account."""
        try:
            result = await self.exchange.set_position_mode(True)
            logger.info(f"{GREEN}Hedge mode set successfully: {result}{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error setting hedge mode: {str(e)}{RESET}")
            raise
            
    async def setup_trading_config(self, symbol: str, leverage: int = 2):
        """Set up trading configuration for a symbol."""
        try:
            formatted_symbol = self._format_symbol(symbol)
            
            # First check if we have enough margin
            balance = await self.get_balance()
            usdt_balance = float(balance.get('USDT', {}).get('free', 0))
            
            if usdt_balance < 5:  # Minimum margin requirement for most futures
                logger.warning(f"{YELLOW}Insufficient margin. Current balance: {usdt_balance} USDT{RESET}")
                logger.warning(f"{YELLOW}Please ensure you have at least 5 USDT available{RESET}")
                return
            
            # Set leverage for both long and short positions
            try:
                await self.exchange.set_leverage(leverage, symbol=formatted_symbol, params={"holdSide": "long"})
                await self.exchange.set_leverage(leverage, symbol=formatted_symbol, params={"holdSide": "short"})
                logger.info(f"{GREEN}Leverage set to {leverage}x for {formatted_symbol} (both sides){RESET}")
            except Exception as e:
                if "40893" in str(e):  # Insufficient margin error
                    logger.warning(f"{YELLOW}Warning: Could not set leverage due to insufficient margin{RESET}")
                    logger.warning(f"{YELLOW}This might be because you have open positions or insufficient balance{RESET}")
                else:
                    raise
            
            # Set cross margin mode
            try:
                await self.exchange.set_margin_mode("cross", symbol=formatted_symbol)
                logger.info(f"{GREEN}Cross margin mode set for {formatted_symbol}{RESET}")
            except Exception as e:
                logger.warning(f"{YELLOW}Warning: Could not set margin mode: {str(e)}{RESET}")
                logger.warning(f"{YELLOW}This might be because you're already in the desired margin mode{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error setting up trading config: {str(e)}{RESET}")
            raise
            
    async def get_market_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get current market ticker for a symbol."""
        try:
            formatted_symbol = self._format_symbol(symbol)
            ticker = await self.exchange.fetch_ticker(formatted_symbol)
            return ticker
        except Exception as e:
            logger.error(f"{RED}Error fetching ticker for {symbol}: {str(e)}{RESET}")
            raise
            
    async def get_positions(self, symbol: str = "BTC/USDT:USDT") -> List[Dict[str, Any]]:
        """
        Get current positions for a symbol.
        
        Args:
            symbol: Trading symbol (e.g., "BTC/USDT:USDT")
            
        Returns:
            List of current positions information
        """
        try:
            # Ensure symbol is properly formatted
            formatted_symbol = self._format_symbol(symbol)
            logger.debug(f"{CYAN}Fetching positions for symbol: {formatted_symbol}{RESET}")
            
            # Fetch all positions first
            all_positions = await self.exchange.fetch_positions()
            
            # Filter positions for the requested symbol
            filtered_positions = []
            for position in all_positions:
                if position and position.get('symbol') == formatted_symbol:
                    filtered_positions.append(position)
            
            if not filtered_positions:
                logger.debug(f"{YELLOW}No positions found for symbol {formatted_symbol}{RESET}")
            
            return filtered_positions
            
        except Exception as e:
            logger.error(f"{RED}Error fetching positions: {str(e)}{RESET}")
            logger.error(f"{RED}Exception type: {type(e).__name__}{RESET}")
            logger.error(f"{RED}Exception args: {e.args}{RESET}")
            return []
            
    async def get_balance(self) -> Dict[str, Any]:
        """Get account balance."""
        try:
            balance = await self.exchange.fetch_balance()
            return balance
        except Exception as e:
            logger.error(f"{RED}Error fetching balance: {str(e)}{RESET}")
            raise
            
    async def place_order(self, 
                         symbol: str,
                         side: str,
                         amount: float,
                         price: Optional[float] = None,
                         order_type: str = "market",
                         reduce_only: bool = False) -> Dict[str, Any]:
        """
        Place an order on BitGet.
        
        Args:
            symbol: Trading symbol (e.g., "BTC/USDT:USDT")
            side: Order side ("buy" or "sell")
            amount: Order amount
            price: Order price (optional, required for limit orders)
            order_type: Order type ("market" or "limit")
            reduce_only: Whether this is a reduce-only order
            
        Returns:
            Order response from the exchange
        """
        try:
            # Format symbol
            formatted_symbol = self._format_symbol(symbol)
            
            # Prepare order parameters
            params = {
                "timeInForce": "GTC" if order_type == "limit" else "IOC",
                "reduceOnly": reduce_only,
                "positionSide": "long" if side == "buy" else "short"  # Add position side for unilateral mode
            }
            
            # Add sub-account if specified
            if self.sub_account:
                params["subAccount"] = self.sub_account
                
            # Place the order
            order = await self.exchange.create_order(
                symbol=formatted_symbol,
                type=order_type,
                side=side,
                amount=amount,
                price=price,
                params=params
            )
            
            logger.info(f"{GREEN}Order placed successfully: {order}{RESET}")
            return order
            
        except Exception as e:
            logger.error(f"{RED}Error placing order: {str(e)}{RESET}")
            raise
            
    async def close_position(self, symbol: str, position: Dict[str, Any]) -> Dict[str, Any]:
        """
        Close an existing position.
        
        Args:
            symbol: Trading symbol
            position: Position information from get_positions()
            
        Returns:
            Order response from the exchange
        """
        try:
            formatted_symbol = self._format_symbol(symbol)
            side = "sell" if position.get('side') == "long" else "buy"
            amount = abs(float(position.get('contracts', 0)))
            
            if amount > 0:
                return await self.place_order(
                    symbol=formatted_symbol,
                    side=side,
                    amount=amount,
                    order_type="market",
                    reduce_only=True
                )
            else:
                logger.info(f"{YELLOW}No position to close{RESET}")
                return {}
                
        except Exception as e:
            logger.error(f"{RED}Error closing position: {str(e)}{RESET}")
            raise
            
    async def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Cancel an existing order."""
        try:
            formatted_symbol = self._format_symbol(symbol)
            result = await self.exchange.cancel_order(order_id, formatted_symbol)
            logger.info(f"{GREEN}Order cancelled successfully: {result}{RESET}")
            return result
        except Exception as e:
            logger.error(f"{RED}Error cancelling order: {str(e)}{RESET}")
            raise
            
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all open orders."""
        try:
            formatted_symbol = self._format_symbol(symbol) if symbol else None
            orders = await self.exchange.fetch_open_orders(formatted_symbol)
            return orders
        except Exception as e:
            logger.error(f"{RED}Error fetching open orders: {str(e)}{RESET}")
            raise
            
    async def watch_orders(self):
        """Watch orders using websocket connection."""
        try:
            while True:
                orders = await self.exchange_pro.watch_orders()
                for order in orders:
                    # Process order update
                    logger.info(f"{CYAN}Order update received: {order}{RESET}")
                    # Add your order processing logic here
                    
        except Exception as e:
            logger.error(f"{RED}Error watching orders: {str(e)}{RESET}")
            raise
            
    async def close(self):
        """Close the exchange connection."""
        try:
            await self.exchange.close()
            await self.exchange_pro.close()
            logger.info(f"{GREEN}Exchange connections closed{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error closing exchange connections: {str(e)}{RESET}")
            raise
            
    def __del__(self):
        """Cleanup when the object is destroyed."""
        try:
            asyncio.create_task(self.close())
        except Exception as e:
            logger.error(f"{RED}Error during cleanup: {str(e)}{RESET}")

async def main():
    """Example usage of the BitGetCCXT class."""
    # Initialize with your API credentials
    exchange = BitGetCCXT(
        api_key="your_api_key",
        secret_key="your_secret_key",
        passphrase="your_passphrase",
        use_testnet=True
    )
    
    try:
        # Initialize the exchange
        await exchange.initialize()
        
        # Get market data
        ticker = await exchange.get_market_ticker("BTC/USDT:USDT")
        print(f"BTC/USDT Ticker: {ticker}")
        
        # Get positions
        positions = await exchange.get_positions()
        print(f"Current positions: {positions}")
        
        # Get balance
        balance = await exchange.get_balance()
        print(f"Account balance: {balance}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await exchange.close()

if __name__ == "__main__":
    asyncio.run(main()) 