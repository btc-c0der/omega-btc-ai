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
Test suite for the Fibonacci Live Trader implementation.
This suite verifies the integration of Fibonacci analysis with BitGet trading.

Tests cover:
1. Pattern detection and signal generation
2. Trading profile integration
3. Position management with Fibonacci levels
4. Risk management and money management
5. BitGet exchange integration
"""

import os
import sys
import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock, AsyncMock
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Add project root to path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
from omega_ai.analysis.fibonacci_patterns import FibonacciPatternDetector, PatternPoint
from omega_ai.utils.fibonacci import (
    calculate_fibonacci_levels,
    calculate_golden_ratio_zones,
    calculate_fibonacci_pivot_points,
    calculate_fibonacci_risk_levels
)

class TestConfig:
    """Test configuration constants"""
    SYMBOL = "BTCUSDT"
    INITIAL_CAPITAL = 10000.0
    TEST_PRICE = 50000.0
    TEST_PRICES = [
        45000.0,  # Point X
        50000.0,  # Point A
        48000.0,  # Point B
        49000.0,  # Point C
        47000.0   # Point D
    ]
    LEVERAGE = 5
    RISK_PERCENT = 1.0
    TIMEFRAME = "1h"

@pytest.fixture
def mock_bitget():
    """Mock BitGet CCXT client"""
    with patch('omega_ai.trading.exchanges.bitget_ccxt.BitGetCCXT') as mock:
        instance = AsyncMock()
        
        # Mock market data
        instance.get_market_ticker = AsyncMock(return_value={
            'symbol': TestConfig.SYMBOL,
            'last': TestConfig.TEST_PRICE,
            'high': TestConfig.TEST_PRICE * 1.05,
            'low': TestConfig.TEST_PRICE * 0.95,
            'volume': 1000.0,
            'timestamp': int(datetime.now(timezone.utc).timestamp() * 1000)
        })
        
        # Mock trading methods
        instance.place_order = AsyncMock(return_value={
            'id': '12345',
            'status': 'open',
            'symbol': TestConfig.SYMBOL,
            'side': 'buy',
            'price': TestConfig.TEST_PRICE,
            'amount': 0.1
        })
        
        instance.get_positions = AsyncMock(return_value=[])
        instance.close_position = AsyncMock()
        instance.initialize = AsyncMock()
        
        mock.return_value = instance
        yield instance

@pytest.fixture
def fibonacci_detector():
    """Create FibonacciPatternDetector instance"""
    detector = FibonacciPatternDetector()
    return detector

@pytest.fixture
def pattern_points():
    """Generate test pattern points"""
    now = datetime.now(timezone.utc)
    return [
        PatternPoint(price=p, timestamp=now, label=l)
        for p, l in zip(TestConfig.TEST_PRICES, ['X', 'A', 'B', 'C', 'D'])
    ]

class TestFibonacciLiveTrader:
    """Test suite for Fibonacci Live Trader"""
    
    @pytest.mark.asyncio
    async def test_initialization(self, mock_bitget):
        """Test trader initialization"""
        from omega_ai.trading.fibonacci_live_trader import FibonacciLiveTrader
        
        # Act
        trader = FibonacciLiveTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL
        )
        await trader.initialize()
        
        # Assert
        assert trader.symbol == TestConfig.SYMBOL
        assert trader.initial_capital == TestConfig.INITIAL_CAPITAL
        assert trader.fibonacci_detector is not None
        mock_bitget.initialize.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_pattern_detection(self, mock_bitget, pattern_points):
        """Test Fibonacci pattern detection"""
        from omega_ai.trading.fibonacci_live_trader import FibonacciLiveTrader
        
        # Arrange
        trader = FibonacciLiveTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL
        )
        await trader.initialize()
        
        # Act
        patterns = trader.detect_patterns(pattern_points)
        
        # Assert
        assert isinstance(patterns, list)
        if patterns:
            pattern = patterns[0]
            assert 'type' in pattern
            assert 'points' in pattern
            assert 'ratios' in pattern
    
    @pytest.mark.asyncio
    async def test_trading_signal_generation(self, mock_bitget, pattern_points):
        """Test trading signal generation from patterns"""
        from omega_ai.trading.fibonacci_live_trader import FibonacciLiveTrader
        
        # Arrange
        trader = FibonacciLiveTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL
        )
        await trader.initialize()
        
        # Act
        signals = trader.generate_trading_signals(pattern_points)
        
        # Assert
        assert isinstance(signals, list)
        if signals:
            signal = signals[0]
            assert 'pattern' in signal
            assert 'type' in signal
            assert 'entry' in signal
            assert 'stop_loss' in signal
            assert 'take_profit' in signal
    
    @pytest.mark.asyncio
    async def test_risk_management(self, mock_bitget):
        """Test risk management calculations"""
        from omega_ai.trading.fibonacci_live_trader import FibonacciLiveTrader
        
        # Arrange
        trader = FibonacciLiveTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL
        )
        await trader.initialize()
        
        # Act
        risk_levels = trader.calculate_risk_levels(
            entry_price=TestConfig.TEST_PRICE,
            risk_percent=TestConfig.RISK_PERCENT
        )
        
        # Assert
        assert isinstance(risk_levels, dict)
        assert 'position_size' in risk_levels
        assert 'stop_loss' in risk_levels
        assert 'take_profit' in risk_levels
        assert risk_levels['position_size'] > 0
    
    @pytest.mark.asyncio
    async def test_order_execution(self, mock_bitget):
        """Test order execution based on Fibonacci signals"""
        from omega_ai.trading.fibonacci_live_trader import FibonacciLiveTrader
        
        # Arrange
        trader = FibonacciLiveTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL
        )
        await trader.initialize()
        
        signal = {
            'type': 'LONG',
            'entry': TestConfig.TEST_PRICE,
            'stop_loss': TestConfig.TEST_PRICE * 0.95,
            'take_profit': TestConfig.TEST_PRICE * 1.05
        }
        
        # Act
        order = await trader.execute_trade(signal)
        
        # Assert
        assert order is not None
        assert 'id' in order
        assert order['status'] == 'open'
        mock_bitget.place_order.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_position_management(self, mock_bitget):
        """Test position management with Fibonacci levels"""
        from omega_ai.trading.fibonacci_live_trader import FibonacciLiveTrader
        
        # Arrange
        trader = FibonacciLiveTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL
        )
        await trader.initialize()
        
        # Mock an open position
        mock_bitget.get_positions.return_value = [{
            'symbol': TestConfig.SYMBOL,
            'side': 'long',
            'size': 0.1,
            'entry_price': TestConfig.TEST_PRICE,
            'unrealized_pnl': 100.0
        }]
        
        # Act
        await trader.manage_positions()
        positions = await trader.get_positions()
        
        # Assert
        assert isinstance(positions, list)
        assert len(positions) > 0
        mock_bitget.get_positions.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_fibonacci_based_exits(self, mock_bitget):
        """Test position exits based on Fibonacci levels"""
        from omega_ai.trading.fibonacci_live_trader import FibonacciLiveTrader
        
        # Arrange
        trader = FibonacciLiveTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL
        )
        await trader.initialize()
        
        # Mock position at take profit level
        position = {
            'symbol': TestConfig.SYMBOL,
            'side': 'long',
            'size': 0.1,
            'entry_price': TestConfig.TEST_PRICE,
            'unrealized_pnl': TestConfig.TEST_PRICE * 0.05  # 5% profit
        }
        
        # Act
        should_exit = trader.should_exit_position(position, TestConfig.TEST_PRICE * 1.05)
        
        # Assert
        assert isinstance(should_exit, bool)
        assert should_exit is True  # Should exit at 5% profit (Fibonacci level)

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 