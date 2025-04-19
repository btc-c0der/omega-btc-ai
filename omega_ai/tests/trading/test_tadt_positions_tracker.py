#!/usr/bin/env python3

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
Test suite for the OMEGA BTC AI TADT Positions Tracker.
Tests the functionality of tracking and analyzing positions for both sub-accounts.
"""

import pytest
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Any
from unittest.mock import AsyncMock, MagicMock, patch

from omega_ai.trading.strategies.trap_aware_dual_traders import TrapAwareDualTraders
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader

# Test data
MOCK_POSITION = {
    "symbol": "BTCUSDT_UMCBL",
    "side": "LONG",
    "contracts": "0.01",
    "entryPrice": "50000.0",
    "unrealizedPnl": "100.0",
    "realizedPnl": "50.0",
    "leverage": "5",
    "marginType": "cross",
    "marginBalance": "1000.0",
    "marginRatio": "0.1"
}

MOCK_POSITION_HISTORY = [
    {
        "id": "1",
        "symbol": "BTCUSDT_UMCBL",
        "side": "LONG",
        "entryPrice": "50000.0",
        "exitPrice": "51000.0",
        "size": "0.01",
        "leverage": "5",
        "entryTime": "2024-03-11T10:00:00Z",
        "exitTime": "2024-03-11T11:00:00Z",
        "pnl": "100.0",
        "status": "CLOSED"
    }
]

@pytest.fixture
def mock_bitget_trader():
    """Create a mock BitGetTrader instance."""
    trader = MagicMock(spec=BitGetTrader)
    trader.get_positions = AsyncMock(return_value=[MOCK_POSITION])
    trader.get_trade_history = AsyncMock(return_value=MOCK_POSITION_HISTORY)
    return trader

@pytest.fixture
def mock_live_traders():
    """Create a mock BitGetLiveTraders instance."""
    traders = MagicMock(spec=BitGetLiveTraders)
    traders.long_trader = MagicMock(spec=BitGetTrader)
    traders.short_trader = MagicMock(spec=BitGetTrader)
    return traders

@pytest.fixture
def tadt_tracker(mock_live_traders):
    """Create a TADT tracker instance with mocked dependencies."""
    with patch('omega_ai.trading.strategies.trap_aware_dual_traders.BitGetLiveTraders', return_value=mock_live_traders):
        tracker = TrapAwareDualTraders(
            trap_probability_threshold=0.7,
            trap_alert_threshold=0.8,
            enable_trap_protection=True,
            enable_elite_exits=True,
            elite_exit_confidence=0.7
        )
        return tracker

@pytest.mark.asyncio
async def test_initialize_tracker(tadt_tracker):
    """Test initialization of the TADT positions tracker."""
    await tadt_tracker.initialize()
    assert tadt_tracker.long_trader is not None
    assert tadt_tracker.short_trader is not None
    assert tadt_tracker.trap_probability_threshold == 0.7
    assert tadt_tracker.trap_alert_threshold == 0.8

@pytest.mark.asyncio
async def test_get_positions_summary(tadt_tracker, mock_live_traders):
    """Test getting positions summary for both sub-accounts."""
    # Mock positions for both traders
    mock_live_traders.long_trader.get_positions.return_value = [MOCK_POSITION]
    mock_live_traders.short_trader.get_positions.return_value = []
    
    await tadt_tracker.initialize()
    summary = await tadt_tracker.get_positions_summary()
    
    assert isinstance(summary, dict)
    assert "long_positions" in summary
    assert "short_positions" in summary
    assert "total_pnl" in summary
    assert len(summary["long_positions"]) == 1
    assert len(summary["short_positions"]) == 0
    assert summary["total_pnl"] == 150.0  # 100 unrealized + 50 realized

@pytest.mark.asyncio
async def test_get_position_history(tadt_tracker, mock_live_traders):
    """Test getting position history for both sub-accounts."""
    # Mock trade history for both traders
    mock_live_traders.long_trader.get_trade_history.return_value = MOCK_POSITION_HISTORY
    mock_live_traders.short_trader.get_trade_history.return_value = []
    
    await tadt_tracker.initialize()
    history = await tadt_tracker.get_position_history()
    
    assert isinstance(history, dict)
    assert "long_history" in history
    assert "short_history" in history
    assert len(history["long_history"]) == 1
    assert len(history["short_history"]) == 0
    assert history["long_history"][0]["pnl"] == 100.0

@pytest.mark.asyncio
async def test_analyze_trader_performance(tadt_tracker, mock_live_traders):
    """Test analyzing trader performance metrics."""
    # Mock trade history with multiple trades
    mock_history = [
        {
            "id": "1",
            "symbol": "BTCUSDT_UMCBL",
            "side": "LONG",
            "entryPrice": "50000.0",
            "exitPrice": "51000.0",
            "size": "0.01",
            "leverage": "5",
            "entryTime": "2024-03-11T10:00:00Z",
            "exitTime": "2024-03-11T11:00:00Z",
            "pnl": "100.0",
            "status": "CLOSED"
        },
        {
            "id": "2",
            "symbol": "BTCUSDT_UMCBL",
            "side": "LONG",
            "entryPrice": "51000.0",
            "exitPrice": "50000.0",
            "size": "0.01",
            "leverage": "5",
            "entryTime": "2024-03-11T12:00:00Z",
            "exitTime": "2024-03-11T13:00:00Z",
            "pnl": "-100.0",
            "status": "CLOSED"
        }
    ]
    
    mock_live_traders.long_trader.get_trade_history.return_value = mock_history
    
    await tadt_tracker.initialize()
    performance = await tadt_tracker.analyze_trader_performance("long")
    
    assert isinstance(performance, dict)
    assert "total_trades" in performance
    assert "win_rate" in performance
    assert "average_pnl" in performance
    assert "profit_factor" in performance
    assert performance["total_trades"] == 2
    assert performance["win_rate"] == 0.5
    assert performance["average_pnl"] == 0.0
    assert performance["profit_factor"] == 1.0

@pytest.mark.asyncio
async def test_detect_trap_patterns(tadt_tracker, mock_live_traders):
    """Test detecting trap patterns in position history."""
    # Mock position history with potential trap patterns
    mock_history = [
        {
            "id": "1",
            "symbol": "BTCUSDT_UMCBL",
            "side": "LONG",
            "entryPrice": "50000.0",
            "exitPrice": "49000.0",
            "size": "0.01",
            "leverage": "5",
            "entryTime": "2024-03-11T10:00:00Z",
            "exitTime": "2024-03-11T11:00:00Z",
            "pnl": "-100.0",
            "status": "CLOSED"
        }
    ]
    
    mock_live_traders.long_trader.get_trade_history.return_value = mock_history
    
    await tadt_tracker.initialize()
    traps = await tadt_tracker.detect_trap_patterns("long")
    
    assert isinstance(traps, list)
    assert len(traps) > 0
    assert "pattern_type" in traps[0]
    assert "confidence" in traps[0]
    assert "entry_price" in traps[0]
    assert "exit_price" in traps[0]

@pytest.mark.asyncio
async def test_get_risk_metrics(tadt_tracker, mock_live_traders):
    """Test calculating risk metrics for positions."""
    # Mock current positions
    mock_live_traders.long_trader.get_positions.return_value = [MOCK_POSITION]
    
    await tadt_tracker.initialize()
    risk_metrics = await tadt_tracker.get_risk_metrics()
    
    assert isinstance(risk_metrics, dict)
    assert "total_exposure" in risk_metrics
    assert "margin_ratio" in risk_metrics
    assert "leverage_ratio" in risk_metrics
    assert "position_concentration" in risk_metrics
    assert risk_metrics["total_exposure"] > 0
    assert 0 <= risk_metrics["margin_ratio"] <= 1
    assert risk_metrics["leverage_ratio"] > 0

@pytest.mark.asyncio
async def test_generate_performance_report(tadt_tracker, mock_live_traders):
    """Test generating a comprehensive performance report."""
    # Mock both position and trade history
    mock_live_traders.long_trader.get_positions.return_value = [MOCK_POSITION]
    mock_live_traders.long_trader.get_trade_history.return_value = MOCK_POSITION_HISTORY
    
    await tadt_tracker.initialize()
    report = await tadt_tracker.generate_performance_report()
    
    assert isinstance(report, dict)
    assert "timestamp" in report
    assert "positions_summary" in report
    assert "performance_metrics" in report
    assert "risk_metrics" in report
    assert "trap_patterns" in report
    assert isinstance(report["timestamp"], str)
    assert isinstance(report["positions_summary"], dict)
    assert isinstance(report["performance_metrics"], dict)
    assert isinstance(report["risk_metrics"], dict)
    assert isinstance(report["trap_patterns"], list)

@pytest.mark.asyncio
async def test_monitor_positions_continuously(tadt_tracker, mock_live_traders):
    """Test continuous position monitoring functionality."""
    # Mock position updates
    mock_live_traders.long_trader.get_positions.return_value = [MOCK_POSITION]
    
    # Start monitoring
    monitor_task = asyncio.create_task(tadt_tracker.monitor_positions_continuously())
    
    # Let it run for a short time
    await asyncio.sleep(0.1)
    
    # Cancel the task
    monitor_task.cancel()
    
    try:
        await monitor_task
    except asyncio.CancelledError:
        pass
    
    # Verify that positions were monitored
    assert mock_live_traders.long_trader.get_positions.called
    assert mock_live_traders.short_trader.get_positions.called 