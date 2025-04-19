#!/usr/bin/env python3
"""
BitGet Exchange API Client

This module implements the BitGet exchange API client for interacting
with the BitGet cryptocurrency exchange.

Copyright (c) 2024 OMEGA BTC AI
Licensed under the GBU2 License - see LICENSE file for details

OMEGA BTC AI - BitGet Exchange Client
===================================

This module implements a client for interacting with the BitGet
cryptocurrency exchange API. It provides methods for:

1. Account Management
2. Market Data
3. Order Management
4. Position Management

Features:
- REST API integration
- WebSocket support
- Rate limiting
- Error handling
"""

import os
import sys
import json
import time
import hmac
import base64
import hashlib
import logging
import aiohttp
import asyncio
from typing import Dict, List, Optional, Any, Union, Type
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BitGetClient:
    """BitGet exchange API client implementation."""
    
    # API endpoints
    BASE_URL = "https://api.bitget.com"
    WS_URL = "wss://ws.bitget.com/spot/v1/stream"
    
    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 passphrase: str):
        """Initialize the BitGet client."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        
        # Initialize session
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws = None
        
        logger.info("Initialized BitGet client")
    
    async def _init_session(self) -> None:
        """Initialize HTTP session."""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    def _generate_signature(self,
                          timestamp: str,
                          method: str,
                          request_path: str,
                          body: str = "") -> str:
        """Generate API request signature."""
        message = timestamp + method.upper() + request_path + body
        mac = hmac.new(
            bytes(self.api_secret, encoding='utf8'),
            bytes(message, encoding='utf-8'),
            digestmod='sha256'
        )
        return base64.b64encode(mac.digest()).decode()
    
    async def _request(self,
                      method: str,
                      path: str,
                      params: Optional[Dict] = None,
                      data: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated API request."""
        if not self.session:
            await self._init_session()
            if not self.session:
                return None
        
        # Prepare request
        url = self.BASE_URL + path
        timestamp = str(int(time.time() * 1000))
        
        # Build signature
        body = json.dumps(data) if data else ""
        signature = self._generate_signature(timestamp, method, path, body)
        
        # Headers
        headers = {
            'ACCESS-KEY': self.api_key,
            'ACCESS-SIGN': signature,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        try:
            async with self.session.request(
                method,
                url,
                headers=headers,
                params=params,
                json=data
            ) as response:
                result = await response.json()
                
                if response.status != 200:
                    logger.error(f"API error: {result}")
                    return None
                
                return result
                
        except Exception as e:
            logger.error(f"Request error: {str(e)}")
            return None
    
    async def get_account_balance(self) -> Optional[Dict]:
        """Get account balance information."""
        try:
            response = await self._request(
                'GET',
                '/api/spot/v1/account/assets'
            )
            
            if response and response.get('data'):
                return response['data']
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting account balance: {str(e)}")
            return None
    
    async def get_market_ticker(self, symbol: str) -> Optional[Dict]:
        """Get market ticker information."""
        try:
            response = await self._request(
                'GET',
                f'/api/spot/v1/market/ticker?symbol={symbol}'
            )
            
            if response and response.get('data'):
                return response['data']
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting market ticker: {str(e)}")
            return None
    
    async def get_klines(self,
                        symbol: str,
                        interval: str,
                        limit: int = 100) -> List[Dict]:
        """Get candlestick data."""
        try:
            response = await self._request(
                'GET',
                f'/api/spot/v1/market/candles',
                params={
                    'symbol': symbol,
                    'period': interval,
                    'limit': limit
                }
            )
            
            if response and response.get('data'):
                # Convert to OHLCV format
                klines = []
                for k in response['data']:
                    klines.append({
                        'timestamp': int(k[0]),
                        'open': float(k[1]),
                        'high': float(k[2]),
                        'low': float(k[3]),
                        'close': float(k[4]),
                        'volume': float(k[5])
                    })
                return klines
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting klines: {str(e)}")
            return []
    
    async def create_order(self,
                          symbol: str,
                          side: str,
                          order_type: str,
                          quantity: float,
                          price: Optional[float] = None,
                          stop_price: Optional[float] = None,
                          time_in_force: str = 'GTC') -> Optional[Dict]:
        """Create a new order."""
        try:
            data = {
                'symbol': symbol,
                'side': side.upper(),
                'orderType': order_type.upper(),
                'quantity': str(quantity),
                'timeInForce': time_in_force
            }
            
            if price is not None:
                data['price'] = str(price)
            
            if stop_price is not None:
                data['stopPrice'] = str(stop_price)
            
            response = await self._request(
                'POST',
                '/api/spot/v1/trade/orders',
                data=data
            )
            
            if response and response.get('data'):
                return response['data']
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return None
    
    async def cancel_order(self,
                          symbol: str,
                          order_id: str) -> bool:
        """Cancel an existing order."""
        try:
            response = await self._request(
                'POST',
                '/api/spot/v1/trade/cancel-order',
                data={
                    'symbol': symbol,
                    'orderId': order_id
                }
            )
            
            return bool(response and response.get('code') == '00000')
            
        except Exception as e:
            logger.error(f"Error canceling order: {str(e)}")
            return False
    
    async def get_order_status(self,
                             symbol: str,
                             order_id: str) -> Optional[str]:
        """Get order status."""
        try:
            response = await self._request(
                'GET',
                f'/api/spot/v1/trade/orders/{order_id}',
                params={'symbol': symbol}
            )
            
            if response and response.get('data'):
                return response['data']['status']
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting order status: {str(e)}")
            return None
    
    async def get_open_orders(self, symbol: str) -> List[Dict]:
        """Get open orders."""
        try:
            response = await self._request(
                'GET',
                '/api/spot/v1/trade/open-orders',
                params={'symbol': symbol}
            )
            
            if response and response.get('data'):
                return response['data']
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting open orders: {str(e)}")
            return []
    
    async def get_positions(self, symbol: str) -> List[Dict]:
        """Get open positions."""
        try:
            response = await self._request(
                'GET',
                '/api/mix/v1/position/allPosition',
                params={'symbol': symbol}
            )
            
            if response and response.get('data'):
                return response['data']
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            return []
    
    async def get_current_price(self, symbol: str) -> float:
        """Get current market price."""
        try:
            ticker = await self.get_market_ticker(symbol)
            if ticker and 'last' in ticker:
                return float(ticker['last'])
            return 0.0
            
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}")
            return 0.0
    
    async def close(self) -> None:
        """Close client connections."""
        try:
            if self.session:
                await self.session.close()
                self.session = None
            
            if self.ws:
                await self.ws.close()
                self.ws = None
                
            logger.info("Closed BitGet client connections")
            
        except Exception as e:
            logger.error(f"Error closing connections: {str(e)}")
    
    async def __aenter__(self) -> 'BitGetClient':
        """Async context manager entry."""
        await self._init_session()
        return self
    
    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException],
                        exc_tb: Optional[Any]) -> None:
        """Async context manager exit."""
        await self.close() 