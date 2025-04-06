#!/usr/bin/env python3
"""
AIXBT Dashboard - Real-Time Price Feed
----------------------------------

Real-time cryptocurrency price feed integration for the AIXBT Dashboard.
Provides WebSocket and REST API connections to BitGet via CCXT.
"""

import os
import sys
import asyncio
import logging
import time
import threading
from typing import Dict, Any, Callable, Optional, List
from pathlib import Path

# Configure logging
logger = logging.getLogger("AIXBTDashboard.PriceFeed")

# Add parent directory to sys.path to fix imports if needed
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Try to import CCXT - gracefully handle if it's not installed
try:
    import ccxt
    import ccxt.async_support as ccxt_async
    HAVE_CCXT = True
except ImportError:
    HAVE_CCXT = False
    logger.warning("CCXT not installed. Install with: pip install ccxt")

class PriceFeed:
    """Real-time price feed for cryptocurrency market data."""
    
    def __init__(self, 
                exchange_id: str = "bitget",
                symbol: str = "BTCUSDT",
                api_key: Optional[str] = None,
                api_secret: Optional[str] = None,
                api_passphrase: Optional[str] = None,
                use_testnet: bool = False,
                update_callback: Optional[Callable[[float], None]] = None):
        """
        Initialize the price feed.
        
        Args:
            exchange_id: CCXT exchange ID (default: bitget)
            symbol: Trading symbol (default: BTCUSDT)
            api_key: API key for exchange
            api_secret: API secret for exchange
            api_passphrase: API passphrase (needed for some exchanges like BitGet)
            use_testnet: Whether to use the exchange's testnet
            update_callback: Callback function that gets called with updated price
        """
        self.exchange_id = exchange_id
        self.symbol = symbol
        self.api_key = api_key or os.environ.get("BITGET_API_KEY", "")
        self.api_secret = api_secret or os.environ.get("BITGET_SECRET_KEY", "")
        self.api_passphrase = api_passphrase or os.environ.get("BITGET_PASSPHRASE", "")
        self.use_testnet = use_testnet
        self.update_callback = update_callback
        
        # Initialize flags and values
        self.running = False
        self.current_price = 0.0
        self.last_update_time = 0
        self.exchange = None
        self.websocket_connected = False
        self.websocket_task = None
        self.last_error = None
        
        # Initialize CCXT if available
        if HAVE_CCXT:
            self._init_ccxt()
        else:
            logger.error("CCXT is required for price feed. Install with: pip install ccxt")
    
    def _init_ccxt(self):
        """Initialize CCXT exchange connection."""
        try:
            # Define exchange options
            options = {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'recvWindow': 60000,
                'testnet': self.use_testnet,
                'createMarketBuyOrderRequiresPrice': False
            }
            
            # Create exchange instance
            self.exchange = ccxt_async.exchanges[self.exchange_id]({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'password': self.api_passphrase,
                'enableRateLimit': True,
                'options': options
            })
            
            # Set sandbox mode if needed
            if self.use_testnet:
                self.exchange.set_sandbox_mode(True)
                
            logger.info(f"Initialized {self.exchange_id.upper()} with {'TESTNET' if self.use_testnet else 'MAINNET'}")
            
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"Failed to initialize exchange: {e}")
            self.exchange = None
    
    def _format_symbol(self) -> str:
        """Format the symbol for the exchange."""
        # Handle BitGet specific format
        if self.exchange_id.lower() == "bitget":
            # If the symbol is already formatted (contains a slash), return it as is
            if '/' in self.symbol:
                return self.symbol.upper()
                
            # Format BTCUSDT to BTC/USDT:USDT for BitGet
            if self.symbol.upper().endswith('USDT'):
                base = self.symbol[:-4]  # Remove 'USDT' from the end
                return f"{base}/USDT:USDT".upper()
                
            # Format basic symbol to include USDT pairs
            return f"{self.symbol}/USDT:USDT".upper()
        
        # Default formatting for other exchanges
        if '/' in self.symbol:
            return self.symbol.upper()
        
        return f"{self.symbol}/USDT".upper()
    
    async def fetch_price(self) -> float:
        """
        Fetch current price using REST API.
        
        Returns:
            Current price as float
        """
        if not self.exchange:
            logger.error("Exchange not initialized")
            return 0.0
        
        try:
            formatted_symbol = self._format_symbol()
            ticker = await self.exchange.fetch_ticker(formatted_symbol)
            
            # Extract last price
            price = float(ticker['last'])
            self.current_price = price
            self.last_update_time = time.time()
            
            # Call update callback if provided
            if self.update_callback:
                self.update_callback(price)
                
            return price
            
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"Error fetching price: {e}")
            return self.current_price
    
    async def _websocket_loop(self):
        """Internal WebSocket connection loop."""
        try:
            # Only attempt WebSocket if the exchange has watchTicker method
            if not hasattr(self.exchange, 'watchTicker'):
                logger.warning(f"{self.exchange_id} does not support WebSocket ticker")
                return
            
            formatted_symbol = self._format_symbol()
            self.websocket_connected = True
            
            logger.info(f"Starting WebSocket connection for {formatted_symbol}")
            
            while self.running:
                try:
                    # Watch ticker via WebSocket
                    ticker = await self.exchange.watchTicker(formatted_symbol)
                    
                    # Extract and update price
                    price = float(ticker['last'])
                    self.current_price = price
                    self.last_update_time = time.time()
                    
                    # Call update callback if provided
                    if self.update_callback:
                        self.update_callback(price)
                        
                except Exception as e:
                    logger.error(f"WebSocket error: {e}")
                    await asyncio.sleep(5)  # Wait before reconnecting
            
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"WebSocket loop error: {e}")
        finally:
            self.websocket_connected = False
            logger.info("WebSocket connection closed")
    
    async def _rest_polling_loop(self, interval_seconds: float = 2.0):
        """
        Poll for price updates using REST API at specified interval.
        
        Args:
            interval_seconds: Seconds between updates
        """
        logger.info(f"Starting REST polling for {self.symbol} at {interval_seconds}s intervals")
        
        while self.running:
            try:
                await self.fetch_price()
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"REST polling error: {e}")
                await asyncio.sleep(5)  # Wait before retrying
    
    def start(self, polling_interval: float = 2.0, use_websocket: bool = True):
        """
        Start the price feed.
        
        Args:
            polling_interval: Seconds between REST API updates
            use_websocket: Whether to use WebSocket (if available)
        """
        if self.running:
            logger.warning("Price feed already running")
            return
        
        if not HAVE_CCXT or not self.exchange:
            logger.error("Cannot start price feed: CCXT not available or exchange not initialized")
            return
        
        self.running = True
        
        # Create and run the asyncio event loop in a separate thread
        def run_event_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Define coroutines to run
                tasks = []
                
                # Use WebSocket if available and requested
                if use_websocket and hasattr(self.exchange, 'watchTicker'):
                    self.websocket_task = loop.create_task(self._websocket_loop())
                    tasks.append(self.websocket_task)
                else:
                    # Fall back to REST polling
                    tasks.append(loop.create_task(self._rest_polling_loop(polling_interval)))
                
                # Run until stopped
                loop.run_until_complete(asyncio.gather(*tasks))
            except Exception as e:
                logger.error(f"Event loop error: {e}")
            finally:
                loop.close()
        
        # Start thread
        threading.Thread(target=run_event_loop, daemon=True).start()
        logger.info(f"Price feed started for {self.symbol}")
    
    def stop(self):
        """Stop the price feed."""
        self.running = False
        logger.info("Price feed stopped")
    
    def get_current_price(self) -> float:
        """
        Get the current price.
        
        Returns:
            Current price as float
        """
        return self.current_price


