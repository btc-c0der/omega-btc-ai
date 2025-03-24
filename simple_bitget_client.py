"""
OMEGA BTC AI - Simple BitGet Client (v0.4.0)

A simplified BitGet client for standalone use.
This is a minimal implementation to support the advanced exit monitor.

Author: OMEGA BTC AI Team
Version: 0.4.0
"""

import os
import json
import time
import hmac
import base64
import logging
import hashlib
import asyncio
import random
from typing import Dict, List, Any, Optional
from urllib.parse import urlencode

try:
    import aiohttp
except ImportError:
    raise ImportError("aiohttp is required. Install it using 'pip install aiohttp'.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('simple_bitget_client')

class BitGetClient:
    """Simple BitGet API client for standalone use."""
    
    def __init__(self, api_key: str = '', api_secret: str = '', passphrase: str = '', is_demo: bool = False):
        """
        Initialize the BitGet client.
        
        Args:
            api_key: API key for authentication
            api_secret: API secret for signature
            passphrase: API passphrase for authentication
            is_demo: Whether to use demo/testnet mode
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.is_demo = is_demo
        
        # Set base URLs
        self.base_url = 'https://api.bitget.com'
        
        # Session for API requests
        self.session = None
        
        # Demo mode message
        if self.is_demo:
            logger.info("Running in demo mode - no real trades will be executed")
            
    async def _init_session(self):
        """Initialize aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
            
    async def _close_session(self):
        """Close aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
            
    def _generate_signature(self, timestamp: str, method: str, request_path: str, body: str = '') -> str:
        """
        Generate BitGet API signature.
        
        Args:
            timestamp: Timestamp in milliseconds
            method: HTTP method (GET, POST, etc.)
            request_path: API endpoint path
            body: Request body for POST/PUT requests
            
        Returns:
            Signature string
        """
        message = timestamp + method + request_path + (body if body else '')
        mac = hmac.new(
            bytes(self.api_secret, encoding='utf8'),
            bytes(message, encoding='utf-8'),
            digestmod=hashlib.sha256
        )
        return base64.b64encode(mac.digest()).decode()
        
    async def _request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """
        Make an API request to BitGet.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters for GET requests
            data: Request body for POST/PUT requests
            
        Returns:
            Response data dictionary
        """
        await self._init_session()
        
        # Full URL
        url = f"{self.base_url}{endpoint}"
        
        # Add query parameters if provided
        if params:
            query_string = urlencode(params)
            url = f"{url}?{query_string}"
            endpoint = f"{endpoint}?{query_string}"
            
        # Prepare request headers
        timestamp = str(int(time.time() * 1000))
        
        # Convert data to JSON string if provided
        body = ''
        if data:
            body = json.dumps(data)
            
        # Generate signature
        signature = self._generate_signature(timestamp, method, endpoint, body)
        
        headers = {
            'ACCESS-KEY': self.api_key,
            'ACCESS-SIGN': signature,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        try:
            # Make the request
            async with self.session.request(method, url, headers=headers, json=data if data else None) as response:
                # Check for errors
                if response.status >= 400:
                    error_text = await response.text()
                    logger.error(f"BitGet API error ({response.status}): {error_text}")
                    return {'success': False, 'error': error_text}
                    
                # Parse response
                response_data = await response.json()
                
                # Check for API errors
                if isinstance(response_data, dict) and response_data.get('code') != '00000':
                    error_msg = response_data.get('msg', 'Unknown API error')
                    logger.error(f"BitGet API error: {error_msg}")
                    return {'success': False, 'error': error_msg}
                    
                return response_data
        except Exception as e:
            logger.error(f"Request error: {str(e)}")
            return {'success': False, 'error': str(e)}
            
    async def get_positions(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Get positions for a specific symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            
        Returns:
            List of position dictionaries
        """
        endpoint = '/api/mix/v1/position/singlePosition'
        params = {'symbol': symbol, 'marginCoin': 'USDT'}
        
        # In demo mode, return mock data
        if self.is_demo:
            return self._generate_mock_positions(symbol)
            
        try:
            response = await self._request('GET', endpoint, params=params)
            
            if not response or not isinstance(response, dict):
                logger.error(f"Invalid response for positions: {response}")
                return []
                
            data = response.get('data', [])
            
            # Filter for active positions only
            active_positions = []
            for pos in data:
                if float(pos.get('total', 0)) > 0:
                    active_positions.append(pos)
                    
            return active_positions
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return []
            
    async def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance information.
        
        Returns:
            Account balance dictionary
        """
        endpoint = '/api/mix/v1/account/accounts'
        params = {'productType': 'umcbl'}
        
        # In demo mode, return mock data
        if self.is_demo:
            return self._generate_mock_account_balance()
            
        try:
            response = await self._request('GET', endpoint, params=params)
            
            if not response or not isinstance(response, dict):
                logger.error(f"Invalid response for account balance: {response}")
                return {}
                
            data = response.get('data', [])
            
            # Find USDT account
            usdt_account = None
            for account in data:
                if account.get('marginCoin') == 'USDT':
                    usdt_account = account
                    break
                    
            if not usdt_account:
                return {}
                
            return {
                'total': usdt_account.get('equity', 0),
                'available_balance': usdt_account.get('available', 0),
                'margin': usdt_account.get('locked', 0),
                'unrealized_pnl': usdt_account.get('unrealizedPL', 0)
            }
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            return {}
            
    async def get_current_price(self, symbol: str) -> float:
        """
        Get current price for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            
        Returns:
            Current price
        """
        endpoint = '/api/mix/v1/market/ticker'
        params = {'symbol': symbol}
        
        # In demo mode, return a mock price
        if self.is_demo:
            if 'BTC' in symbol:
                return random.uniform(63000, 65000)
            elif 'ETH' in symbol:
                return random.uniform(3000, 3200)
            else:
                return random.uniform(100, 1000)
                
        try:
            response = await self._request('GET', endpoint, params=params)
            
            if not response or not isinstance(response, dict):
                logger.error(f"Invalid response for ticker: {response}")
                return 0.0
                
            data = response.get('data', {})
            price = float(data.get('last', 0))
            
            return price
        except Exception as e:
            logger.error(f"Error getting current price: {e}")
            return 0.0
            
    async def create_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> Dict[str, Any]:
        """
        Create a new order.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: Order side ('buy' or 'sell')
            order_type: Order type ('limit' or 'market')
            quantity: Order quantity
            price: Order price (required for limit orders)
            
        Returns:
            Order response dictionary
        """
        endpoint = '/api/mix/v1/order/placeOrder'
        
        # Required for BitGet
        margin_coin = 'USDT'
        
        # Map side to BitGet format
        bitget_side = '1' if side.lower() == 'buy' else '2'
        
        # Map order type to BitGet format
        bitget_order_type = '1' if order_type.lower() == 'limit' else '2'
        
        data = {
            'symbol': symbol,
            'marginCoin': margin_coin,
            'size': str(quantity),
            'side': bitget_side,
            'orderType': bitget_order_type
        }
        
        # Add price for limit orders
        if order_type.lower() == 'limit' and price is not None:
            data['price'] = str(price)
            
        # In demo mode, return mock data
        if self.is_demo:
            logger.info(f"DEMO MODE: Would create order: {data}")
            return {'success': True, 'order_id': f'demo_{int(time.time())}'}
            
        try:
            response = await self._request('POST', endpoint, data=data)
            return response
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return {'success': False, 'error': str(e)}
            
    def _generate_mock_positions(self, symbol: str) -> List[Dict[str, Any]]:
        """Generate mock position data for testing."""
        # Only generate for BTC and ETH in this simple mock
        if 'BTC' not in symbol and 'ETH' not in symbol:
            return []
            
        base_price = 64000 if 'BTC' in symbol else 3200
        current_price = base_price * (1 + random.uniform(-0.05, 0.05))
        
        # Generate a random position
        side = random.choice(['long', 'short'])
        size = random.uniform(0.01, 0.5) if 'BTC' in symbol else random.uniform(0.1, 5.0)
        leverage = random.choice([1, 3, 5, 10])
        entry_price = current_price * (1 + random.uniform(-0.02, 0.02))
        
        # Calculate PnL
        if side == 'long':
            unrealized_pnl = size * (current_price - entry_price)
        else:
            unrealized_pnl = size * (entry_price - current_price)
            
        return [{
            'symbol': symbol,
            'side': side,
            'leverage': str(leverage),
            'total': str(size),
            'averageOpenPrice': str(entry_price),
            'marketPrice': str(current_price),
            'unrealizedPL': str(unrealized_pnl)
        }]
        
    def _generate_mock_account_balance(self) -> Dict[str, Any]:
        """Generate mock account balance data for testing."""
        total_balance = random.uniform(5000, 20000)
        margin_used = total_balance * random.uniform(0.1, 0.4)
        available_balance = total_balance - margin_used
        unrealized_pnl = random.uniform(-500, 500)
        
        return {
            'total': str(total_balance),
            'available_balance': str(available_balance),
            'margin': str(margin_used),
            'unrealized_pnl': str(unrealized_pnl)
        }

# Example usage
async def example():
    """Example usage of the BitGetClient."""
    # Initialize client
    client = BitGetClient(
        api_key=os.environ.get('BITGET_API_KEY', ''),
        api_secret=os.environ.get('BITGET_API_SECRET', ''),
        passphrase=os.environ.get('BITGET_PASSPHRASE', ''),
        is_demo=True  # Use demo mode for testing
    )
    
    # Get positions
    positions = await client.get_positions('BTCUSDT')
    print(f"Positions: {positions}")
    
    # Get account balance
    balance = await client.get_account_balance()
    print(f"Account Balance: {balance}")
    
    # Get current price
    price = await client.get_current_price('BTCUSDT')
    print(f"Current BTC Price: ${price}")
    
    # Close session
    await client._close_session()

if __name__ == '__main__':
    asyncio.run(example()) 