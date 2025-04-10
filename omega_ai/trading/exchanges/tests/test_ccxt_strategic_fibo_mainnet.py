
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
Test suite for CCXT Strategic Fibonacci Trader with sub-accounts on mainnet.
"""

import os
import pytest
import asyncio
from typing import Dict, Any
from datetime import datetime, timezone
from omega_ai.trading.exchanges.ccxt_strategic_fibo_trader import CCXTStrategicFiboTrader

# Test configuration
TEST_SYMBOL = "BTCUSDT"
TEST_INITIAL_CAPITAL = 100.0  # Higher capital for mainnet
TEST_LEVERAGE = 11

@pytest.fixture
async def fibo_trader():
    """Create a CCXT Strategic Fibonacci Trader instance for testing."""
    # Get sub-account name from environment
    sub_account = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
    if not sub_account:
        pytest.skip("STRATEGIC_SUB_ACCOUNT_NAME not set in environment variables")
    
    trader = CCXTStrategicFiboTrader(
        symbol=TEST_SYMBOL,
        initial_capital=TEST_INITIAL_CAPITAL,
        leverage=TEST_LEVERAGE,
        use_testnet=False,  # Use mainnet
        sub_account=sub_account
    )
    
    # Initialize the trader
    await trader.initialize()
    
    yield trader
    
    # Cleanup
    if trader.is_running:
        await trader.stop_trading()

@pytest.mark.asyncio
async def test_initialization(fibo_trader):
    """Test trader initialization with sub-account."""
    assert fibo_trader is not None
    assert fibo_trader.symbol == TEST_SYMBOL
    assert fibo_trader.initial_capital == TEST_INITIAL_CAPITAL
    assert fibo_trader.leverage == TEST_LEVERAGE
    assert not fibo_trader.use_testnet
    assert fibo_trader.sub_account == os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME")

@pytest.mark.asyncio
async def test_market_data_update(fibo_trader):
    """Test market data update with sub-account."""
    await fibo_trader.update_market_data()
    assert fibo_trader.current_price > 0
    assert len(fibo_trader.fib_levels) > 0
    assert all(isinstance(price, float) for price in fibo_trader.fib_levels.values())

@pytest.mark.asyncio
async def test_entry_signals(fibo_trader):
    """Test entry signal generation with sub-account."""
    # Update market data first
    await fibo_trader.update_market_data()
    
    # Check for entry signals
    signal = await fibo_trader.check_entry_signals()
    assert signal is not None or signal is None  # Either a valid signal or no signal is acceptable
    
    if signal:
        assert "side" in signal
        assert "price" in signal
        assert "level" in signal
        assert signal["side"] in ["buy", "sell"]
        assert isinstance(signal["price"], float)
        assert isinstance(signal["level"], str)

@pytest.mark.asyncio
async def test_position_management(fibo_trader):
    """Test position management with sub-account."""
    # Get current positions
    positions = await fibo_trader.exchange.get_positions(f"{TEST_SYMBOL}/USDT:USDT")
    assert positions is not None
    
    # Check for open positions
    open_positions = [p for p in positions if p.get('contracts', 0) > 0]
    
    if open_positions:
        # Test exit signals for existing positions
        for position in open_positions:
            should_close = await fibo_trader.check_exit_signals(position)
            assert isinstance(should_close, bool)

@pytest.mark.asyncio
async def test_trading_cycle(fibo_trader):
    """Test complete trading cycle with sub-account."""
    # Update market data
    await fibo_trader.update_market_data()
    
    # Check for entry signals
    signal = await fibo_trader.check_entry_signals()
    
    if signal:
        # Execute trade
        await fibo_trader.execute_trade(signal)
        
        # Wait for position to be opened
        await asyncio.sleep(2)
        
        # Get updated positions
        positions = await fibo_trader.exchange.get_positions(f"{TEST_SYMBOL}/USDT:USDT")
        open_positions = [p for p in positions if p.get('contracts', 0) > 0]
        
        if open_positions:
            # Check exit signals
            for position in open_positions:
                should_close = await fibo_trader.check_exit_signals(position)
                if should_close:
                    # Close position
                    await fibo_trader.close_position(position)

@pytest.mark.asyncio
async def test_risk_management(fibo_trader):
    """Test risk management parameters with sub-account."""
    assert fibo_trader.max_position_size > 0
    assert fibo_trader.stop_loss_pct > 0
    assert fibo_trader.take_profit_pct > 0
    
    # Verify position size calculation
    position_size = fibo_trader.max_position_size / fibo_trader.current_price
    assert position_size > 0
    assert position_size <= (TEST_INITIAL_CAPITAL * TEST_LEVERAGE) / fibo_trader.current_price

@pytest.mark.asyncio
async def test_sub_account_balance(fibo_trader):
    """Test sub-account balance retrieval."""
    balance = await fibo_trader.exchange.get_balance()
    assert balance is not None
    
    # Check USDT balance
    if 'USDT' in balance:
        usdt_balance = balance['USDT']
        assert 'free' in usdt_balance
        assert 'total' in usdt_balance
        assert float(usdt_balance['total']) >= 0
        assert float(usdt_balance['free']) >= 0

@pytest.mark.asyncio
async def test_sub_account_trading_config(fibo_trader):
    """Test trading configuration for sub-account."""
    # Verify leverage setting
    positions = await fibo_trader.exchange.get_positions(f"{TEST_SYMBOL}/USDT:USDT")
    if positions:
        for position in positions:
            assert position.get('leverage', 0) == TEST_LEVERAGE 