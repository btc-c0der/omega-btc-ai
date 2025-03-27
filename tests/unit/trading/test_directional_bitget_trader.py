#!/usr/bin/env python3

"""
Test suite for the DirectionalBitGetTrader class.

This test suite verifies that the DirectionalBitGetTrader properly:
1. Initializes with a specified direction (long or short)
2. Filters signals based on the configured direction
3. Properly overrides the _check_new_entry method
4. Correctly passes through signals matching the configured direction

Author: OMEGA BTC AI Team
"""

import os
import sys
import pytest
import json
import asyncio
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock, AsyncMock

# Add project root to path for module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.trading.exchanges.dual_position_traders import DirectionalBitGetTrader
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT

# Constants for testing
TEST_SYMBOL = "BTCUSDT"
TEST_API_KEY = "test_api_key"
TEST_SECRET_KEY = "test_secret_key"
TEST_PASSPHRASE = "test_passphrase"
TEST_PRICE = 50000.0

# Terminal colors for blessed output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Fixtures
@pytest.fixture
def mock_bitget_ccxt():
    """Mock BitGet CCXT client for testing."""
    with patch('omega_ai.trading.exchanges.bitget_ccxt.BitGetCCXT') as mock_ccxt:
        # Setup mock methods
        mock_instance = AsyncMock()
        
        # Mock initialize method
        mock_instance.initialize = AsyncMock()
        
        # Mock get_market_ticker method
        mock_instance.get_market_ticker = AsyncMock(return_value={
            'symbol': f"{TEST_SYMBOL.replace('USDT', '')}/USDT:USDT",
            'last': TEST_PRICE,
            'high': TEST_PRICE * 1.05,
            'low': TEST_PRICE * 0.95,
            'vol': 1000.0,
            'timestamp': int(datetime.now(timezone.utc).timestamp() * 1000)
        })
        
        # Mock place_order method
        mock_instance.place_order = AsyncMock(return_value={
            'id': '123456789',
            'status': 'open',
            'symbol': f"{TEST_SYMBOL.replace('USDT', '')}/USDT:USDT",
            'side': 'buy',
            'price': TEST_PRICE,
            'amount': 0.1,
            'timestamp': int(datetime.now(timezone.utc).timestamp() * 1000)
        })
        
        # Mock get_positions method
        mock_instance.get_positions = AsyncMock(return_value=[])
        
        # Mock close_position method
        mock_instance.close_position = AsyncMock(return_value={
            'id': '123456789',
            'status': 'closed',
            'symbol': f"{TEST_SYMBOL.replace('USDT', '')}/USDT:USDT",
            'side': 'buy',
            'price': TEST_PRICE,
            'amount': 0.1,
            'timestamp': int(datetime.now(timezone.utc).timestamp() * 1000)
        })
        
        # Mock get_balance method
        mock_instance.get_balance = AsyncMock(return_value={
            'USDT': {'free': 1000.0, 'used': 0.0, 'total': 1000.0}
        })
        
        # Mock setup_trading_config method
        mock_instance.setup_trading_config = AsyncMock()
        
        # Mock close method
        mock_instance.close = AsyncMock()
        
        mock_ccxt.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def long_trader(mock_bitget_ccxt):
    """Create a long-only DirectionalBitGetTrader instance."""
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetCCXT', return_value=mock_bitget_ccxt):
        # Create trader with "long" direction
        trader = DirectionalBitGetTrader(
            direction="long",
            use_testnet=True,
            initial_capital=24.0,
            symbol=TEST_SYMBOL,
            api_key=TEST_API_KEY,
            secret_key=TEST_SECRET_KEY,
            passphrase=TEST_PASSPHRASE
        )
        return trader

@pytest.fixture
def short_trader(mock_bitget_ccxt):
    """Create a short-only DirectionalBitGetTrader instance."""
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetCCXT', return_value=mock_bitget_ccxt):
        # Create trader with "short" direction
        trader = DirectionalBitGetTrader(
            direction="short",
            use_testnet=True,
            initial_capital=24.0,
            symbol=TEST_SYMBOL,
            api_key=TEST_API_KEY,
            secret_key=TEST_SECRET_KEY,
            passphrase=TEST_PASSPHRASE
        )
        return trader

