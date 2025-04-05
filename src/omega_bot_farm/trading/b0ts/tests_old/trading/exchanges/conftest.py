#!/usr/bin/env python3

"""
Common fixtures for CCXT exchange tests.

This module provides pytest fixtures for testing CCXT-related functionality across
different exchange implementations, with support for running tests without CCXT installed.
"""

import json
import pytest
import os
from typing import Dict, Any, Optional, List
from unittest.mock import Mock, MagicMock, patch, AsyncMock

# Test if CCXT is available
try:
    import ccxt
    HAVE_CCXT = True
except ImportError:
    HAVE_CCXT = False
    
# Skip tests that require CCXT if it's not available
requires_ccxt = pytest.mark.skipif(not HAVE_CCXT, reason="CCXT not installed")

# Default mock data for testing
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_FORMATTED_SYMBOL = "BTC/USDT:USDT"
DEFAULT_PRICE = 30000.0

# Setup environment variables for testing (if they don't exist)
if 'SYMBOL' not in os.environ:
    os.environ['SYMBOL'] = DEFAULT_SYMBOL
if 'BITGET_API_KEY' not in os.environ:
    os.environ['BITGET_API_KEY'] = 'test_api_key'
if 'BITGET_SECRET_KEY' not in os.environ:
    os.environ['BITGET_SECRET_KEY'] = 'test_secret_key'
if 'BITGET_PASSPHRASE' not in os.environ:
    os.environ['BITGET_PASSPHRASE'] = 'test_passphrase'
if 'USE_TESTNET' not in os.environ:
    os.environ['USE_TESTNET'] = 'true'

@pytest.fixture
def mock_ccxt_order():
    """Create a mock CCXT order object with to_dict method."""
    order = MagicMock()
    order_dict = {
        "id": "123456789",
        "clientOrderId": "test-client-order-id",
        "timestamp": 1625097600000,
        "datetime": "2023-04-02T12:00:00.000Z",
        "status": "closed",
        "symbol": DEFAULT_FORMATTED_SYMBOL,
        "type": "market",
        "timeInForce": "GTC",
        "side": "buy",
        "price": DEFAULT_PRICE,
        "amount": 0.01,
        "filled": 0.01,
        "remaining": 0.0,
        "cost": 300.0,
        "average": DEFAULT_PRICE,
        "trades": [],
        "fee": {"cost": 0.3, "currency": "USDT"},
    }
    
    order.to_dict.return_value = order_dict
    # Also make the order act like a dict for key access
    order.__getitem__ = lambda self, key: order_dict.get(key)
    order.get = lambda key, default=None: order_dict.get(key, default)
    
    return order

@pytest.fixture
def mock_ccxt_ticker():
    """Create a mock CCXT ticker object with to_dict method."""
    ticker = MagicMock()
    ticker_dict = {
        "symbol": DEFAULT_FORMATTED_SYMBOL,
        "timestamp": 1625097600000,
        "datetime": "2023-04-02T12:00:00.000Z",
        "high": 31000.0,
        "low": 29000.0,
        "bid": DEFAULT_PRICE,
        "bidVolume": 10.0,
        "ask": 30100.0,
        "askVolume": 5.0,
        "vwap": 30050.0,
        "open": 29500.0,
        "close": DEFAULT_PRICE, 
        "last": DEFAULT_PRICE,
        "previousClose": 29500.0,
        "change": 500.0,
        "percentage": 1.69,
        "average": 29750.0,
        "baseVolume": 1000.0,
        "quoteVolume": 30050000.0
    }
    
    ticker.to_dict.return_value = ticker_dict
    # Also make the ticker act like a dict for key access
    ticker.__getitem__ = lambda self, key: ticker_dict.get(key)
    ticker.get = lambda key, default=None: ticker_dict.get(key, default)
    
    return ticker

