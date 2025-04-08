#!/usr/bin/env python3

"""
Exchange Service for Omega Bot Farm

This module provides a centralized service for initializing and managing
exchange clients across different bots. It handles common exchange operations,
credential management, and error handling.
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union

# Global ccxt import
try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    logging.warning("ccxt module not installed. Exchange functionality will be limited.")

class ExchangeService:
    """
    Service for managing exchange clients and operations.
    
    This service provides a centralized way to initialize exchange clients,
    handle credentials, and perform common exchange operations. It supports
    multiple exchanges with a focus on BitGet.
    """
    
    SUPPORTED_EXCHANGES = ["bitget", "binance", "bybit", "okx"]
    
    def __init__(self, 
                 exchange_id: str = "bitget",
                 api_key: Optional[str] = None, 
                 api_secret: Optional[str] = None,
                 api_passphrase: Optional[str] = None,
                 use_testnet: bool = False,
                 options: Optional[Dict[str, Any]] = None):
        """
        Initialize the Exchange Service.
        
        Args:
            exchange_id: The exchange ID (e.g., "bitget", "binance")
            api_key: API key (will use env var {EXCHANGE_ID}_API_KEY if None)
            api_secret: API secret (will use env var {EXCHANGE_ID}_SECRET_KEY if None)
            api_passphrase: API passphrase (will use env var {EXCHANGE_ID}_PASSPHRASE if None)
            use_testnet: Whether to use testnet
            options: Additional options for the exchange client
        """
        self.exchange_id = exchange_id.lower()
        self.use_testnet = use_testnet
        
        # Validate exchange ID
        if self.exchange_id not in self.SUPPORTED_EXCHANGES:
            logging.warning(f"Exchange {exchange_id} is not officially supported. Proceed with caution.")
        
        # Get API credentials
        self.api_key = api_key or os.environ.get(f"{exchange_id.upper()}_API_KEY", "")
        self.api_secret = api_secret or os.environ.get(f"{exchange_id.upper()}_SECRET_KEY", "")
        self.api_passphrase = api_passphrase or os.environ.get(f"{exchange_id.upper()}_PASSPHRASE", "")
        
        # Default options
        self.options = {
            'defaultType': 'swap',
            'adjustForTimeDifference': True,
            'testnet': use_testnet,
        }
        
        # Update with custom options if provided
        if options:
            self.options.update(options)
        
        # Exchange client
        self.exchange = None
        self.ccxt_client = None  # For async client compatibility
        
        # Initialize if ccxt is available
        if CCXT_AVAILABLE:
            self._initialize_exchange()
        else:
            logging.error(f"Cannot initialize {exchange_id} exchange: CCXT not available")
    
    def _initialize_exchange(self) -> None:
        """Initialize the CCXT exchange client."""
        # Check global ccxt availability to avoid unbound error
        if not CCXT_AVAILABLE:
            logging.error("Cannot initialize exchange: CCXT not available")
            return
            
        if not self.api_key or not self.api_secret:
            logging.error(f"Cannot initialize {self.exchange_id} exchange: Missing API credentials")
            return
        
        try:
            # Create exchange config
            exchange_config = {
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'options': self.options
            }
            
            # Add passphrase for exchanges that require it
            if self.exchange_id in ["bitget", "okx", "kucoin"]:
                if not self.api_passphrase:
                    logging.error(f"{self.exchange_id} requires a passphrase, but none was provided")
                    return
                exchange_config['password'] = self.api_passphrase
            
            # Initialize the exchange client using the globally imported ccxt
            exchange_class = getattr(ccxt, self.exchange_id)
            self.exchange = exchange_class(exchange_config)
            
            # Set testnet mode if required
            if self.use_testnet:
                self.exchange.set_sandbox_mode(True)
                logging.info(f"Connected to {self.exchange_id.upper()} TESTNET")
            else:
                logging.info(f"Connected to {self.exchange_id.upper()} MAINNET")
                
        except AttributeError:
            logging.error(f"Exchange {self.exchange_id} is not supported by CCXT")
            self.exchange = None
        except Exception as e:
            logging.error(f"Failed to initialize {self.exchange_id} exchange: {e}")
            self.exchange = None
    
    def is_connected(self) -> bool:
        """Check if the exchange client is properly initialized."""
        return self.exchange is not None
    
    async def fetch_positions(self) -> List[Dict[str, Any]]:
        """
        Fetch positions from the exchange.
        
        Returns:
            List of position data dictionaries
        """
        if not self.exchange:
            logging.error("Cannot fetch positions: Exchange client not initialized")
            return []
            
        try:
            positions = self.exchange.fetch_positions()
            return positions
        except Exception as e:
            logging.error(f"Error fetching positions from {self.exchange_id}: {e}")
            return []
    
    async def fetch_balance(self) -> Dict[str, Any]:
        """
        Fetch account balance from the exchange.
        
        Returns:
            Dictionary with balance information
        """
        if not self.exchange:
            logging.error("Cannot fetch balance: Exchange client not initialized")
            return {}
            
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            logging.error(f"Error fetching balance from {self.exchange_id}: {e}")
            return {}
    
    async def create_order(self, 
                          symbol: str, 
                          order_type: str, 
                          side: str, 
                          amount: float, 
                          price: Optional[float] = None,
                          params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create an order on the exchange.
        
        Args:
            symbol: Trading pair symbol
            order_type: Order type (market, limit, etc.)
            side: Order side (buy or sell)
            amount: Order amount
            price: Order price (for limit orders)
            params: Additional order parameters
            
        Returns:
            Dictionary with order information
        """
        if not self.exchange:
            logging.error("Cannot create order: Exchange client not initialized")
            return {"error": "Exchange client not initialized"}
            
        try:
            order = self.exchange.create_order(symbol, order_type, side, amount, price, params or {})
            return order
        except Exception as e:
            logging.error(f"Error creating order on {self.exchange_id}: {e}")
            return {"error": str(e)}
    
    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch ticker information for a symbol.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Dictionary with ticker information
        """
        if not self.exchange:
            logging.error("Cannot fetch ticker: Exchange client not initialized")
            return {}
            
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            logging.error(f"Error fetching ticker for {symbol} from {self.exchange_id}: {e}")
            return {}
            
    async def close(self) -> None:
        """Close the exchange connection and clean up resources."""
        if hasattr(self.exchange, 'close') and callable(self.exchange.close):
            try:
                await self.exchange.close()
                logging.info(f"Closed connection to {self.exchange_id.upper()}")
            except Exception as e:
                logging.error(f"Error closing {self.exchange_id} connection: {e}")
        
        self.exchange = None
        self.ccxt_client = None
            
    def get_exchange_client(self):
        """Get the underlying CCXT exchange client."""
        return self.exchange


def create_exchange_service(exchange: str = "bitget", 
                           api_key: Optional[str] = None,
                           api_secret: Optional[str] = None,
                           api_passphrase: Optional[str] = None,
                           use_testnet: bool = False,
                           **kwargs) -> ExchangeService:
    """
    Create and initialize an ExchangeService instance.
    
    Args:
        exchange: Exchange ID (e.g., 'bitget', 'binance')
        api_key: API key
        api_secret: API secret
        api_passphrase: API passphrase
        use_testnet: Whether to use testnet
        **kwargs: Additional options
        
    Returns:
        Initialized ExchangeService instance
    """
    service = ExchangeService(
        exchange_id=exchange,
        api_key=api_key,
        api_secret=api_secret,
        api_passphrase=api_passphrase,
        use_testnet=use_testnet,
        options=kwargs.get('options')
    )
    
    return service 