# Additional fixtures for dual position traders tests
@pytest.fixture
def mock_directional_trader():
    """Create a mock DirectionalBitGetTrader for testing."""
    with patch('omega_ai.trading.exchanges.dual_position_traders.DirectionalBitGetTrader') as mock_class:
        # Setup mock instance behavior
        mock_instance = AsyncMock()
        mock_instance.initialize = AsyncMock()
        mock_instance.start_trading = AsyncMock()
        mock_instance.stop_trading = AsyncMock()
        mock_instance.traders = {"strategic": AsyncMock()}
        mock_instance.traders["strategic"].get_balance = AsyncMock(return_value={
            "USDT": {"free": 1000.0, "used": 0.0, "total": 1000.0}
        })
        mock_instance.traders["strategic"].get_positions = AsyncMock(return_value=[
            {
                "symbol": f"{TEST_SYMBOL.replace('USDT', '')}/USDT:USDT",
                "side": "buy",
                "contracts": 0.1,
                "entryPrice": TEST_PRICE,
                "unrealizedPnl": 50.0,
                "realizedPnl": 25.0
            }
        ])
        
        # Make the mock class return the mock instance
        mock_class.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def dual_position_traders():
    """Create a BitGetDualPositionTraders instance with mocked traders."""
    with patch('omega_ai.trading.exchanges.dual_position_traders.DirectionalBitGetTrader') as mock_directional:
        # Setup mock instance behavior for both long and short traders
        long_mock = AsyncMock()
        long_mock.initialize = AsyncMock()
        long_mock.start_trading = AsyncMock()
        long_mock.stop_trading = AsyncMock()
        long_mock.traders = {"strategic": AsyncMock()}
        long_mock.traders["strategic"].get_balance = AsyncMock(return_value={
            "USDT": {"free": 1000.0, "used": 0.0, "total": 1000.0}
        })
        long_mock.traders["strategic"].get_positions = AsyncMock(return_value=[
            {
                "symbol": f"{TEST_SYMBOL.replace('USDT', '')}/USDT:USDT",
                "side": "buy",
                "contracts": 0.1,
                "entryPrice": TEST_PRICE,
                "unrealizedPnl": 50.0,
                "realizedPnl": 25.0
            }
        ])
        
        short_mock = AsyncMock()
        short_mock.initialize = AsyncMock()
        short_mock.start_trading = AsyncMock()
        short_mock.stop_trading = AsyncMock()
        short_mock.traders = {"strategic": AsyncMock()}
        short_mock.traders["strategic"].get_balance = AsyncMock(return_value={
            "USDT": {"free": 800.0, "used": 200.0, "total": 1000.0}
        })
        short_mock.traders["strategic"].get_positions = AsyncMock(return_value=[
            {
                "symbol": f"{TEST_SYMBOL.replace('USDT', '')}/USDT:USDT",
                "side": "sell",
                "contracts": 0.2,
                "entryPrice": TEST_PRICE,
                "unrealizedPnl": -25.0,
                "realizedPnl": 10.0
            }
        ])
        
        # Make the mock class return different instances for each call
        mock_directional.side_effect = [long_mock, short_mock]
        
        # Patch the send_telegram_alert function
        with patch('omega_ai.trading.exchanges.dual_position_traders.send_telegram_alert', new_callable=AsyncMock) as mock_alert:
            # Create the dual traders instance
            from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders
            traders = BitGetDualPositionTraders(
                use_testnet=True,
                long_capital=24.0,
                short_capital=24.0,
                symbol=TEST_SYMBOL,
                api_key=TEST_API_KEY,
                secret_key=TEST_SECRET_KEY,
                passphrase=TEST_PASSPHRASE,
                long_leverage=11,
                short_leverage=11,
                enable_pnl_alerts=True,
                long_sub_account="long_test",
                short_sub_account="short_test"
            )
            
            # Set the mocked traders
            traders.long_trader = long_mock
            traders.short_trader = short_mock
            
            yield traders, mock_alert