@pytest.fixture
def mock_ccxt_position():
    """Create a mock CCXT position object with to_dict method."""
    position = MagicMock()
    position_dict = {
        "info": {"some": "info"},
        "symbol": DEFAULT_FORMATTED_SYMBOL,
        "contracts": 0.01,
        "contractSize": 1.0,
        "entryPrice": DEFAULT_PRICE,
        "side": "long",
        "unrealizedPnl": 100.0,
        "leverage": 20.0,
        "collateral": 15.0,
        "notional": 300.0,
        "markPrice": 31000.0,
        "liquidationPrice": 28000.0,
        "marginMode": "isolated",
        "percentage": 3.33
    }
    
    position.to_dict.return_value = position_dict
    # Also make the position act like a dict for key access
    position.__getitem__ = lambda self, key: position_dict.get(key)
    position.get = lambda key, default=None: position_dict.get(key, default)
    
    return position

@pytest.fixture
def mock_ccxt_candles():
    """Create mock OHLCV candles data."""
    return [
        [1609459200000, 29000.0, 29100.0, 28900.0, 29050.0, 100.0],
        [1609462800000, 29050.0, 29200.0, 29000.0, 29150.0, 150.0],
    ]

@pytest.fixture
def mock_exchange_client(exchange_id="bitget"):
    """Create a mock ExchangeClientB0t that works without CCXT installed."""
    with patch("src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt", create=True):
        with patch("src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt_async", create=True):
            with patch("src.omega_bot_farm.trading.exchanges.ccxt_b0t.HAVE_CCXT", True):
                from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t
                
                client = MagicMock(spec=ExchangeClientB0t)
                client.exchange_id = exchange_id
                client.symbol_format = "{0}/USDT:USDT"
                client.symbol_suffix = "_UMCBL"
                client.use_testnet = True
                client.default_symbol = DEFAULT_SYMBOL
                
                # Mock the methods
                client.create_market_order.return_value = {"id": "12345"}
                client.create_order.return_value = {"id": "12345"}
                client.fetch_ticker.return_value = {"symbol": DEFAULT_FORMATTED_SYMBOL, "last": DEFAULT_PRICE}
                client.fetch_balance.return_value = {"free": {"USDT": 1000.0}, "used": {"USDT": 500.0}}
                client.fetch_positions.return_value = [{"symbol": DEFAULT_FORMATTED_SYMBOL, "side": "long", "contracts": 0.01}]
                client.fetch_ohlcv.return_value = [[1625097600000, 30000.0, 31000.0, 29000.0, 30500.0, 100.0]]
                client.close_position.return_value = {"closed_positions": [{"id": "12345"}]}
                client.set_leverage.return_value = {"leverage": 20}
                
                return client

@pytest.fixture
def ccxt_client():
    """Create a mock CCXT client with exchange for testing with CCXT."""
    with patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt'):
        with patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt_async'):
            with patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.HAVE_CCXT', True):
                from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t
                
                # Create a mock exchange
                mock_exchange = AsyncMock()
                
                # Create the client and set the exchange
                client = ExchangeClientB0t(exchange_id='bitget')
                client.exchange = mock_exchange
                return client

@pytest.fixture
def no_ccxt_client():
    """Create a client with CCXT not available for testing error cases."""
    with patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.HAVE_CCXT', False):
        from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t
        return ExchangeClientB0t(exchange_id='bitget')

@pytest.fixture
def ticker_dict():
    """Return a standard ticker dictionary for testing."""
    return {
        "symbol": DEFAULT_FORMATTED_SYMBOL,
        "timestamp": 1625097600000,
        "datetime": "2023-04-02T12:00:00.000Z",
        "high": 31000.0,
        "low": 29000.0,
        "bid": DEFAULT_PRICE,
        "ask": 30100.0,
        "last": DEFAULT_PRICE
    }

@pytest.fixture
def position_dict():
    """Return a standard position dictionary for testing."""
    return {
        "symbol": DEFAULT_FORMATTED_SYMBOL,
        "contracts": 0.01,
        "contractSize": 1.0,
        "entryPrice": DEFAULT_PRICE,
        "side": "long",
        "unrealizedPnl": 100.0,
        "leverage": 20.0
    }

@pytest.fixture
def mock_to_dict_functions():
    """Patch the to_dict function in ccxt_b0t module for testing."""
    with patch("src.omega_bot_farm.trading.exchanges.ccxt_b0t.to_dict") as mock_to_dict:
        def side_effect(obj):
            if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
                return obj.to_dict()
            if isinstance(obj, dict):
                return obj
            return {"mock": "data"}
            
        mock_to_dict.side_effect = side_effect
        yield mock_to_dict 