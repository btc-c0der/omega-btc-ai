"""
Test suite for BitGet CCXT order-related functionality.
Tests order placement, modification, and cancellation methods.
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
TEST_STOP_PRICE = 49000.0
TEST_TAKE_PROFIT_PRICE = 51000.0
TEST_ORDER_ID = "test_order_id"

@pytest.fixture
def mock_ccxt(mocker):
    """Create a mock CCXT instance."""
    mock = MagicMock()
    
    # Mock order response
    mock_order_response = {
        "id": TEST_ORDER_ID,
        "symbol": TEST_SYMBOL,
        "side": "buy",
        "type": "market",
        "amount": TEST_AMOUNT,
        "price": TEST_PRICE,
        "status": "open",
        "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
    }
    
    # Mock position response
    mock_position_response = [
        {
            "id": "test_position_id",
            "symbol": TEST_SYMBOL,
            "side": "long",
            "contracts": TEST_AMOUNT,
            "contractSize": 1,
            "entryPrice": TEST_PRICE,
            "leverage": 10,
            "unrealizedPnl": 0,
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
        },
        {
            "id": "test_position_id_2",
            "symbol": TEST_SYMBOL,
            "side": "short",
            "contracts": TEST_AMOUNT / 2,
            "contractSize": 1,
            "entryPrice": TEST_PRICE,
            "leverage": 10,
            "unrealizedPnl": 0,
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
        }
    ]
    
    # Mock orders list
    mock_orders = [
        {
            "id": "sl_order_id",
            "symbol": TEST_SYMBOL,
            "side": "sell",
            "type": "stop",
            "amount": TEST_AMOUNT,
            "price": None,
            "status": "open",
            "params": {"stopLoss": True, "stopPrice": TEST_STOP_PRICE},
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
        },
        {
            "id": "tp_order_id",
            "symbol": TEST_SYMBOL,
            "side": "sell",
            "type": "limit",
            "amount": TEST_AMOUNT,
            "price": TEST_TAKE_PROFIT_PRICE,
            "status": "open",
            "params": {"takeProfit": True, "takeProfitPrice": TEST_TAKE_PROFIT_PRICE},
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
        }
    ]
    
    # Mock candle data
    mock_candles = [
        [int(datetime.now(timezone.utc).timestamp() * 1000), 49000, 50500, 48500, 50000, 100],  # [timestamp, open, high, low, close, volume]
        [int(datetime.now(timezone.utc).timestamp() * 1000) - 3600000, 48000, 49500, 47500, 49000, 120],
    ]
    
    # Set up mock methods
    mock.create_order = AsyncMock(return_value=mock_order_response)
    mock.fetch_positions = AsyncMock(return_value=mock_position_response)
    mock.fetch_open_orders = AsyncMock(return_value=mock_orders)
    mock.cancel_order = AsyncMock(return_value={"id": TEST_ORDER_ID, "status": "canceled"})
    mock.fetch_ohlcv = AsyncMock(return_value=mock_candles)
    mock.load_markets = AsyncMock(return_value={})
    mock.fetch_position_mode = AsyncMock(return_value={'hedged': True})
    mock.set_position_mode = AsyncMock(return_value={'success': True})
    mock.set_leverage = AsyncMock(return_value={'success': True})
    mock.set_margin_mode = AsyncMock(return_value={'success': True})
    
    return mock

@pytest.fixture
def bitget_ccxt(mock_ccxt):
    """Create a BitGetCCXT instance with mock CCXT."""
    instance = BitGetCCXT()
    instance.exchange = mock_ccxt
    return instance

@pytest.mark.asyncio
async def test_place_order(bitget_ccxt):
    """Test placing a market order."""
    logger.info("Testing order placement")
    order = await bitget_ccxt.place_order(
        symbol=TEST_SYMBOL,
        side="buy",
        amount=TEST_AMOUNT,
        order_type="market"
    )
    
    assert order['id'] == TEST_ORDER_ID
    assert order['symbol'] == TEST_SYMBOL
    assert order['side'] == "buy"
    assert order['type'] == "market"
    assert order['amount'] == TEST_AMOUNT
    bitget_ccxt.exchange.create_order.assert_called_once()

@pytest.mark.asyncio
async def test_place_stop_loss(bitget_ccxt):
    """Test placing a stop loss order."""
    logger.info("Testing stop loss order placement")
    order = await bitget_ccxt.place_stop_loss(
        symbol=TEST_SYMBOL,
        side="sell",
        amount=TEST_AMOUNT,
        stop_price=TEST_STOP_PRICE,
        position_side="long"
    )
    
    assert order['id'] == TEST_ORDER_ID
    assert order['symbol'] == TEST_SYMBOL
    bitget_ccxt.exchange.create_order.assert_called_once()

@pytest.mark.asyncio
async def test_place_take_profit(bitget_ccxt):
    """Test placing a take profit order."""
    logger.info("Testing take profit order placement")
    order = await bitget_ccxt.place_take_profit(
        symbol=TEST_SYMBOL,
        side="sell",
        amount=TEST_AMOUNT,
        take_profit_price=TEST_TAKE_PROFIT_PRICE,
        position_side="long"
    )
    
    assert order['id'] == TEST_ORDER_ID
    assert order['symbol'] == TEST_SYMBOL
    bitget_ccxt.exchange.create_order.assert_called_once()

@pytest.mark.asyncio
async def test_get_positions(bitget_ccxt):
    """Test retrieving positions."""
    logger.info("Testing position retrieval")
    positions = await bitget_ccxt.get_positions(TEST_SYMBOL)
    
    assert len(positions) == 2
    assert positions[0]['symbol'] == TEST_SYMBOL
    assert positions[0]['side'] == "long"
    assert positions[0]['contracts'] == TEST_AMOUNT
    bitget_ccxt.exchange.fetch_positions.assert_called_once()

@pytest.mark.asyncio
async def test_get_stop_loss_orders(bitget_ccxt):
    """Test retrieving stop loss orders."""
    logger.info("Testing stop loss orders retrieval")
    orders = await bitget_ccxt.get_stop_loss_orders(TEST_SYMBOL)
    
    assert len(orders) == 1
    assert orders[0]['params']['stopLoss'] is True
    assert orders[0]['params']['stopPrice'] == TEST_STOP_PRICE

@pytest.mark.asyncio
async def test_get_take_profit_orders(bitget_ccxt):
    """Test retrieving take profit orders."""
    logger.info("Testing take profit orders retrieval")
    orders = await bitget_ccxt.get_take_profit_orders(TEST_SYMBOL)
    
    assert len(orders) == 1
    assert orders[0]['params']['takeProfit'] is True
    assert orders[0]['params']['takeProfitPrice'] == TEST_TAKE_PROFIT_PRICE

@pytest.mark.asyncio
async def test_cancel_order(bitget_ccxt):
    """Test cancelling an order."""
    logger.info("Testing order cancellation")
    result = await bitget_ccxt.cancel_order(TEST_ORDER_ID, TEST_SYMBOL)
    
    assert result['id'] == TEST_ORDER_ID
    assert result['status'] == "canceled"
    bitget_ccxt.exchange.cancel_order.assert_called_once()

@pytest.mark.asyncio
async def test_get_open_orders(bitget_ccxt):
    """Test retrieving open orders."""
    logger.info("Testing open orders retrieval")
    orders = await bitget_ccxt.get_open_orders(TEST_SYMBOL)
    
    assert len(orders) == 2
    assert any(order['params'].get('stopLoss', False) for order in orders)
    assert any(order['params'].get('takeProfit', False) for order in orders)
    bitget_ccxt.exchange.fetch_open_orders.assert_called_once()

@pytest.mark.asyncio
async def test_fibonacci_levels(bitget_ccxt):
    """Test calculating Fibonacci levels."""
    logger.info("Testing Fibonacci levels calculation")
    levels = await bitget_ccxt.get_fibonacci_levels(TEST_SYMBOL)
    
    assert '0' in levels
    assert '0.236' in levels
    assert '0.382' in levels
    assert '0.5' in levels
    assert '0.618' in levels
    assert '0.786' in levels
    assert '1' in levels
    
    # Verify the calculation is correct
    high = 50500  # From mock candle data
    low = 47500   # From mock candle data
    diff = high - low
    assert levels['0'] == low
    assert levels['0.5'] == low + diff * 0.5
    assert levels['1'] == high

@pytest.mark.asyncio
async def test_fetch_ohlcv(bitget_ccxt):
    """Test retrieving OHLCV data."""
    logger.info("Testing OHLCV data retrieval")
    candles = await bitget_ccxt.fetch_ohlcv(TEST_SYMBOL, timeframe="1h", limit=100)
    
    assert len(candles) == 2
    assert len(candles[0]) == 6  # Each candle should have 6 elements
    assert candles[0][4] == 50000  # Close price
    bitget_ccxt.exchange.fetch_ohlcv.assert_called_once()

@pytest.mark.asyncio
async def test_close_position(bitget_ccxt):
    """Test closing a position."""
    logger.info("Testing position closure")
    with patch.object(bitget_ccxt, 'fetch_positions', AsyncMock(return_value=bitget_ccxt.exchange.fetch_positions.return_value)):
        with patch.object(bitget_ccxt, 'place_order', AsyncMock(return_value={"id": "close_order_id"})):
            result = await bitget_ccxt.close_position(TEST_SYMBOL, "long")
            
            assert result['id'] == "close_order_id"
            bitget_ccxt.place_order.assert_called_once() 