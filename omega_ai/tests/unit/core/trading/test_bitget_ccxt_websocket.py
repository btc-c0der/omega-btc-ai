"""
Test suite for BitGet CCXT websocket functionality.
Tests the websocket-related methods used for real-time data.
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

@pytest.fixture
def mock_ccxt_pro(mocker):
    """Create a mock CCXT Pro instance."""
    mock = MagicMock()
    
    # Mock order update
    mock_order_update = [
        {
            "id": "test_order_id",
            "symbol": TEST_SYMBOL,
            "side": "buy",
            "type": "market",
            "status": "filled",
            "filled": 0.1,
            "remaining": 0,
            "cost": 5000,
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
        }
    ]
    
    # Mock ticker update
    mock_ticker_update = {
        "symbol": TEST_SYMBOL,
        "last": 50000.0,
        "bid": 49990.0,
        "ask": 50010.0,
        "high": 50500.0,
        "low": 49500.0,
        "volume": 100.0,
        "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
    }
    
    # Set up mock methods for websocket
    mock.watch_orders = AsyncMock(return_value=mock_order_update)
    mock.watch_ticker = AsyncMock(return_value=mock_ticker_update)
    mock.close = AsyncMock()
    
    return mock

@pytest.fixture
def mock_ccxt_rest(mocker):
    """Create a mock CCXT REST instance."""
    mock = MagicMock()
    
    # Set up mock methods for REST
    mock.close = AsyncMock()
    mock.load_markets = AsyncMock(return_value={})
    mock.fetch_position_mode = AsyncMock(return_value={'hedged': True})
    
    return mock

@pytest.fixture
def bitget_ccxt(mock_ccxt_rest, mock_ccxt_pro):
    """Create a BitGetCCXT instance with mock CCXT."""
    instance = BitGetCCXT()
    instance.exchange = mock_ccxt_rest
    instance.exchange_pro = mock_ccxt_pro
    return instance

@pytest.mark.asyncio
async def test_watch_orders(bitget_ccxt):
    """Test watching orders via websocket."""
    logger.info("Testing order watching via websocket")
    
    # Create a task for the watch_orders method that will be cancelled after a short time
    task = asyncio.create_task(bitget_ccxt.watch_orders())
    
    # Let it run briefly
    await asyncio.sleep(0.1)
    
    # Cancel the task
    task.cancel()
    
    # Try to await the cancelled task
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    # Verify that the watch_orders method was called
    bitget_ccxt.exchange_pro.watch_orders.assert_called_once()

@pytest.mark.asyncio
async def test_watch_orders_exception(bitget_ccxt):
    """Test exception handling in watch_orders."""
    logger.info("Testing exception handling in watch_orders")
    
    # Make the watch_orders method raise an exception
    bitget_ccxt.exchange_pro.watch_orders = AsyncMock(side_effect=Exception("Test error"))
    
    # Create a task for the watch_orders method that will be cancelled after a short time
    task = asyncio.create_task(bitget_ccxt.watch_orders())
    
    # Let it run briefly
    await asyncio.sleep(0.1)
    
    # Cancel the task
    task.cancel()
    
    # Try to await the cancelled task
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    # Verify that the watch_orders method was called
    bitget_ccxt.exchange_pro.watch_orders.assert_called_once()

@pytest.mark.asyncio
async def test_close_connections(bitget_ccxt):
    """Test closing both REST and websocket connections."""
    logger.info("Testing connection closure")
    
    await bitget_ccxt.close()
    
    # Verify that both close methods were called
    bitget_ccxt.exchange.close.assert_called_once()
    bitget_ccxt.exchange_pro.close.assert_called_once()

@pytest.mark.asyncio
async def test_cleanup_del(bitget_ccxt):
    """Test cleanup when object is destroyed."""
    logger.info("Testing cleanup on object destruction")
    
    # Create a new running event loop for testing __del__
    with patch('asyncio.create_task') as mock_create_task:
        # Trigger __del__
        bitget_ccxt.__del__()
        
        # Verify that create_task was called with close
        mock_create_task.assert_called_once()
        
        # Get the argument to create_task
        arg = mock_create_task.call_args[0][0]
        
        # Verify it's the coroutine from the close method
        assert arg.cr_code.co_name == 'close' 