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
Coin Picker Module for OmegaBTC AI

This module provides functionality to select and filter trading pairs
based on various criteria using the BitGet API.
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from dataclasses import dataclass
from enum import Enum

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

logger = logging.getLogger(__name__)

class CoinType(Enum):
    """Enum for different types of coins."""
    SPOT = "spot"
    FUTURES = "futures"
    LEVERAGED = "leveraged"

@dataclass
class CoinInfo:
    """Information about a trading symbol."""
    symbol: str
    base_currency: str
    quote_currency: str
    type: CoinType = CoinType.SPOT
    maker_fee: float = 0.0
    taker_fee: float = 0.0
    min_trade_amount: float = 0.0
    min_trade_usd: float = 0.0
    last_price: Optional[float] = None
    volume_24h: Optional[float] = None
    price_change_24h: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "symbol": self.symbol,
            "base_currency": self.base_currency,
            "quote_currency": self.quote_currency,
            "type": self.type.value,
            "maker_fee": self.maker_fee,
            "taker_fee": self.taker_fee,
            "min_trade_amount": self.min_trade_amount,
            "min_trade_usd": self.min_trade_usd,
            "last_price": self.last_price,
            "volume_24h": self.volume_24h,
            "price_change_24h": self.price_change_24h
        }

class CoinPicker:
    """Handles coin selection and filtering using BitGet API."""
    
    def __init__(self, use_testnet: bool = True, api_key: str = "", secret_key: str = "", passphrase: str = ""):
        """Initialize the CoinPicker."""
        self.use_testnet = use_testnet
        self.coins_cache: Dict[str, CoinInfo] = {}
        self.last_update = datetime.min
        self.cache_valid_time = 3600  # Cache valid for 1 hour
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        
        # Set API URL based on testnet flag
        if use_testnet:
            self.api_url = "https://api-testnet.bitget.com"
        else:
            self.api_url = "https://api.bitget.com"
            
        # Set API base path
        self.api_base = "/api/v2"  # Updated to v2 API
        
        # Initialize features
        self.market_data_cache: Dict[str, Dict[str, Any]] = {}
        self.volume_cache: Dict[str, float] = {}
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """Make an HTTP request to the BitGet API."""
        try:
            url = f"{self.api_url}{endpoint}"
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"{RED}Error making request: {str(e)}{RESET}")
            return None
            
    def update_coins_cache(self) -> bool:
        """Update the coins cache with fresh data from BitGet."""
        try:
            # Get spot symbols
            spot_endpoint = f"{self.api_base}/spot/public/symbols"
            spot_response = self._make_request("GET", spot_endpoint)
            if not spot_response:
                return False
                
            spot_data = spot_response.json()
            if spot_data.get("code") != "00000":
                logger.error(f"{RED}Error fetching spot symbols: {spot_data.get('msg')}{RESET}")
                return False
                
            # Get futures symbols
            futures_endpoint = f"{self.api_base}/mix/market/contracts"
            futures_response = self._make_request("GET", futures_endpoint, params={"productType": "USDT-FUTURES"})
            if not futures_response:
                return False
                
            futures_data = futures_response.json()
            if futures_data.get("code") != "00000":
                logger.error(f"{RED}Error fetching futures symbols: {futures_data.get('msg')}{RESET}")
                return False
                
            # Clear existing cache
            self.coins_cache.clear()
                
            # Process spot symbols
            for symbol_data in spot_data.get("data", []):
                symbol_name = symbol_data.get("symbolName")
                base_currency = symbol_data.get("baseCoin")
                quote_currency = symbol_data.get("quoteCoin")
                
                if not symbol_name or not base_currency or not quote_currency:
                    continue
                    
                self.coins_cache[symbol_name] = CoinInfo(
                    symbol=symbol_name,
                    base_currency=base_currency,
                    quote_currency=quote_currency,
                    type=CoinType.SPOT,
                    maker_fee=float(symbol_data.get("makerFeeRate", 0)),
                    taker_fee=float(symbol_data.get("takerFeeRate", 0)),
                    min_trade_amount=float(symbol_data.get("minTradeAmount", 0)),
                    min_trade_usd=float(symbol_data.get("minTradeUSDT", 0))
                )
                
            # Process futures symbols
            for symbol_data in futures_data.get("data", []):
                symbol_name = symbol_data.get("symbol")
                base_currency = symbol_data.get("baseCoin")
                quote_currency = symbol_data.get("quoteCoin")
                
                if not symbol_name or not base_currency or not quote_currency:
                    continue
                    
                self.coins_cache[symbol_name] = CoinInfo(
                    symbol=symbol_name,
                    base_currency=base_currency,
                    quote_currency=quote_currency,
                    type=CoinType.FUTURES,
                    maker_fee=float(symbol_data.get("makerFeeRate", 0)),
                    taker_fee=float(symbol_data.get("takerFeeRate", 0)),
                    min_trade_amount=float(symbol_data.get("minTradeNum", 0)),
                    min_trade_usd=float(symbol_data.get("minTradeUSDT", 0))
                )
                
            logger.info(f"{GREEN}Successfully updated coins cache with {len(self.coins_cache)} coins{RESET}")
            logger.info(f"{BLUE}Spot coins: {len([c for c in self.coins_cache.values() if c.type == CoinType.SPOT])}{RESET}")
            logger.info(f"{BLUE}Futures coins: {len([c for c in self.coins_cache.values() if c.type == CoinType.FUTURES])}{RESET}")
            
            # Update timestamp
            self.last_update = datetime.now()
            return True
            
        except Exception as e:
            logger.error(f"{RED}Error updating coins cache: {str(e)}{RESET}")
            return False
            
    def get_symbol_info(self, symbol: str) -> Optional[CoinInfo]:
        """Get information about a specific symbol."""
        # Update cache if needed
        if not self.last_update or (datetime.now() - self.last_update).seconds > self.cache_valid_time:
            self.update_coins_cache()
            
        return self.coins_cache.get(symbol)
        
    def get_available_symbols(self, 
                           coin_type: Optional[CoinType] = None,
                           min_volume: Optional[float] = None,
                           min_price: Optional[float] = None,
                           max_price: Optional[float] = None,
                           quote_currency: Optional[str] = None,
                           min_trade_usd: Optional[float] = None,
                           max_trade_usd: Optional[float] = None) -> List[CoinInfo]:
        """Get list of available symbols filtered by criteria."""
        # Update cache if needed
        if not self.last_update or (datetime.now() - self.last_update).seconds > self.cache_valid_time:
            self.update_coins_cache()
            
        filtered_symbols = []
        
        for symbol in self.coins_cache.values():
            # Apply filters
            if coin_type and symbol.type != coin_type:
                continue
                
            if quote_currency and symbol.quote_currency != quote_currency:
                continue
                
            if min_volume and (not symbol.volume_24h or symbol.volume_24h < min_volume):
                continue
                
            if min_price and (not symbol.last_price or symbol.last_price < min_price):
                continue
                
            if max_price and (not symbol.last_price or symbol.last_price > max_price):
                continue
                
            if min_trade_usd and (symbol.min_trade_usd < min_trade_usd):
                continue
                
            if max_trade_usd and (symbol.min_trade_usd > max_trade_usd):
                continue
                
            filtered_symbols.append(symbol)
            
        return filtered_symbols
        
    def get_top_symbols(self, 
                       limit: int = 10,
                       sort_by: str = "volume",
                       quote_currency: str = "USDT") -> List[CoinInfo]:
        """Get top symbols by specified criteria."""
        # Update cache if needed
        if not self.last_update or (datetime.now() - self.last_update).seconds > self.cache_valid_time:
            self.update_coins_cache()
            
        # Get all symbols with the specified quote currency
        symbols = self.get_available_symbols(quote_currency=quote_currency)
        
        # Sort symbols based on criteria
        if sort_by == "volume":
            symbols.sort(key=lambda x: x.volume_24h or 0, reverse=True)
        elif sort_by == "price":
            symbols.sort(key=lambda x: x.last_price or 0, reverse=True)
        elif sort_by == "price_change":
            symbols.sort(key=lambda x: x.price_change_24h or 0, reverse=True)
            
        return symbols[:limit]
        
    def get_symbol_ticker(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current ticker data for a symbol."""
        endpoint = f"{self.api_base}/spot/market/ticker"
        params = {"symbol": symbol}
        
        response = self._make_request("GET", endpoint, params=params)
        if not response:
            return None
            
        data = response.json()
        if data.get("code") != "00000":
            logger.error(f"{RED}Error fetching ticker: {data.get('msg')}{RESET}")
            return None
            
        return data.get("data")
        
    def get_symbol_klines(self, 
                         symbol: str,
                         interval: str = "1h",
                         limit: int = 100) -> Optional[List[Dict[str, Any]]]:
        """Get kline (candlestick) data for a symbol."""
        endpoint = f"{self.api_base}/spot/market/candles"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": str(limit)
        }
        
        response = self._make_request("GET", endpoint, params=params)
        if not response:
            return None
            
        data = response.json()
        if data.get("code") != "00000":
            logger.error(f"{RED}Error fetching klines: {data.get('msg')}{RESET}")
            return None
            
        return data.get("data")
        
    def get_symbol_depth(self, 
                        symbol: str,
                        limit: int = 100) -> Optional[Dict[str, Any]]:
        """Get order book depth for a symbol."""
        endpoint = f"{self.api_base}/spot/market/depth"
        params = {
            "symbol": symbol,
            "limit": str(limit)
        }
        
        response = self._make_request("GET", endpoint, params=params)
        if not response:
            return None
            
        data = response.json()
        if data.get("code") != "00000":
            logger.error(f"{RED}Error fetching depth: {data.get('msg')}{RESET}")
            return None
            
        return data.get("data")
        
    def get_symbol_trades(self, 
                         symbol: str,
                         limit: int = 100) -> Optional[List[Dict[str, Any]]]:
        """Get recent trades for a symbol."""
        endpoint = f"{self.api_base}/spot/market/trades"
        params = {
            "symbol": symbol,
            "limit": str(limit)
        }
        
        response = self._make_request("GET", endpoint, params=params)
        if not response:
            return None
            
        data = response.json()
        if data.get("code") != "00000":
            logger.error(f"{RED}Error fetching trades: {data.get('msg')}{RESET}")
            return None
            
        return data.get("data")
        
    def analyze_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Analyze a symbol to get detailed market information."""
        # Get symbol info
        symbol_info = self.get_symbol_info(symbol)
        if not symbol_info:
            logger.error(f"{RED}Symbol {symbol} not found{RESET}")
            return None
            
        # Get ticker
        ticker_endpoint = "/api/v2/mix/market/ticker" if symbol_info.type == CoinType.FUTURES else "/api/v2/spot/market/tickers"
        ticker_params = {"symbol": symbol}
            
        ticker_response = self._make_request("GET", ticker_endpoint, params=ticker_params)
        if not ticker_response:
            logger.error(f"{RED}Failed to get ticker for {symbol}{RESET}")
            return None
            
        ticker_data = ticker_response.json()
        if ticker_data.get("code") != "00000":
            logger.error(f"{RED}Error fetching ticker: {ticker_data.get('msg')}{RESET}")
            return None
            
        ticker = ticker_data.get("data")
        
        # Get depth
        depth_endpoint = "/api/v2/mix/market/orderbook" if symbol_info.type == CoinType.FUTURES else "/api/v2/spot/market/orderbook"
        depth_params = {"symbol": symbol, "limit": "5"}
            
        depth_response = self._make_request("GET", depth_endpoint, params=depth_params)
        if not depth_response:
            logger.error(f"{RED}Failed to get depth for {symbol}{RESET}")
            return None
            
        depth_data = depth_response.json()
        if depth_data.get("code") != "00000":
            logger.error(f"{RED}Error fetching depth: {depth_data.get('msg')}{RESET}")
            return None
            
        depth = depth_data.get("data")
        
        # Try to update symbol info with market data
        symbol_info.last_price = float(ticker.get("last", 0))
        symbol_info.volume_24h = float(ticker.get("volume24h", 0))
        symbol_info.price_change_24h = float(ticker.get("priceChangePercent", 0))
        
        # Return comprehensive analysis
        return {
            "symbol": symbol_info.symbol,
            "base_currency": symbol_info.base_currency,
            "quote_currency": symbol_info.quote_currency,
            "type": symbol_info.type.value,
            "last_price": symbol_info.last_price,
            "volume_24h": symbol_info.volume_24h,
            "price_change_24h": symbol_info.price_change_24h,
            "depth": {
                "bids": len(depth.get("bids", [])),
                "asks": len(depth.get("asks", []))
            },
            "maker_fee_rate": symbol_info.maker_fee,
            "taker_fee_rate": symbol_info.taker_fee,
            "min_trade_amount": symbol_info.min_trade_amount,
            "min_trade_usd": symbol_info.min_trade_usd
        }