# Singleton instance for global access
_price_feed_instance = None

def init_price_feed(exchange_id: str = "bitget",
                   symbol: str = "BTCUSDT",
                   api_key: Optional[str] = None,
                   api_secret: Optional[str] = None,
                   api_passphrase: Optional[str] = None,
                   use_testnet: bool = False,
                   update_callback: Optional[Callable[[float], None]] = None,
                   polling_interval: float = 2.0,
                   use_websocket: bool = True) -> PriceFeed:
    """
    Initialize and start the global price feed.
    
    Args:
        exchange_id: CCXT exchange ID
        symbol: Trading symbol
        api_key: API key for exchange
        api_secret: API secret for exchange
        api_passphrase: API passphrase
        use_testnet: Whether to use testnet
        update_callback: Callback function for price updates
        polling_interval: Seconds between REST updates
        use_websocket: Whether to use WebSocket
        
    Returns:
        PriceFeed instance
    """
    global _price_feed_instance
    
    if _price_feed_instance is not None:
        _price_feed_instance.stop()
    
    _price_feed_instance = PriceFeed(
        exchange_id=exchange_id,
        symbol=symbol,
        api_key=api_key,
        api_secret=api_secret,
        api_passphrase=api_passphrase,
        use_testnet=use_testnet,
        update_callback=update_callback
    )
    
    _price_feed_instance.start(
        polling_interval=polling_interval,
        use_websocket=use_websocket
    )
    
    return _price_feed_instance

def get_price_feed() -> Optional[PriceFeed]:
    """
    Get the global price feed instance.
    
    Returns:
        PriceFeed instance or None if not initialized
    """
    return _price_feed_instance 