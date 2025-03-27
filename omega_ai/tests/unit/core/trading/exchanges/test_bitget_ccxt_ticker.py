"""
Test suite for BitGetCCXT ticker functionality.
"""

import pytest
from unittest.mock import AsyncMock, patch
from typing import Dict, Any
from datetime import datetime, timezone

from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT

# Test constants
TEST_SYMBOL = "BTCUSDT"
TEST_PRICE = 50000.0
TEST_HIGH = 51000.0
TEST_LOW = 49000.0
TEST_VOLUME = 1000.0

@pytest.fixture
def mock_ccxt():
    """Create a mock BitGetCCXT instance."""
    with patch('omega_ai.trading.exchanges.bitget_ccxt.BitGetCCXT') as mock:
        instance = AsyncMock()
        instance.exchange = AsyncMock()
        instance._format_symbol = lambda x: f"{x}/USDT:USDT"
        mock.return_value = instance
        yield instance

@pytest.mark.asyncio
async def test_get_market_ticker_success(mock_ccxt):
    """Test successful market ticker retrieval."""
    # Arrange
    expected_ticker = {
        'symbol': f"{TEST_SYMBOL}/USDT:USDT",
        'last': TEST_PRICE,
        'high': TEST_HIGH,
        'low': TEST_LOW,
        'volume': TEST_VOLUME,
        'timestamp': int(datetime.now(timezone.utc).timestamp() * 1000)
    }
    mock_ccxt.exchange.fetch_ticker.return_value = expected_ticker
    
    # Act
    ticker = await mock_ccxt.get_market_ticker(TEST_SYMBOL)
    
    # Assert
    assert ticker == expected_ticker
    mock_ccxt.exchange.fetch_ticker.assert_called_once_with(f"{TEST_SYMBOL}/USDT:USDT")

@pytest.mark.asyncio
async def test_get_market_ticker_empty_symbol(mock_ccxt):
    """Test market ticker retrieval with empty symbol."""
    # Act
    ticker = await mock_ccxt.get_market_ticker("")
    
    # Assert
    assert ticker is None
    mock_ccxt.exchange.fetch_ticker.assert_not_called()

@pytest.mark.asyncio
async def test_get_market_ticker_whitespace_symbol(mock_ccxt):
    """Test market ticker retrieval with whitespace symbol."""
    # Act
    ticker = await mock_ccxt.get_market_ticker("   ")
    
    # Assert
    assert ticker is None
    mock_ccxt.exchange.fetch_ticker.assert_not_called()

@pytest.mark.asyncio
async def test_get_market_ticker_format_error(mock_ccxt):
    """Test market ticker retrieval when symbol formatting fails."""
    # Arrange
    mock_ccxt._format_symbol = lambda x: None
    
    # Act
    ticker = await mock_ccxt.get_market_ticker(TEST_SYMBOL)
    
    # Assert
    assert ticker is None
    mock_ccxt.exchange.fetch_ticker.assert_not_called()

@pytest.mark.asyncio
async def test_get_market_ticker_fetch_error(mock_ccxt):
    """Test market ticker retrieval when fetch_ticker raises an exception."""
    # Arrange
    mock_ccxt.exchange.fetch_ticker.side_effect = Exception("API Error")
    
    # Act
    ticker = await mock_ccxt.get_market_ticker(TEST_SYMBOL)
    
    # Assert
    assert ticker is None
    mock_ccxt.exchange.fetch_ticker.assert_called_once_with(f"{TEST_SYMBOL}/USDT:USDT")

@pytest.mark.asyncio
async def test_get_market_ticker_none_symbol(mock_ccxt):
    """Test market ticker retrieval with None symbol."""
    # Act
    ticker = await mock_ccxt.get_market_ticker(None)
    
    # Assert
    assert ticker is None
    mock_ccxt.exchange.fetch_ticker.assert_not_called()

@pytest.mark.asyncio
async def test_get_market_ticker_special_characters(mock_ccxt):
    """Test market ticker retrieval with special characters in symbol."""
    # Arrange
    special_symbol = "BTC/USDT@USDT"
    expected_ticker = {
        'symbol': f"{special_symbol}/USDT:USDT",
        'last': TEST_PRICE,
        'high': TEST_HIGH,
        'low': TEST_LOW,
        'volume': TEST_VOLUME,
        'timestamp': int(datetime.now(timezone.utc).timestamp() * 1000)
    }
    mock_ccxt.exchange.fetch_ticker.return_value = expected_ticker
    
    # Act
    ticker = await mock_ccxt.get_market_ticker(special_symbol)
    
    # Assert
    assert ticker == expected_ticker
    mock_ccxt.exchange.fetch_ticker.assert_called_once_with(f"{special_symbol}/USDT:USDT") 