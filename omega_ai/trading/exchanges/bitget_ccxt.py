"""
BitGet Exchange Integration using CCXT
"""

import asyncio
import json
import logging
import time
import os
from typing import Dict, List, Optional, Any, Union, TypeVar, Callable

# Use async version of ccxt
import ccxt.async_support as ccxt_async
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
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the BitGet CCXT client."""
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        
        # Get API credentials from config or environment variables
        api_key = self.config.get('api_key', os.getenv('BITGET_API_KEY', ''))
        api_secret = self.config.get('api_secret', os.getenv('BITGET_SECRET_KEY', ''))
        api_password = self.config.get('api_password', os.getenv('BITGET_PASSPHRASE', ''))
        
        # Enable testnet only if explicitly specified
        use_testnet = self.config.get('use_testnet', False)
        if 'options' in self.config:
            use_testnet = self.config['options'].get('testnet', use_testnet)
        
        # Create CCXT exchange object
        self.exchange = ccxt_async.bitget({
            'apiKey': api_key,
            'secret': api_secret,
            'password': api_password,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'testnet': use_testnet
            }
        })
        
        # Set URL to testnet if specified
        if use_testnet:
            self.exchange.urls['api'] = 'https://api.bitget-testnet.com'
            self.logger.info("Initialized BitGet CCXT with TESTNET")
        else:
            self.logger.info("Initialized BitGet CCXT with MAINNET")
        
        # WebSocket related attributes    
        self.ws_callbacks = {}  # Store callbacks for different streams
        self.ws_connected = False
        self.ws_last_message_time = {}
        self.ws_heartbeat_interval = 30  # seconds
            
    async def load_markets(self, reload: bool = False) -> Dict[str, Any]:
        """Load exchange markets."""
        try:
            return await self.exchange.load_markets(reload=reload)
        except Exception as e:
            self.logger.error(f"Error loading markets: {str(e)}")
            raise
            
    async def fetch_ticker(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch current ticker for a symbol."""
        try:
            formatted_symbol = self._format_symbol(symbol)
            self.logger.info(f"Fetching ticker for formatted symbol: {formatted_symbol}")
            return await self.exchange.fetch_ticker(formatted_symbol)
        except Exception as e:
            self.logger.error(f"Error fetching ticker: {str(e)}")
            return None
            
    async def fetch_ohlcv(self, 
                         symbol: str, 
                         timeframe: str = '1h',
                         since: Optional[int] = None,
                         limit: Optional[int] = None) -> Optional[List[List[float]]]:
        """
        Fetch OHLCV candlestick data.
        
        Args:
            symbol: Trading symbol
            timeframe: Candlestick timeframe
            since: Timestamp to start from
            limit: Number of candles to fetch
            
        Returns:
            List of OHLCV candles [timestamp, open, high, low, close, volume]
        """
        try:
            return await self.exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                since=since,
                limit=limit
            )
        except Exception as e:
            self.logger.error(f"Error fetching OHLCV data: {str(e)}")
            return None
            
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
        """Close exchange connection."""
        await self.exchange.close()
        
    async def get_market_ticker(self, symbol: str) -> Dict[str, Any]:
        """Fetch ticker for a symbol (compatibility method)."""
        return await self.fetch_ticker(symbol)
        
    async def get_market_candles(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> List[List[float]]:
        """
        Fetch candlestick data for a symbol (compatibility method).
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe interval (e.g. "1m", "5m", "1h", "4h", "1d")
            limit: Number of candles to fetch
            
        Returns:
            List of OHLCV candles in format [timestamp, open, high, low, close, volume]
        """
        try:
            formatted_symbol = self._format_symbol(symbol)
            candles = await self.exchange.fetch_ohlcv(formatted_symbol, timeframe=timeframe, limit=limit)
            return candles
        except Exception as e:
            self.logger.error(f"Error fetching candles: {e}")
            return []
        
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

    def _format_symbol(self, symbol: str) -> str:
        """Format symbol for BitGet API."""
        if not symbol:
            return "BTC-USDT-UMCBL"  # Default to BTC
        
        # If the symbol has BitGet format already (contains -UMCBL), return it as is
        if "-UMCBL" in symbol:
            return symbol
        
        # Remove any formatting characters
        base = symbol.upper().replace("/", "").replace(":", "").replace("_", "-")
        
        # If it ends with -UMCBL or -UMCBL, return as is
        if base.endswith("-UMCBL") or base.endswith("-UMCBL"):
            return base
        
        # If it has USDT in it already
        if "USDT" in base:
            # Replace USDT with -USDT-UMCBL
            return base.replace("USDT", "-USDT-UMCBL")
        
        # Default case: append -USDT-UMCBL
        return f"{base}-USDT-UMCBL"
