#!/usr/bin/env python3

"""
CCXT Exchange Integration for Omega Bot Farm

This module provides a wrapper around the CCXT library for standardized
exchange interactions in the containerized bot environment.
"""

import logging
import time
import asyncio
from typing import Dict, List, Optional, Any, Callable, Union, Literal, TypeVar
import os
from dotenv import load_dotenv

# Try to load environment variables from the root .env file
try:
    # First try loading from the project root
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    env_path = os.path.join(root_dir, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logging.info(f"Loaded environment variables from {env_path}")
    else:
        logging.warning(f"No .env file found at {env_path}")
except Exception as e:
    logging.warning(f"Failed to load environment variables: {e}")

# Import CCXT with error handling for containerized environment
try:
    import ccxt
    import ccxt.async_support as ccxt_async
    from ccxt.base.types import Order, Ticker, Position, OrderSide, OrderType
    HAVE_CCXT = True
except ImportError:
    HAVE_CCXT = False
    logging.warning("CCXT library not installed. Exchange functionality will be limited.")
    logging.warning("Install CCXT with: pip install ccxt")

# Configure logging
logger = logging.getLogger("ccxt_b0t")

T = TypeVar("T")

def to_dict(obj: Any) -> Dict[str, Any]:
    """Convert an object to a dictionary."""
    if hasattr(obj, "__dict__"):
        return dict(obj.__dict__)
    if isinstance(obj, dict):
        return obj
    # For CCXT types that implement a to_dict method
    if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
        return obj.to_dict()
    return {}

class ExchangeClientB0t:
    """Base exchange client for bot farm operations."""
    
    def __init__(self, exchange_id: str = None, api_key: str = None, 
                 api_secret: str = None, api_password: str = None, 
                 use_testnet: bool = None, symbol: str = None):
        """
        Initialize exchange client with containerized environment support.
        
        Args:
            exchange_id: CCXT exchange ID (e.g., 'bitget', 'binance')
            api_key: API key (can be provided via environment variable)
            api_secret: API secret (can be provided via environment variable)
            api_password: API password/passphrase (can be provided via environment variable)
            use_testnet: Whether to use testnet (default from environment or True)
            symbol: Trading symbol (default from environment or "BTCUSDT")
        """
        if not HAVE_CCXT:
            logger.error("CCXT library not installed. Exchange functionality will be limited.")
            self.exchange = None
            self.exchange_id = exchange_id or "bitget"
            return
        
        # Default to BitGet unless specified
        self.exchange_id = exchange_id or "bitget"
        
        # Allow configuration from environment for containerized deployment
        # Use BitGet-specific environment variables if exchange is bitget
        if self.exchange_id.lower() == "bitget":
            # BitGet credentials from .env
            api_key = api_key or os.environ.get("BITGET_API_KEY")
            api_secret = api_secret or os.environ.get("BITGET_SECRET_KEY")
            api_password = api_password or os.environ.get("BITGET_PASSPHRASE")
            # Symbol formatting based on BitGet specs
            self.symbol_format = "{0}/USDT:USDT"
            self.symbol_suffix = "_UMCBL"
            # BitGet specific API URL
            self.api_url = os.environ.get("BITGET_API_URL")
        else:
            # Generic credentials for other exchanges
            api_key = api_key or os.environ.get("EXCHANGE_API_KEY")
            api_secret = api_secret or os.environ.get("EXCHANGE_API_SECRET")
            api_password = api_password or os.environ.get("EXCHANGE_API_PASSPHRASE")
            # Default symbol format
            self.symbol_format = "{0}/USDT"
            self.symbol_suffix = ""
            self.api_url = None
            
        # Default to testnet from environment
        use_testnet_env = os.environ.get("USE_TESTNET", "").lower()
        self.use_testnet = use_testnet if use_testnet is not None else (use_testnet_env == "true")
        
        # Set default trading symbol
        self.default_symbol = symbol or os.environ.get("SYMBOL", "BTCUSDT")
        
        # Initialize exchange with proper options
        try:
            options = {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'recvWindow': 60000,
                'testnet': self.use_testnet,
            }
            
            # Add any additional exchange-specific options
            if self.exchange_id.lower() == "bitget":
                options["createMarketBuyOrderRequiresPrice"] = False
                if self.api_url:
                    options["urls"] = {"api": self.api_url}
                
            # Create exchange instance
            self.exchange = ccxt_async.exchanges[self.exchange_id]({
                'apiKey': api_key,
                'secret': api_secret,
                'password': api_password,
                'enableRateLimit': True,
                'options': options
            })
            
            if self.use_testnet:
                self.exchange.set_sandbox_mode(True)
                
            logger.info(f"Initialized {self.exchange_id.upper()} with {'TESTNET' if self.use_testnet else 'MAINNET'}")
            
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {e}")
            self.exchange = None
            
        # WebSocket related attributes
        self.ws_callbacks = {}
        self.ws_connected = False
        self.ws_last_message_time = {}
        self.ws_heartbeat_interval = 30  # seconds
        
    def _format_symbol(self, symbol: Optional[str]) -> str:
        """Format symbol for exchange API."""
        if not symbol:
            symbol = self.default_symbol
            
        # If the symbol is already formatted (contains a slash), return it as is
        if '/' in symbol:
            return symbol.upper()
            
        # Strip the symbol suffix if it's already there
        if self.symbol_suffix and symbol.endswith(self.symbol_suffix):
            symbol = symbol[:-len(self.symbol_suffix)]
        
        # If the symbol ends with USDT, remove it for formatting
        if symbol.upper().endswith('USDT'):
            base = symbol[:-4]  # Remove 'USDT' from the end
            return self.symbol_format.format(base).upper()
            
        # Format for default symbol
        return self.symbol_format.format(symbol).upper()
        
    async def create_market_order(
        self,
        symbol: str,
        side: Literal["buy", "sell"],
        amount: float,
        reduce_only: bool = False,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a market order.
        
        Args:
            symbol: Trading symbol
            side: Order side (buy/sell)
            amount: Order amount
            reduce_only: Whether this order should only reduce position
            params: Additional parameters
            
        Returns:
            Dict containing order information
        """
        if not self.exchange:
            logger.error("Exchange not initialized")
            return {"error": "Exchange not initialized"}
            
        formatted_symbol = self._format_symbol(symbol)
        
        try:
            order_params = params or {}
            if reduce_only:
                order_params["reduceOnly"] = True
                
            order = await self.exchange.create_order(
                symbol=formatted_symbol,
                type="market",
                side=side,
                amount=amount,
                params=order_params
            )
            
            logger.info(f"Created market {side} order for {amount} {formatted_symbol}")
            return to_dict(order)
            
        except Exception as e:
            logger.error(f"Error creating market order: {e}")
            return {"error": str(e)}
    
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
        Create an order of any type.
        
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
        if not self.exchange:
            logger.error("Exchange not initialized")
            return {"error": "Exchange not initialized"}
            
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
            
            logger.info(f"Created {type} {side} order for {amount} {formatted_symbol}")
            return to_dict(order)
            
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return {"error": str(e)}
            
    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch current ticker information for a symbol.
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Dict containing ticker information
        """
        if not self.exchange:
            logger.error("Exchange not initialized")
            return {"error": "Exchange not initialized"}
            
        formatted_symbol = self._format_symbol(symbol)
        
        try:
            ticker = await self.exchange.fetch_ticker(formatted_symbol)
            return to_dict(ticker)
        except Exception as e:
            logger.error(f"Error fetching ticker: {e}")
            return {"error": str(e)}
            
    async def fetch_balance(self) -> Dict[str, Any]:
        """
        Fetch current account balance.
        
        Returns:
            Dict containing balance information
        """
        if not self.exchange:
            logger.error("Exchange not initialized")
            return {"error": "Exchange not initialized"}
            
        try:
            balance = await self.exchange.fetch_balance()
            return to_dict(balance)
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return {"error": str(e)}
            
    async def fetch_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch current positions.
        
        Args:
            symbol: Optional trading symbol to filter positions
            
        Returns:
            List of position information
        """
        if not self.exchange:
            logger.error("Exchange not initialized")
            return [{"error": "Exchange not initialized"}]
            
        try:
            formatted_symbol = self._format_symbol(symbol) if symbol else None
            formatted_symbols = [formatted_symbol] if formatted_symbol else None
            positions = await self.exchange.fetch_positions(formatted_symbols)
            return [to_dict(pos) for pos in positions]
        except Exception as e:
            logger.error(f"Error fetching positions: {e}")
            return [{"error": str(e)}]

    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List[List[Any]]:
        """
        Fetch OHLCV candlestick data.
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            limit: Number of candles to fetch
            
        Returns:
            List of OHLCV candles [timestamp, open, high, low, close, volume]
        """
        if not self.exchange:
            logger.error("Exchange not initialized")
            return []
            
        formatted_symbol = self._format_symbol(symbol)
        
        try:
            candles = await self.exchange.fetch_ohlcv(
                symbol=formatted_symbol,
                timeframe=timeframe,
                limit=limit
            )
            return candles
        except Exception as e:
            logger.error(f"Error fetching OHLCV data: {e}")
            return []
    
    async def close_position(self, symbol: str, side: Optional[str] = None) -> Dict[str, Any]:
        """
        Close an open position.
        
        Args:
            symbol: Trading symbol
            side: Optional side to close (if None, closes both sides)
            
        Returns:
            Result of the close operation
        """
        if not self.exchange:
            logger.error("Exchange not initialized")
            return {"error": "Exchange not initialized"}
            
        try:
            # Get current positions
            positions = await self.fetch_positions(symbol)
            if not positions or "error" in positions[0]:
                return {"error": "No positions found or error fetching positions"}
                
            results = []
            for position in positions:
                # Skip if position info is missing
                if not position.get("info"):
                    continue
                    
                # Skip positions with no size
                position_size = float(position.get("contracts", 0))
                if position_size == 0:
                    continue
                    
                # Skip if side doesn't match requested side
                position_side = position.get("side", "").lower()
                if side and position_side != side.lower():
                    continue
                    
                # Create market order in opposite direction
                close_side = "sell" if position_side == "long" else "buy"
                close_result = await self.create_market_order(
                    symbol=symbol,
                    side=close_side,
                    amount=abs(position_size),
                    reduce_only=True
                )
                
                results.append(close_result)
                
            return {"closed_positions": results}
                
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return {"error": str(e)}
            
    async def set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """
        Set leverage for a symbol.
        
        Args:
            symbol: Trading symbol
            leverage: Leverage level
            
        Returns:
            Result of setting leverage
        """
        if not self.exchange:
            logger.error("Exchange not initialized")
            return {"error": "Exchange not initialized"}
            
        # Get max leverage from env or use provided
        max_leverage = int(os.environ.get("MAX_LEVERAGE", "20"))
        if leverage > max_leverage:
            logger.warning(f"Requested leverage {leverage} exceeds max leverage {max_leverage}. Using {max_leverage} instead.")
            leverage = max_leverage
            
        formatted_symbol = self._format_symbol(symbol)
        
        try:
            result = await self.exchange.set_leverage(leverage, formatted_symbol)
            logger.info(f"Set leverage for {formatted_symbol} to {leverage}x")
            return to_dict(result) if result else {"success": True}
        except Exception as e:
            logger.error(f"Error setting leverage: {e}")
            return {"error": str(e)}
            
    async def initialize(self) -> None:
        """Initialize the exchange connection."""
        if not self.exchange:
            logger.error("Exchange not initialized")
            return
            
        try:
            # Load markets
            await self.exchange.load_markets()
            logger.info(f"Loaded markets for {self.exchange_id}")
        except Exception as e:
            logger.error(f"Error initializing exchange: {e}")
            
    async def close(self) -> None:
        """Close exchange connections."""
        if self.exchange:
            try:
                await self.exchange.close()
                logger.info(f"Closed connection to {self.exchange_id}")
            except Exception as e:
                logger.error(f"Error closing exchange connection: {e}")

# Alias for backward compatibility  
CCXTClientB0t = ExchangeClientB0t 