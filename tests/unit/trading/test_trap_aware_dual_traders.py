#!/usr/bin/env python3

"""
Test suite for the Trap-Aware Dual Position Traders system.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
import asyncio
import sys

from omega_ai.trading.strategies.trap_aware_dual_traders import TrapAwareDualTraders
from omega_ai.utils.trap_probability_utils import (
    get_current_trap_probability,
    get_probability_components,
    get_detected_trap_info,
    get_probability_threshold,
    is_trap_likely
)

# Test constants
TEST_SYMBOL = "BTCUSDT"
TEST_PRICE = 50000.0
TEST_API_KEY = "test_api_key"
TEST_SECRET_KEY = "test_secret_key"
TEST_PASSPHRASE = "test_passphrase"

@pytest.fixture
def trap_aware_traders():
    """Create a TrapAwareDualTraders instance with mocked dependencies."""
    with patch('omega_ai.trading.exchanges.dual_position_traders.DirectionalBitGetTrader') as mock_directional, \
         patch('omega_ai.trading.exchanges.dual_position_traders.BitGetCCXT') as mock_exchange:
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
        
        # Setup mock exchange
        mock_exchange_instance = AsyncMock()
        mock_exchange_instance.get_market_ticker = AsyncMock(return_value={"last": TEST_PRICE})
        mock_exchange_instance.get_klines = AsyncMock(return_value=[])
        mock_exchange_instance.get_orderbook = AsyncMock(return_value={"bids": [], "asks": []})
        mock_exchange.return_value = mock_exchange_instance
        
        # Patch the send_telegram_alert function
        with patch('omega_ai.trading.strategies.trap_aware_dual_traders.send_telegram_alert', new_callable=AsyncMock) as mock_alert:
            # Create the trap-aware traders instance
            traders = TrapAwareDualTraders(
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
                short_sub_account="short_test",
                trap_probability_threshold=0.7,
                trap_alert_threshold=0.8,
                enable_trap_protection=True,
                enable_elite_exits=True,
                elite_exit_confidence=0.7
            )
            
            # Set the mocked traders
            traders.long_trader = long_mock
            traders.short_trader = short_mock
            
            yield traders, mock_alert

@pytest.mark.asyncio
async def test_trap_aware_traders_initialization(trap_aware_traders):
    """Test that TrapAwareDualTraders initializes correctly."""
    traders, _ = trap_aware_traders
    
    # Verify initialization parameters
    assert traders.trap_probability_threshold == 0.7
    assert traders.trap_alert_threshold == 0.8
    assert traders.enable_trap_protection is True
    assert traders.enable_elite_exits is True
    assert traders.elite_exit_confidence == 0.7
    assert traders.long_risk_multiplier == 1.0
    assert traders.short_risk_multiplier == 1.0
    
    # Verify elite exit strategy was initialized
    assert hasattr(traders, 'elite_exit_strategy')
    assert traders.elite_exit_strategy is not None

@pytest.mark.asyncio
async def test_check_for_traps(trap_aware_traders):
    """Test trap detection functionality."""
    traders, _ = trap_aware_traders
    
    # Mock trap probability utilities
    with patch('omega_ai.trading.strategies.trap_aware_dual_traders.is_trap_likely') as mock_is_likely, \
         patch('omega_ai.trading.strategies.trap_aware_dual_traders.get_current_trap_probability') as mock_prob, \
         patch('omega_ai.trading.strategies.trap_aware_dual_traders.get_probability_components') as mock_components:
        
        # Setup mock returns
        mock_is_likely.return_value = (True, "bull_trap", 0.85)
        mock_prob.return_value = 0.85
        mock_components.return_value = {
            "price_pattern": 0.8,
            "volume_spike": 0.7,
            "fibonacci_level": 0.9
        }
        
        # Call check_for_traps
        result = await traders.check_for_traps()
        
        # Verify result
        assert result["is_trap_likely"] is True
        assert result["trap_type"] == "bull_trap"
        assert result["confidence"] == 0.85
        assert result["probability"] == 0.85
        assert "components" in result
        assert "timestamp" in result

@pytest.mark.asyncio
async def test_adjust_trading_based_on_traps(trap_aware_traders):
    """Test trading adjustments based on detected traps."""
    traders, _ = trap_aware_traders
    
    # Test bull trap adjustment
    bull_trap_data = {
        "probability": 0.85,
        "trap_type": "bull_trap",
        "confidence": 0.85
    }
    await traders._adjust_trading_based_on_traps(bull_trap_data)
    assert traders.long_risk_multiplier == 0.5
    assert traders.short_risk_multiplier == 1.2
    
    # Test bear trap adjustment
    bear_trap_data = {
        "probability": 0.85,
        "trap_type": "bear_trap",
        "confidence": 0.85
    }
    await traders._adjust_trading_based_on_traps(bear_trap_data)
    assert traders.long_risk_multiplier == 1.2
    assert traders.short_risk_multiplier == 0.5
    
    # Test liquidity grab adjustment
    liquidity_data = {
        "probability": 0.85,
        "trap_type": "liquidity_grab",
        "confidence": 0.85
    }
    await traders._adjust_trading_based_on_traps(liquidity_data)
    assert traders.long_risk_multiplier == 0.7
    assert traders.short_risk_multiplier == 0.7

@pytest.mark.asyncio
async def test_send_trap_alert(trap_aware_traders):
    """Test trap alert functionality."""
    traders, mock_alert = trap_aware_traders
    
    # Test data
    trap_data = {
        "trap_type": "bull_trap",
        "probability": 0.85,
        "confidence": 0.85,
        "components": {
            "price_pattern": 0.8,
            "volume_spike": 0.7
        }
    }
    
    # Call _send_trap_alert
    await traders._send_trap_alert(trap_data)
    
    # Verify alert was sent
    mock_alert.assert_called_once()
    
    # Get alert message
    alert_msg = mock_alert.call_args[0][0]
    
    # Verify alert content
    assert "MARKET MAKER TRAP DETECTED" in alert_msg
    assert "🐂 Bull Trap" in alert_msg
    assert "85.0%" in alert_msg
    assert "Trading Recommendations" in alert_msg

@pytest.mark.asyncio
async def test_monitor_traps(trap_aware_traders):
    """Test trap monitoring functionality."""
    traders, _ = trap_aware_traders
    
    # Mock check_for_traps and _adjust_trading_based_on_traps
    with patch.object(traders, 'check_for_traps') as mock_check, \
         patch.object(traders, '_adjust_trading_based_on_traps') as mock_adjust:
        
        # Setup mock returns
        mock_check.return_value = {
            "probability": 0.85,
            "trap_type": "bull_trap",
            "confidence": 0.85
        }
        
        # Set running flag
        traders.running = True
        
        # Start monitoring task
        monitor_task = asyncio.create_task(traders._monitor_traps())
        
        # Let it run for a short time
        await asyncio.sleep(0.1)
        
        # Stop monitoring
        traders.running = False
        await monitor_task
        
        # Verify calls
        mock_check.assert_called()
        mock_adjust.assert_called_once()

@pytest.mark.asyncio
async def test_elite_exit_signals(trap_aware_traders):
    """Test elite exit signal detection and execution."""
    traders, _ = trap_aware_traders
    
    # Mock elite exit strategy
    mock_exit_signal = MagicMock()
    mock_exit_signal.confidence = 0.85
    mock_exit_signal.reasons = ["Fibonacci level reached", "Pattern detected"]
    
    with patch.object(traders.elite_exit_strategy, 'analyze_exit_opportunity', new_callable=AsyncMock) as mock_analyze, \
         patch.object(traders.elite_exit_strategy, 'execute_exit', new_callable=AsyncMock) as mock_execute:
        
        # Setup mock returns
        mock_analyze.return_value = mock_exit_signal
        mock_execute.return_value = True
        
        # Mock exchange
        traders.exchange = AsyncMock()
        traders.exchange.get_market_ticker.return_value = {"last": TEST_PRICE}
        
        # Test long position exit
        await traders._run_long_trader()
        
        # Verify calls
        mock_analyze.assert_called()
        mock_execute.assert_called_once()
        
        # Test short position exit
        await traders._run_short_trader()
        
        # Verify calls again
        assert mock_analyze.call_count == 2
        assert mock_execute.call_count == 2

@pytest.mark.asyncio
async def test_start_trading(trap_aware_traders):
    """Test trading system startup."""
    traders, _ = trap_aware_traders
    
    # Mock initialize and check_account_limit
    with patch.object(traders, 'initialize', new_callable=AsyncMock) as mock_init, \
         patch.object(traders, 'check_account_limit', new_callable=AsyncMock) as mock_check:
        
        # Setup mock returns
        mock_check.return_value = True
        
        # Start trading
        await traders.start_trading()
        
        # Verify calls
        mock_init.assert_called_once()
        mock_check.assert_called_once()
        
        # Verify tasks were created
        assert len(traders.tasks) == 4  # long, short, performance, traps

@pytest.mark.asyncio
async def test_parse_args():
    """Test command line argument parsing."""
    from omega_ai.trading.strategies.trap_aware_dual_traders import parse_args
    
    # Save original sys.argv
    original_argv = sys.argv
    
    try:
        # Test default arguments
        sys.argv = ['trap_aware_dual_traders.py']
        args = parse_args()
        assert args.symbol == "BTCUSDT"
        assert args.trap_probability_threshold == 0.7
        assert args.trap_alert_threshold == 0.8
        assert args.enable_elite_exits is False
        assert args.elite_exit_confidence == 0.7
        
        # Test custom arguments
        sys.argv = [
            'trap_aware_dual_traders.py',
            '--symbol', 'ETHUSDT',
            '--trap-probability-threshold', '0.8',
            '--trap-alert-threshold', '0.9',
            '--enable-elite-exits',
            '--elite-exit-confidence', '0.85'
        ]
        args = parse_args()
        assert args.symbol == "ETHUSDT"
        assert args.trap_probability_threshold == 0.8
        assert args.trap_alert_threshold == 0.9
        assert args.enable_elite_exits is True
        assert args.elite_exit_confidence == 0.85
        
    finally:
        # Restore original sys.argv
        sys.argv = original_argv 