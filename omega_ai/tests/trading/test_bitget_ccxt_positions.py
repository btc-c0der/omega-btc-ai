
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
Test suite for BitGet CCXT position management functionality.
Tests position retrieval, modification, and related methods.
"""

import pytest
import asyncio
import logging
from typing import Type, Union, Tuple, Dict, Any, List
from unittest.mock import AsyncMock, patch, MagicMock
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
from datetime import datetime, timezone
import ccxt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test configuration
TEST_SYMBOL = "BTC/USDT:USDT"  # CCXT standard format
TEST_AMOUNT = 0.1
TEST_PRICE = 50000.0
TEST_LEVERAGE = 5
TEST_MARGIN_MODE = "cross"  # or "isolated"

@pytest.fixture
def mock_ccxt(mocker):
    """Create a mock CCXT instance."""
    mock = MagicMock()
    
    # Mock position response
    mock_position_response = [
        {
            "id": "test_position_id",
            "symbol": TEST_SYMBOL,
            "side": "long",
            "contracts": TEST_AMOUNT,
            "contractSize": 1,
            "entryPrice": TEST_PRICE,
            "leverage": TEST_LEVERAGE,
            "marginMode": TEST_MARGIN_MODE,
            "unrealizedPnl": 100,
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
        },
        {
            "id": "test_position_id_2",
            "symbol": TEST_SYMBOL,
            "side": "short",
            "contracts": TEST_AMOUNT / 2,
            "contractSize": 1,
            "entryPrice": TEST_PRICE,
            "leverage": TEST_LEVERAGE,
            "marginMode": TEST_MARGIN_MODE,
            "unrealizedPnl": -50,
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
        }
    ]
    
    # Mock balance response
    mock_balance_response = {
        "info": {"some_exchange_specific_info": "value"},
        "USDT": {
            "free": 1000.0,
            "used": 200.0,
            "total": 1200.0
        },
        "BTC": {
            "free": 0.5,
            "used": 0.1,
            "total": 0.6
        }
    }
    
    # Set up mock methods
    mock.fetch_positions = AsyncMock(return_value=mock_position_response)
    mock.fetch_balance = AsyncMock(return_value=mock_balance_response)
    mock.set_leverage = AsyncMock(return_value={"success": True, "leverage": TEST_LEVERAGE})
    mock.set_margin_mode = AsyncMock(return_value={"success": True, "marginMode": TEST_MARGIN_MODE})
    mock.load_markets = AsyncMock(return_value={
        "BTC/USDT:USDT": {
            "id": "BTCUSDT_UMCBL",
            "symbol": "BTC/USDT:USDT",
            "base": "BTC",
            "quote": "USDT",
            "type": "swap",
            "active": True,
            "precision": {"amount": 4, "price": 2},
            "limits": {"amount": {"min": 0.0001, "max": 10}, "price": {"min": 1, "max": 100000}},
            "info": {}
        }
    })
    mock.fetch_position_mode = AsyncMock(return_value={'hedged': True})
    mock.set_position_mode = AsyncMock(return_value={'success': True})
    mock.close = AsyncMock()
    
    return mock

@pytest.fixture
def bitget_ccxt(mock_ccxt):
    """Create a BitGetCCXT instance with mock CCXT."""
    instance = BitGetCCXT()
    instance.exchange = mock_ccxt
    instance.exchange_pro = mock_ccxt  # For websocket methods
    return instance

@pytest.mark.asyncio
async def test_initialize(bitget_ccxt):
    """Test exchange initialization."""
    logger.info("Testing exchange initialization")
    await bitget_ccxt.initialize()
    
    # Check if methods were called
    bitget_ccxt.exchange.load_markets.assert_called_once()
    bitget_ccxt.exchange.fetch_position_mode.assert_called_once()

@pytest.mark.asyncio
async def test_set_hedge_mode(bitget_ccxt):
    """Test setting hedge mode."""
    logger.info("Testing hedge mode setting")
    result = await bitget_ccxt.set_hedge_mode()
    
    # Check if method was called
    bitget_ccxt.exchange.set_position_mode.assert_called_once()

@pytest.mark.asyncio
async def test_setup_trading_config(bitget_ccxt):
    """Test setting up trading configuration."""
    logger.info("Testing trading config setup")
    await bitget_ccxt.setup_trading_config(TEST_SYMBOL, leverage=TEST_LEVERAGE)
    
    # Check if methods were called - but don't assert_called_once as it's called twice (once for each side)
    assert bitget_ccxt.exchange.set_leverage.call_count == 2
    bitget_ccxt.exchange.set_margin_mode.assert_called_once()

@pytest.mark.asyncio
async def test_get_balance(bitget_ccxt):
    """Test retrieving account balance."""
    logger.info("Testing balance retrieval")
    balance = await bitget_ccxt.get_balance()
    
    # Check result
    assert balance['USDT']['free'] == 1000.0
    assert balance['BTC']['total'] == 0.6
    bitget_ccxt.exchange.fetch_balance.assert_called_once()

@pytest.mark.asyncio
async def test_get_positions(bitget_ccxt):
    """Test retrieving positions for a specific symbol."""
    logger.info("Testing position retrieval for specific symbol")
    positions = await bitget_ccxt.get_positions(TEST_SYMBOL)
    
    # Check result
    assert len(positions) == 2
    assert positions[0]['symbol'] == TEST_SYMBOL
    assert positions[0]['side'] == "long"
    assert positions[0]['contracts'] == TEST_AMOUNT
    bitget_ccxt.exchange.fetch_positions.assert_called_once()

@pytest.mark.asyncio
async def test_get_positions_all(bitget_ccxt):
    """Test retrieving all positions."""
    logger.info("Testing all positions retrieval")
    positions = await bitget_ccxt.get_positions()
    
    # Check result
    assert len(positions) == 2
    assert positions[0]['symbol'] == TEST_SYMBOL
    assert positions[1]['side'] == "short"
    bitget_ccxt.exchange.fetch_positions.assert_called_once()

@pytest.mark.asyncio
async def test_get_market_candles(bitget_ccxt):
    """Test retrieving market candles."""
    logger.info("Testing market candles retrieval")
    
    # Mock fetch_ohlcv method
    mock_candles = [
        [int(datetime.now(timezone.utc).timestamp() * 1000), 49000, 50500, 48500, 50000, 100],
        [int(datetime.now(timezone.utc).timestamp() * 1000) - 3600000, 48000, 49500, 47500, 49000, 120],
    ]
    bitget_ccxt.exchange.fetch_ohlcv = AsyncMock(return_value=mock_candles)
    
    candles = await bitget_ccxt.get_market_candles(TEST_SYMBOL, timeframe="1h", limit=100)
    
    # Check result
    assert len(candles) == 2
    assert len(candles[0]) == 6  # Each candle should have 6 elements
    bitget_ccxt.exchange.fetch_ohlcv.assert_called_once()

@pytest.mark.asyncio
async def test_format_symbol(bitget_ccxt):
    """Test symbol formatting."""
    logger.info("Testing symbol formatting")
    
    # Test with CCXT format
    assert bitget_ccxt._format_symbol("BTC/USDT:USDT") == "BTC/USDT:USDT"
    
    # Test with exchange format
    assert bitget_ccxt._format_symbol("BTCUSDT") == "BTC/USDT:USDT"
    
    # Test with None
    assert bitget_ccxt._format_symbol(None) == "BTC/USDT:USDT"
    
    # Test with empty string
    assert bitget_ccxt._format_symbol("") == "BTC/USDT:USDT"

@pytest.mark.asyncio
async def test_close_exchange_connection(bitget_ccxt):
    """Test closing exchange connection."""
    logger.info("Testing exchange connection closure")
    await bitget_ccxt.close()
    
    # Don't check for assert_called_once since there are multiple calls
    assert bitget_ccxt.exchange.close.called
    assert bitget_ccxt.exchange_pro.close.called

@pytest.mark.asyncio
async def test_get_market_candles_error_handling(bitget_ccxt):
    """Test error handling in get_market_candles."""
    logger.info("Testing error handling in market candles retrieval")
    
    # Mock fetch_ohlcv to raise an exception
    bitget_ccxt.exchange.fetch_ohlcv = AsyncMock(side_effect=Exception("Test error"))
    
    # Call the method
    candles = await bitget_ccxt.get_market_candles(TEST_SYMBOL)
    
    # Check that it returns an empty list on error
    assert candles == [] 