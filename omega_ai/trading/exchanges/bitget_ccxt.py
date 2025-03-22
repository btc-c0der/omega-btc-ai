"""
BitGet Exchange Integration using CCXT
"""

import ccxt
import ccxt.async_support as ccxt_async
import logging
from typing import Dict, Any, Optional, List, Callable, TypeVar, cast, Literal, Union
from datetime import datetime
import asyncio
import json
import time
from ccxt.base.types import Order, Ticker, Position, OrderSide, OrderType

logger = logging.getLogger(__name__)

T = TypeVar("T")

def to_dict(obj: Any) -> Dict[str, Any]:
    """Convert an object to a dictionary."""
    if hasattr(obj, "__dict__"):
        return dict(obj)
    if isinstance(obj, dict):
        return obj
    return dict(obj)

class BitGetCCXT:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize BitGet exchange interface using CCXT
        
        Args:
            config: Dictionary containing exchange configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize CCXT exchange
        self.exchange = ccxt_async.bitget({
            'apiKey': config.get('api_key'),
            'secret': config.get('api_secret'),
            'password': config.get('api_password'),
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'recvWindow': 60000,
                'testnet': config.get('use_testnet', True),
            }
        })
        
        if config.get('use_testnet', True):
            self.exchange.set_sandbox_mode(True)
        
        # WebSocket related attributes    
        self.ws_callbacks = {}  # Store callbacks for different streams
        self.ws_connected = False
        self.ws_last_message_time = {}
        self.ws_heartbeat_interval = 30  # seconds
            
        logger.info(
            f"Initialized BitGet CCXT with {'TESTNET' if config.get('use_testnet', True) else 'MAINNET'}"
        )
            
    def _format_symbol(self, symbol: Optional[str]) -> str:
        """Format symbol for BitGet API"""
        if not symbol:
            raise ValueError("Symbol is required")
            
        # If the symbol is already formatted (contains a slash), return it as is
        if '/' in symbol:
            return symbol.upper()
            
        # Format BTCUSDT to BTC/USDT:USDT
        if symbol.upper().endswith('USDT'):
            base = symbol[:-4]  # Remove 'USDT' from the end
            return f"{base}/USDT:USDT".upper()
            
        # Format basic symbol to include USDT pairs
        return f"{symbol}/USDT:USDT".upper()
        
    async def create_market_order(
        self,
        symbol: str,
        side: Literal["buy", "sell"],
        amount: float,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a market order
        
        Args:
            symbol: Trading symbol
            side: Order side (buy/sell)
            amount: Order amount
            params: Additional parameters
            
        Returns:
            Dict containing order information
        """
        formatted_symbol = self._format_symbol(symbol)
        
        try:
            order_params = params or {}
            
            order = await self.exchange.create_order(
                symbol=formatted_symbol,
                type="market",
                side=side,
                amount=amount,
                params=order_params
            )
            
            self.logger.info(f"Created market {side} order for {amount} {formatted_symbol}")
            return to_dict(order)
            
        except Exception as e:
            self.logger.error(f"Error creating market order: {e}")
            raise
    
    async def create_order(
        self, 
        symbol: str, 
        type: str, 
        side: str, 
        amount: float, 
        price: Optional[float] = None, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an order of any type
        
        Args:
            symbol: Trading symbol
            type: Order type (market, limit, stop, etc.)
            side: Order side (buy/sell)
            amount: Order amount
            price: Order price (required for limit orders)
            params: Additional parameters
            
        Returns:
            Dict containing order information
        """
        formatted_symbol = self._format_symbol(symbol)
        
        try:
            order_params = params or {}
            
            order = await self.exchange.create_order(
                symbol=formatted_symbol,
                type=type,
                side=side,
                amount=amount,
                price=price,
                params=order_params
            )
            
            self.logger.info(f"Created {type} {side} order for {amount} {formatted_symbol}")
            return to_dict(order)
            
        except Exception as e:
            self.logger.error(f"Error creating order: {e}")
            raise
            
    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch current ticker information for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Dict containing ticker information
        """
        formatted_symbol = self._format_symbol(symbol)
        
        try:
            ticker = await self.exchange.fetch_ticker(formatted_symbol)
            return to_dict(ticker)
        except Exception as e:
            self.logger.error(f"Error fetching ticker: {e}")
            raise
            
    async def fetch_balance(self) -> Dict[str, Any]:
        """
        Fetch current account balance
        
        Returns:
            Dict containing balance information
        """
        try:
            balance = await self.exchange.fetch_balance()
            return to_dict(balance)
        except Exception as e:
            self.logger.error(f"Error fetching balance: {e}")
            raise
            
    async def fetch_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch current positions
        
        Args:
            symbol: Optional trading symbol to filter positions
            
        Returns:
            List of position information
        """
        try:
            formatted_symbol = [self._format_symbol(symbol)] if symbol else None
            positions = await self.exchange.fetch_positions(formatted_symbol)
            return [to_dict(pos) for pos in positions]
        except Exception as e:
            self.logger.error(f"Error fetching positions: {e}")
            raise

    # WebSocket related methods
    def add_ws_callback(self, stream: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Add a callback for a websocket stream
        
        Args:
            stream: Stream name
            callback: Callback function to execute on message
        """
        if stream not in self.ws_callbacks:
            self.ws_callbacks[stream] = []
            
        self.ws_callbacks[stream].append(callback)
        self.logger.info(f"Added callback for {stream} stream")
        
    async def start_websocket(self, symbols: List[str]) -> None:
        """
        Start websocket connection
        
        Args:
            symbols: List of symbols to subscribe to
        """
        self.ws_connected = True
        
        # Initialize last message time
        for stream in self.ws_callbacks:
            self.ws_last_message_time[stream] = time.time()
            
        # Start heartbeat
        asyncio.create_task(self._heartbeat())
        
        self.logger.info(f"Started WebSocket connection for {len(symbols)} symbols")
        
    async def _heartbeat(self) -> None:
        """Send periodic heartbeats to keep connection alive"""
        while self.ws_connected:
            await asyncio.sleep(self.ws_heartbeat_interval)
            
            # Update last message time for heartbeat
            for stream in self.ws_callbacks:
                if time.time() - self.ws_last_message_time.get(stream, 0) > self.ws_heartbeat_interval * 2:
                    self.logger.warning(f"No messages received on {stream} stream for a while")
                    
    async def close_websocket(self) -> None:
        """Close the websocket connection"""
        self.ws_connected = False
        self.logger.info("Closed WebSocket connection")

    # Compatibility methods with older implementations
    async def initialize(self) -> None:
        """Compatibility method - does nothing as initialization occurs in constructor."""
        # No action needed as CCXT is initialized in the constructor
        pass
        
    async def close(self) -> None:
        """Close the exchange connection."""
        await self.exchange.close()
        
    async def get_market_ticker(self, symbol: str) -> Dict[str, Any]:
        """Fetch ticker for a symbol (compatibility method)."""
        return await self.fetch_ticker(symbol)
        
    async def get_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch positions (compatibility method)."""
        return await self.fetch_positions(symbol)
        
    async def get_balance(self) -> Dict[str, Any]:
        """Fetch balance (compatibility method)."""
        return await self.fetch_balance()
        
    async def close_position(self, symbol: str, position: Dict[str, Any]) -> Dict[str, Any]:
        """Close a position using market order."""
        side = "sell" if position.get("side", "").lower() == "long" else "buy"
        amount = float(position.get("contracts", 0))
        
        if amount <= 0:
            self.logger.warning(f"Cannot close position with zero contracts")
            return {}
            
        return await self.create_market_order(
            symbol=symbol,
            side=side,
            amount=amount
        )
        
    async def setup_trading_config(self, symbol: str, leverage: int) -> None:
        """Set up trading configuration including leverage."""
        # Format symbol
        formatted_symbol = self._format_symbol(symbol)
        
        try:
            # Set leverage
            await self.exchange.set_leverage(leverage, formatted_symbol)
            self.logger.info(f"Set leverage to {leverage}x for {formatted_symbol}")
        except Exception as e:
            self.logger.error(f"Error setting up trading config: {e}")
            raise

    async def place_order(self, symbol: str, side: str, amount: float, 
                         price: Optional[float] = None, order_type: str = "market",
                         params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Place an order with the exchange."""
        if order_type.lower() == "market":
            return await self.create_market_order(
                symbol=symbol,
                side=side,
                amount=amount,
                params=params or {}
            )
        else:
            return await self.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                amount=amount,
                price=price,
                params=params or {}
            )

    async def create_market_order(self, symbol: str, side: str, amount: float, 
                                reduce_only: bool = False,
                                params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a market order with optional reduce_only flag."""
        formatted_symbol = self._format_symbol(symbol)
        
        order_params = params or {}
        if reduce_only:
            order_params["reduceOnly"] = True
            
        try:
            order = await self.exchange.create_order(
                symbol=formatted_symbol,
                type="market",
                side=side,
                amount=amount,
                params=order_params
            )
            
            self.logger.info(f"Created market {side} order for {amount} {formatted_symbol}")
            return to_dict(order)
            
        except Exception as e:
            self.logger.error(f"Error creating market order: {e}")
            raise