# Tests
@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_long_trader_initialization(long_trader):
    """Test that long trader initializes correctly with long direction."""
    assert long_trader.direction == "long"
    assert long_trader.symbol == TEST_SYMBOL
    assert long_trader.initial_capital == 24.0

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_short_trader_initialization(short_trader):
    """Test that short trader initializes correctly with short direction."""
    assert short_trader.direction == "short"
    assert short_trader.symbol == TEST_SYMBOL
    assert short_trader.initial_capital == 24.0

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_long_trader_accepts_long_signal(long_trader, mock_bitget_ccxt):
    """Test that long trader accepts long signals."""
    # Patch the BitGetLiveTraders parent class's _check_new_entry to return a long signal
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetLiveTraders._check_new_entry', new_callable=AsyncMock) as mock_parent_check:
        # Set up the mock to return a long signal
        mock_parent_check.return_value = {"side": "long", "price": TEST_PRICE}
        
        # Call the method on the DirectionalBitGetTrader instance
        result = await long_trader._check_new_entry(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the mock was called correctly
        mock_parent_check.assert_called_once_with(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the result was passed through without modification
        assert result == {"side": "long", "price": TEST_PRICE}

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_long_trader_filters_short_signal(long_trader, mock_bitget_ccxt):
    """Test that long trader filters out short signals."""
    # Patch the BitGetLiveTraders parent class's _check_new_entry to return a short signal
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetLiveTraders._check_new_entry', new_callable=AsyncMock) as mock_parent_check:
        # Set up the mock to return a short signal
        mock_parent_check.return_value = {"side": "short", "price": TEST_PRICE}
        
        # Call the method on the DirectionalBitGetTrader instance
        result = await long_trader._check_new_entry(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the mock was called correctly
        mock_parent_check.assert_called_once_with(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the short signal was filtered out
        assert result is None

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_short_trader_accepts_short_signal(short_trader, mock_bitget_ccxt):
    """Test that short trader accepts short signals."""
    # Patch the BitGetLiveTraders parent class's _check_new_entry to return a short signal
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetLiveTraders._check_new_entry', new_callable=AsyncMock) as mock_parent_check:
        # Set up the mock to return a short signal
        mock_parent_check.return_value = {"side": "short", "price": TEST_PRICE}
        
        # Call the method on the DirectionalBitGetTrader instance
        result = await short_trader._check_new_entry(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the mock was called correctly
        mock_parent_check.assert_called_once_with(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the result was passed through without modification
        assert result == {"side": "short", "price": TEST_PRICE}

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_short_trader_filters_long_signal(short_trader, mock_bitget_ccxt):
    """Test that short trader filters out long signals."""
    # Patch the BitGetLiveTraders parent class's _check_new_entry to return a long signal
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetLiveTraders._check_new_entry', new_callable=AsyncMock) as mock_parent_check:
        # Set up the mock to return a long signal
        mock_parent_check.return_value = {"side": "long", "price": TEST_PRICE}
        
        # Call the method on the DirectionalBitGetTrader instance
        result = await short_trader._check_new_entry(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the mock was called correctly
        mock_parent_check.assert_called_once_with(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the long signal was filtered out
        assert result is None

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_trader_handles_none_signal(long_trader, mock_bitget_ccxt):
    """Test that trader handles None signals correctly."""
    # Patch the BitGetLiveTraders parent class's _check_new_entry to return None
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetLiveTraders._check_new_entry', new_callable=AsyncMock) as mock_parent_check:
        # Set up the mock to return None
        mock_parent_check.return_value = None
        
        # Call the method on the DirectionalBitGetTrader instance
        result = await long_trader._check_new_entry(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the mock was called correctly
        mock_parent_check.assert_called_once_with(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify None was passed through
        assert result is None

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_trader_handles_malformed_signal(long_trader, mock_bitget_ccxt):
    """Test that trader handles malformed signals correctly."""
    # Patch the BitGetLiveTraders parent class's _check_new_entry to return a signal without a side
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetLiveTraders._check_new_entry', new_callable=AsyncMock) as mock_parent_check:
        # Set up the mock to return a malformed signal
        mock_parent_check.return_value = {"price": TEST_PRICE}
        
        # Call the method on the DirectionalBitGetTrader instance
        result = await long_trader._check_new_entry(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the mock was called correctly
        mock_parent_check.assert_called_once_with(mock_bitget_ccxt, TEST_PRICE)
        
        # Verify the malformed signal was passed through
        assert result == {"price": TEST_PRICE}

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_trader_initialization_with_real_method(mock_bitget_ccxt):
    """Test trader initialization with real method."""
    # Create a trader without mocking the parent _check_new_entry
    trader = DirectionalBitGetTrader(
        direction="long",
        use_testnet=True,
        initial_capital=24.0,
        symbol=TEST_SYMBOL,
        api_key=TEST_API_KEY,
        secret_key=TEST_SECRET_KEY,
        passphrase=TEST_PASSPHRASE
    )
    
    # Verify the trader was created correctly
    assert trader.direction == "long"
    assert trader.symbol == TEST_SYMBOL
    assert trader.initial_capital == 24.0

# Tests for BitGetDualPositionTraders
@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_dual_traders_initialization():
    """Test that BitGetDualPositionTraders initializes correctly."""
    with patch('omega_ai.trading.exchanges.dual_position_traders.DirectionalBitGetTrader') as mock_directional:
        # Setup mock instances
        long_mock = AsyncMock()
        long_mock.initialize = AsyncMock()
        short_mock = AsyncMock()
        short_mock.initialize = AsyncMock()
        
        # Make the mock class return different instances for each call
        mock_directional.side_effect = [long_mock, short_mock]
        
        # Create the dual traders instance
        from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders
        traders = BitGetDualPositionTraders(
            use_testnet=True,
            long_capital=24.0,
            short_capital=24.0,
            symbol=TEST_SYMBOL,
            api_key=TEST_API_KEY,
            secret_key=TEST_SECRET_KEY,
            passphrase=TEST_PASSPHRASE,
            long_leverage=11,
            short_leverage=11,
            enable_pnl_alerts=True,
            long_sub_account="long_test",
            short_sub_account="short_test"
        )
        
        # Initialize the traders
        await traders.initialize()
        
        # Verify DirectionalBitGetTrader was called correctly for long trader
        mock_directional.assert_any_call(
            direction="long",
            use_testnet=True,
            initial_capital=24.0,
            symbol=TEST_SYMBOL,
            api_key=TEST_API_KEY,
            secret_key=TEST_SECRET_KEY,
            passphrase=TEST_PASSPHRASE,
            strategic_only=True,
            enable_pnl_alerts=False,
            leverage=11
        )
        
        # Verify DirectionalBitGetTrader was called correctly for short trader
        mock_directional.assert_any_call(
            direction="short",
            use_testnet=True,
            initial_capital=24.0,
            symbol=TEST_SYMBOL,
            api_key=TEST_API_KEY,
            secret_key=TEST_SECRET_KEY,
            passphrase=TEST_PASSPHRASE,
            strategic_only=True,
            enable_pnl_alerts=False,
            leverage=11
        )
        
        # Verify initialize was called on both traders
        long_mock.initialize.assert_called_once()
        short_mock.initialize.assert_called_once()
        
        # Verify the traders were set correctly
        assert traders.long_trader == long_mock
        assert traders.short_trader == short_mock

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_dual_traders_check_account_limit(dual_position_traders):
    """Test that check_account_limit works correctly."""
    traders, _ = dual_position_traders
    
    # Test with no limit (0.0)
    traders.account_limit = 0.0
    result = await traders.check_account_limit()
    assert result is True
    
    # Test with high limit (above total balance)
    traders.account_limit = 3000.0
    result = await traders.check_account_limit()
    assert result is True
    
    # Test with low limit (below total balance)
    traders.account_limit = 1500.0
    result = await traders.check_account_limit()
    assert result is False
    
    # Test with very low limit (should return False)
    traders.account_limit = 500.0
    result = await traders.check_account_limit()
    assert result is False

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_dual_traders_get_trader_metrics(dual_position_traders):
    """Test that _get_trader_metrics works correctly."""
    traders, _ = dual_position_traders
    
    # Test getting metrics for long trader
    positions, pnl = await traders._get_trader_metrics(traders.long_trader)
    assert len(positions) == 1
    assert positions[0]["side"] == "buy"
    assert positions[0]["contracts"] == 0.1
    assert positions[0]["entryPrice"] == TEST_PRICE
    assert pnl == 50.0
    
    # Test getting metrics for short trader
    positions, pnl = await traders._get_trader_metrics(traders.short_trader)
    assert len(positions) == 1
    assert positions[0]["side"] == "sell"
    assert positions[0]["contracts"] == 0.2
    assert positions[0]["entryPrice"] == TEST_PRICE
    assert pnl == -25.0
    
    # Test with None trader
    positions, pnl = await traders._get_trader_metrics(None)
    assert positions == []
    assert pnl == 0.0

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_dual_traders_send_pnl_alert(dual_position_traders):
    """Test that _send_pnl_alert works correctly."""
    traders, mock_alert = dual_position_traders
    
    # Set up test data
    long_positions = [
        {
            "symbol": f"{TEST_SYMBOL.replace('USDT', '')}/USDT:USDT",
            "side": "buy",
            "contracts": 0.1,
            "entryPrice": TEST_PRICE,
            "unrealizedPnl": 50.0,
            "realizedPnl": 25.0
        }
    ]
    
    short_positions = [
        {
            "symbol": f"{TEST_SYMBOL.replace('USDT', '')}/USDT:USDT",
            "side": "sell",
            "contracts": 0.2,
            "entryPrice": TEST_PRICE,
            "unrealizedPnl": -25.0,
            "realizedPnl": 10.0
        }
    ]
    
    # Set last alert time to trigger immediate alert
    from datetime import datetime, timezone, timedelta
    traders.last_pnl_alert_time = datetime.now(timezone.utc) - timedelta(minutes=2)
    
    # Mock datetime.now to return a fixed time with seconds=0 (to pass the <5 seconds condition)
    fixed_now = datetime.now(timezone.utc).replace(second=0)
    with patch('omega_ai.trading.exchanges.dual_position_traders.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)  # To not break other datetime constructors
        
        # Call the method
        await traders._send_pnl_alert(long_positions, short_positions, 50.0, -25.0)
        
        # Verify alert was sent
        mock_alert.assert_called_once()
        
        # Get alert message
        alert_msg = mock_alert.call_args[0][0]
        
        # Verify alert contains expected information
        assert "DUAL POSITION TRADERS PNL UPDATE" in alert_msg
        assert "Long PnL: +50.00 USDT (1 positions)" in alert_msg
        assert "Short PnL: -25.00 USDT (1 positions)" in alert_msg
        assert "Total PnL: +25.00 USDT" in alert_msg
        assert "LONG POSITIONS" in alert_msg
        assert "SHORT POSITIONS" in alert_msg
    
    # Test with disabled alerts
    mock_alert.reset_mock()
    traders.enable_pnl_alerts = False
    await traders._send_pnl_alert(long_positions, short_positions, 50.0, -25.0)
    mock_alert.assert_not_called()

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_dual_traders_stop_trading(dual_position_traders):
    """Test that stop_trading works correctly."""
    traders, mock_alert = dual_position_traders
    
    # Set is_running to True
    traders.is_running = True
    
    # Call the method
    await traders.stop_trading()
    
    # Verify is_running was set to False
    assert traders.is_running is False
    
    # Verify both traders' stop_trading methods were called
    traders.long_trader.stop_trading.assert_called_once()
    traders.short_trader.stop_trading.assert_called_once()
    
    # Verify alert was sent
    mock_alert.assert_called_once()
    
    # Get alert message
    alert_msg = mock_alert.call_args[0][0]
    
    # Verify alert contains expected information
    assert "DUAL POSITION TRADERS SHUTDOWN" in alert_msg
    assert TEST_SYMBOL in alert_msg

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_dual_traders_start_trading(dual_position_traders):
    """Test that start_trading works correctly."""
    traders, _ = dual_position_traders
    
    # Create coroutine mocks for the internal methods
    run_long_mock = AsyncMock()
    run_short_mock = AsyncMock()
    monitor_mock = AsyncMock()
    
    # Patch the internal methods to return the mocks
    with patch.object(traders, '_run_long_trader', return_value=run_long_mock()):
        with patch.object(traders, '_run_short_trader', return_value=run_short_mock()):
            with patch.object(traders, '_monitor_performance', return_value=monitor_mock()):
                # Mock asyncio.gather to return a completed future
                with patch('omega_ai.trading.exchanges.dual_position_traders.asyncio.gather') as mock_gather:
                    mock_gather.return_value = asyncio.Future()
                    mock_gather.return_value.set_result(None)
                    
                    # Call the method
                    await traders.start_trading()
                    
                    # Verify gather was called with the appropriate methods
                    mock_gather.assert_called_once()
                    
                    # Check that is_running was set to True
                    assert traders.is_running is True

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_run_long_trader(dual_position_traders):
    """Test that _run_long_trader works correctly."""
    traders, _ = dual_position_traders
    
    # Call the method
    await traders._run_long_trader()
    
    # Verify that long_trader.initialize and start_trading were called
    traders.long_trader.initialize.assert_called_once()
    traders.long_trader.start_trading.assert_called_once()

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_run_short_trader(dual_position_traders):
    """Test that _run_short_trader works correctly."""
    traders, _ = dual_position_traders
    
    # Call the method
    await traders._run_short_trader()
    
    # Verify that short_trader.initialize and start_trading were called
    traders.short_trader.initialize.assert_called_once()
    traders.short_trader.start_trading.assert_called_once()

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_monitor_performance(dual_position_traders):
    """Test that _monitor_performance works correctly."""
    traders, _ = dual_position_traders
    
    # Set is_running to False to exit the loop immediately
    traders.is_running = False
    
    # Call the method
    await traders._monitor_performance()
    
    # Verify that is_running is still False
    assert traders.is_running is False
    
    # Now test with an account limit exceeded
    traders.is_running = True
    traders.account_limit = 500.0  # Set low limit that will be exceeded
    
    # Mock check_account_limit to return False once then set is_running to False to exit loop
    original_check_account_limit = traders.check_account_limit
    check_calls = 0
    
    async def mock_check_account_limit():
        nonlocal check_calls
        check_calls += 1
        if check_calls == 1:
            # First call returns False to trigger limit exceeded
            return False
        # Second call won't happen because is_running will be False
        return True
    
    traders.check_account_limit = mock_check_account_limit
    traders.stop_trading = AsyncMock()
    
    # Call the method
    await traders._monitor_performance()
    
    # Verify that is_running is False and stop_trading was called
    assert traders.is_running is False
    traders.stop_trading.assert_called_once()
    
    # Restore original method
    traders.check_account_limit = original_check_account_limit

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_dual_traders_error_handling():
    """Test error handling in BitGetDualPositionTraders."""
    # Test error in initialization
    with patch('omega_ai.trading.exchanges.dual_position_traders.DirectionalBitGetTrader') as mock_directional:
        # Make DirectionalBitGetTrader.initialize raise an exception
        mock_instance = AsyncMock()
        mock_instance.initialize = AsyncMock(side_effect=Exception("Test exception"))
        mock_directional.return_value = mock_instance
        
        # Create the dual traders instance
        from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders
        traders = BitGetDualPositionTraders(
            use_testnet=True,
            symbol=TEST_SYMBOL
        )
        
        # Call initialize and verify it raises the exception
        with pytest.raises(Exception, match="Test exception"):
            await traders.initialize()
    
    # Test error in check_account_limit
    with patch('omega_ai.trading.exchanges.dual_position_traders.DirectionalBitGetTrader') as mock_directional:
        # Create a mock instance that raises an exception on get_balance
        mock_instance = AsyncMock()
        mock_instance.traders = {"strategic": AsyncMock()}
        mock_instance.traders["strategic"].get_balance = AsyncMock(side_effect=Exception("Test balance exception"))
        mock_directional.return_value = mock_instance
        
        # Create the dual traders instance with the mock
        traders = BitGetDualPositionTraders(
            use_testnet=True,
            symbol=TEST_SYMBOL,
            account_limit=1000.0  # Set a limit to trigger the check
        )
        
        # Set the traders
        traders.long_trader = mock_instance
        traders.short_trader = mock_instance
        
        # Call check_account_limit and verify it handles the exception
        result = await traders.check_account_limit()
        assert result is True  # Should return True on error

@pytest.mark.asyncio
@pytest.mark.directional_trader
async def test_get_trader_metrics_error_handling(dual_position_traders):
    """Test error handling in _get_trader_metrics."""
    traders, _ = dual_position_traders
    
    # Create a mock trader that raises an exception
    mock_trader = AsyncMock()
    mock_trader.traders = {"strategic": AsyncMock()}
    mock_trader.traders["strategic"].get_positions = AsyncMock(side_effect=Exception("Test metrics exception"))
    
    # Call _get_trader_metrics with the mock
    positions, pnl = await traders._get_trader_metrics(mock_trader)
    
    # Verify the method handled the exception and returned empty results
    assert positions == []
    assert pnl == 0.0

# Run the tests if executed directly
if __name__ == "__main__":
    pytest.main(["-v", __file__]) 