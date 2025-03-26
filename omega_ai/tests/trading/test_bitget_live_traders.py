"""
OMEGA BTC AI - BitGet Live Traders Test Suite
===========================================

Comprehensive test suite for the BitGet Live Traders module.
Ensures divine execution and flawless trading operations.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import Mock, patch, AsyncMock
import logging
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader

# Configure logging with divine energy
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Terminal colors for blessed output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

@pytest.fixture
def mock_trader():
    """Create a mock BitGetTrader with divine attributes."""
    trader = Mock(spec=BitGetTrader)
    trader.get_market_ticker = AsyncMock(return_value={"last": 50000.0})
    trader.get_positions = AsyncMock(return_value=[])
    trader.total_pnl = 0.0
    trader.win_rate = 0.0
    trader.calculate_sharpe_ratio = Mock(return_value=1.5)
    trader.calculate_max_drawdown = Mock(return_value=0.1)
    trader.update_price = AsyncMock()
    trader.manage_open_positions = AsyncMock()
    return trader

@pytest.fixture
def live_traders(mock_trader):
    """Initialize BitGetLiveTraders with mock traders."""
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetTrader', return_value=mock_trader):
        traders = BitGetLiveTraders(use_testnet=True)
        return traders

@pytest.mark.asyncio
async def test_initialization(live_traders):
    """Test divine initialization of live traders."""
    logger.info(f"{GREEN}Testing initialization with divine energy{RESET}")
    
    assert len(live_traders.traders) == 4  # Strategic, Aggressive, Newbie, Scalper
    assert all(isinstance(trader, BitGetTrader) for trader in live_traders.traders.values())
    assert live_traders.use_testnet is True
    assert live_traders.symbol == "BTCUSDT_UMCBL"
    assert live_traders.update_interval == 1.0

@pytest.mark.asyncio
async def test_trader_update(live_traders):
    """Test divine trader state updates."""
    logger.info(f"{GREEN}Testing trader updates with cosmic precision{RESET}")
    
    # Update trader states
    await live_traders.update_traders()
    
    # Verify each trader was updated
    for trader in live_traders.traders.values():
        trader.update_price.assert_called_once()
        trader.manage_open_positions.assert_called_once()

@pytest.mark.asyncio
async def test_performance_metrics(live_traders):
    """Test divine performance metrics calculation."""
    logger.info(f"{GREEN}Testing performance metrics with JAH BLESSING{RESET}")
    
    # Set up mock performance data
    for trader in live_traders.traders.values():
        trader.total_pnl = 100.0
        trader.win_rate = 0.6
        trader.calculate_sharpe_ratio.return_value = 2.0
        trader.calculate_max_drawdown.return_value = 0.15
    
    # Calculate metrics
    metrics = await live_traders.calculate_performance_metrics()
    
    assert metrics["total_pnl"] == 400.0  # 100 * 4 traders
    assert metrics["win_rate"] == 0.6
    assert metrics["sharpe_ratio"] == 2.0
    assert metrics["max_drawdown"] == 0.15

@pytest.mark.asyncio
async def test_stop_trading(live_traders):
    """Test divine shutdown of trading operations."""
    logger.info(f"{GREEN}Testing graceful shutdown with divine protection{RESET}")
    
    # Start trading
    live_traders.is_running = True
    
    # Stop trading
    await live_traders.stop_trading()
    
    assert live_traders.is_running is False
    for trader in live_traders.traders.values():
        trader.close_all_positions.assert_called_once()

@pytest.mark.asyncio
async def test_error_handling(live_traders):
    """Test divine error handling and recovery."""
    logger.info(f"{GREEN}Testing error handling with divine resilience{RESET}")
    
    # Simulate API error
    for trader in live_traders.traders.values():
        trader.get_market_ticker.side_effect = Exception("API Error")
    
    # Update should continue despite errors
    await live_traders.update_traders()
    
    # Verify system continues running
    assert live_traders.is_running is True

@pytest.mark.asyncio
async def test_main_loop(live_traders):
    """Test divine main trading loop."""
    logger.info(f"{GREEN}Testing main loop with cosmic energy{RESET}")
    
    # Start trading
    live_traders.is_running = True
    
    # Run one iteration
    await live_traders.main_loop()
    
    # Verify updates occurred
    for trader in live_traders.traders.values():
        trader.update_price.assert_called_once()
        trader.manage_open_positions.assert_called_once()

@pytest.mark.asyncio
async def test_position_management(live_traders):
    """Test divine position management."""
    logger.info(f"{GREEN}Testing position management with divine wisdom{RESET}")
    
    # Mock open positions
    mock_positions = [
        {"id": "1", "side": "LONG", "entry_price": 50000.0, "size": 0.1, "leverage": 10, "status": "OPEN"},
        {"id": "2", "side": "SHORT", "entry_price": 51000.0, "size": 0.1, "leverage": 10, "status": "OPEN"}
    ]
    
    for trader in live_traders.traders.values():
        trader.get_positions.return_value = mock_positions
    
    # Update positions
    await live_traders.update_traders()
    
    # Verify position management
    for trader in live_traders.traders.values():
        trader.manage_open_positions.assert_called_once()

@pytest.mark.asyncio
async def test_risk_management(live_traders):
    """Test divine risk management."""
    logger.info(f"{GREEN}Testing risk management with divine protection{RESET}")
    
    # Set up risk metrics
    for trader in live_traders.traders.values():
        trader.calculate_max_drawdown.return_value = 0.2
        trader.calculate_sharpe_ratio.return_value = 1.8
    
    # Calculate risk metrics
    metrics = await live_traders.calculate_performance_metrics()
    
    assert metrics["max_drawdown"] == 0.2
    assert metrics["sharpe_ratio"] == 1.8

@pytest.mark.asyncio
async def test_telegram_alerts(live_traders):
    """Test divine alert system."""
    logger.info(f"{GREEN}Testing alert system with divine communication{RESET}")
    
    # Mock alert sending
    with patch('omega_ai.alerts.telegram_market_report.send_telegram_alert') as mock_send:
        # Trigger an alert
        await live_traders.send_alert("Test Alert")
        mock_send.assert_called_once_with("Test Alert")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"]) 