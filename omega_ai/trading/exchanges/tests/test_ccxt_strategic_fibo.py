"""
Test suite for CCXT Strategic Fibonacci Trader.
"""

import pytest
import asyncio
from typing import Dict, Any
from ..ccxt_strategic_fibo_trader import CCXTStrategicFiboTrader

@pytest.fixture
async def trader():
    """Create a CCXT strategic Fibonacci trader instance for testing."""
    trader = CCXTStrategicFiboTrader(
        symbol="BTCUSDT",
        initial_capital=24.0,
        leverage=11,
        use_testnet=True
    )
    await trader.initialize()
    yield trader
    await trader.stop_trading()

@pytest.mark.asyncio
async def test_initialization(trader):
    """Test trader initialization."""
    assert trader.symbol == "BTCUSDT"
    assert trader.initial_capital == 24.0
    assert trader.leverage == 11
    assert trader.use_testnet is True
    assert trader.is_running is False
    assert trader.current_price == 0.0
    assert isinstance(trader.fib_levels, dict)

@pytest.mark.asyncio
async def test_market_data_update(trader):
    """Test market data update and Fibonacci level calculation."""
    await trader.update_market_data()
    assert trader.current_price > 0
    assert len(trader.fib_levels) > 0
    assert all(isinstance(price, float) for price in trader.fib_levels.values())

@pytest.mark.asyncio
async def test_entry_signals(trader):
    """Test entry signal generation."""
    # Update market data first
    await trader.update_market_data()
    
    # Check entry signals
    signal = await trader.check_entry_signals()
    assert signal is None  # Should be None if no positions and price not at Fibonacci level
    
    # Test with price at a Fibonacci level
    trader.current_price = trader.fib_levels['0.382']
    signal = await trader.check_entry_signals()
    assert signal is not None
    assert signal["side"] in ["buy", "sell"]
    assert signal["price"] == trader.current_price
    assert signal["level"] in trader.fib_levels

@pytest.mark.asyncio
async def test_exit_signals(trader):
    """Test exit signal generation."""
    # Create a mock position
    position = {
        "side": "long",
        "entryPrice": 50000.0,
        "contracts": 0.001
    }
    
    # Test stop loss
    trader.current_price = 49500.0  # 1% below entry
    should_exit = await trader.check_exit_signals(position)
    assert should_exit is True
    
    # Test take profit
    trader.current_price = 51000.0  # 2% above entry
    should_exit = await trader.check_exit_signals(position)
    assert should_exit is True
    
    # Test Fibonacci level exit
    trader.current_price = trader.fib_levels['0.618']  # Above 0.5 for long position
    should_exit = await trader.check_exit_signals(position)
    assert should_exit is True

@pytest.mark.asyncio
async def test_trade_execution(trader):
    """Test trade execution."""
    # Create a mock signal
    signal = {
        "side": "buy",
        "price": 50000.0,
        "level": "0.382"
    }
    
    # Set current price
    trader.current_price = signal["price"]
    
    # Execute trade
    await trader.execute_trade(signal)
    
    # Verify position was opened
    positions = await trader.exchange.get_positions(f"{trader.symbol}/USDT:USDT")
    open_positions = [p for p in positions if p.get('contracts', 0) > 0]
    assert len(open_positions) > 0

@pytest.mark.asyncio
async def test_position_closure(trader):
    """Test position closure."""
    # Create a mock position
    position = {
        "side": "long",
        "entryPrice": 50000.0,
        "contracts": 0.001,
        "unrealizedPnl": 100.0
    }
    
    # Close position
    await trader.close_position(position)
    
    # Verify position was closed
    positions = await trader.exchange.get_positions(f"{trader.symbol}/USDT:USDT")
    open_positions = [p for p in positions if p.get('contracts', 0) > 0]
    assert len(open_positions) == 0

@pytest.mark.asyncio
async def test_trading_cycle(trader):
    """Test complete trading cycle."""
    # Start trading
    trader.is_running = True
    
    # Run one iteration
    await trader.update_market_data()
    positions = await trader.exchange.get_positions(f"{trader.symbol}/USDT:USDT")
    open_positions = [p for p in positions if p.get('contracts', 0) > 0]
    
    # Check for entries if no open positions
    if not open_positions:
        entry_signal = await trader.check_entry_signals()
        if entry_signal:
            await trader.execute_trade(entry_signal)
    
    # Handle open positions
    for position in open_positions:
        if await trader.check_exit_signals(position):
            await trader.close_position(position)
    
    # Verify trading state
    assert trader.is_running is True
    assert trader.current_price > 0
    assert isinstance(trader.fib_levels, dict) 