#!/usr/bin/env python3
"""
Test suite for Fibonacci profile integration with BitGet live trader.
"""

import pytest
import asyncio
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

# Test configuration
class TestConfig:
    """Test configuration for Fibonacci trader tests."""
    SYMBOL = "BTCUSDT"
    INITIAL_CAPITAL = 10000.0
    TEST_PRICE = 50000.0
    RISK_PERCENT = 1.0
    LEVERAGE = 3

@pytest.fixture
def mock_bitget():
    """Mock BitGet client."""
    mock = MagicMock()
    mock.initialize = MagicMock(return_value=asyncio.Future())
    mock.initialize.return_value.set_result(None)
    
    mock.create_order = MagicMock(return_value=asyncio.Future())
    mock.create_order.return_value.set_result({
        "orderId": "123456",
        "status": "open"
    })
    
    mock.get_positions = MagicMock(return_value=asyncio.Future())
    mock.get_positions.return_value.set_result([])
    
    mock.get_klines = MagicMock(return_value=asyncio.Future())
    mock.get_klines.return_value.set_result([
        {"timestamp": datetime.now(timezone.utc), "price": TestConfig.TEST_PRICE}
    ])
    
    return mock

@pytest.fixture
def pattern_points():
    """Sample pattern points for testing."""
    return [
        {"price": 45000.0, "timestamp": datetime.now(timezone.utc)},
        {"price": 50000.0, "timestamp": datetime.now(timezone.utc)},
        {"price": 48000.0, "timestamp": datetime.now(timezone.utc)},
        {"price": 49000.0, "timestamp": datetime.now(timezone.utc)},
        {"price": 47000.0, "timestamp": datetime.now(timezone.utc)}
    ]

@pytest.fixture
def mock_market_analyzer():
    """Mock market condition analyzer."""
    mock = MagicMock()
    mock.update_market_conditions = MagicMock(return_value=asyncio.Future())
    mock.update_market_conditions.return_value.set_result(None)
    
    mock.get_market_adjustments = MagicMock(return_value={
        "fibonacci_adjustments": {
            "retracement_multiplier": 1.0,
            "extension_multiplier": 1.0
        },
        "risk_adjustments": {
            "risk_percent": 1.0,
            "stop_loss_multiplier": 1.0,
            "take_profit_multiplier": 1.0
        }
    })
    
    mock.get_market_state = MagicMock(return_value={
        "volatility": 0.02,
        "trend_strength": 0.7,
        "market_regime": "bullish"
    })
    
    return mock

class TestFibonacciProfileIntegration:
    """Test suite for Fibonacci profile integration with BitGet live trader."""
    
    @pytest.mark.asyncio
    async def test_fibonacci_profile_initialization(self, monkeypatch, mock_bitget):
        """Test Fibonacci profile initialization with BitGet live trader."""
        # Import the class after monkeypatching
        from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
        
        # Arrange
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.BitGetClient", 
                          lambda **kwargs: mock_bitget)
        
        # Act
        trader = FibonacciProfileTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL,
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_pass"
        )
        await trader.initialize()
        
        # Assert
        assert trader.symbol == TestConfig.SYMBOL
        assert trader.initial_capital == TestConfig.INITIAL_CAPITAL
        assert trader.profile.name == "Strategic Fibonacci Trader"
        assert mock_bitget.initialize.called
    
    @pytest.mark.asyncio
    async def test_fibonacci_pattern_detection(self, monkeypatch, mock_bitget, pattern_points):
        """Test Fibonacci pattern detection in profile trader."""
        # Import after monkeypatching
        from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
        
        # Arrange
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.BitGetClient", 
                          lambda **kwargs: mock_bitget)
        
        # Mock the pattern validation to return a pattern
        mock_validate = MagicMock(return_value={
            "type": "Bullish Gartley",
            "points": [p["price"] for p in pattern_points],
            "confidence": 0.8
        })
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.validate_pattern", mock_validate)
        
        # Act
        trader = FibonacciProfileTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL,
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_pass"
        )
        await trader.initialize()
        
        # Update with pattern points
        await trader.update_pattern_points(pattern_points)
        patterns = trader.detect_patterns()
        
        # Assert
        assert len(patterns) > 0
        assert "type" in patterns[0]
        assert patterns[0]["type"] == "Bullish Gartley"
        assert "confidence" in patterns[0]
        assert mock_validate.called
    
    @pytest.mark.asyncio
    async def test_trading_signal_generation(self, monkeypatch, mock_bitget, pattern_points, mock_market_analyzer):
        """Test trading signal generation from Fibonacci patterns."""
        # Import after monkeypatching
        from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
        
        # Arrange
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.BitGetClient", 
                          lambda **kwargs: mock_bitget)
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.MarketConditionAnalyzer", 
                          lambda **kwargs: mock_market_analyzer)
        
        # Mock the pattern validation
        mock_validate = MagicMock(return_value={
            "type": "Bullish Gartley",
            "points": [p["price"] for p in pattern_points],
            "confidence": 0.8
        })
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.validate_pattern", mock_validate)
        
        # Mock the Fibonacci level calculation
        mock_calc_levels = MagicMock(return_value={
            "0": 45000.0,
            "0.236": 46000.0,
            "0.382": 47000.0,
            "0.5": 48000.0,
            "0.618": 49000.0,
            "0.786": 50000.0,
            "1.0": 51000.0,
            "1.618": 52000.0
        })
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.calculate_fibonacci_levels", mock_calc_levels)
        
        # Act
        trader = FibonacciProfileTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL,
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_pass"
        )
        await trader.initialize()
        
        # Update with pattern points
        await trader.update_pattern_points(pattern_points)
        patterns = trader.detect_patterns()
        signal = trader.generate_trading_signal(patterns[0])
        
        # Assert
        assert signal is not None
        assert signal.pattern_type == "Bullish Gartley"
        assert signal.entry_price == 49000.0  # 0.618 level
        assert signal.stop_loss == 50000.0    # 0.786 level
        assert signal.take_profit == 52000.0  # 1.618 level
        assert signal.risk_percent == 1.0
        assert mock_calc_levels.called
    
    @pytest.mark.asyncio
    async def test_risk_management(self, monkeypatch, mock_bitget, mock_market_analyzer):
        """Test risk management calculations with profile parameters."""
        # Import after monkeypatching
        from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
        
        # Arrange
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.BitGetClient", 
                          lambda **kwargs: mock_bitget)
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.MarketConditionAnalyzer", 
                          lambda **kwargs: mock_market_analyzer)
        
        # Mock the position size calculation
        mock_calc_position = MagicMock(return_value=0.1)  # Return 0.1 BTC position size
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.calculate_position_size", mock_calc_position)
        
        # Mock account size
        mock_bitget.get_account_balance = MagicMock(return_value=asyncio.Future())
        mock_bitget.get_account_balance.return_value.set_result(TestConfig.INITIAL_CAPITAL)
        
        # Act
        trader = FibonacciProfileTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL,
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_pass",
            base_risk_percent=TestConfig.RISK_PERCENT,
            leverage=TestConfig.LEVERAGE
        )
        await trader.initialize()
        
        # Calculate risk levels
        risk_levels = trader.calculate_risk_levels(
            entry_price=TestConfig.TEST_PRICE,
            risk_percent=TestConfig.RISK_PERCENT
        )
        
        # Assert
        assert "position_size" in risk_levels
        assert "stop_loss" in risk_levels
        assert "take_profit" in risk_levels
        assert risk_levels["position_size"] == 0.1  # From mock
        assert mock_calc_position.called
    
    @pytest.mark.asyncio
    async def test_fibonacci_trade_execution(self, monkeypatch, mock_bitget, mock_market_analyzer):
        """Test trade execution based on Fibonacci profile."""
        # Import after monkeypatching
        from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
        from omega_ai.trading.fibonacci_profile_trader import TradingSignal
        
        # Arrange
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.BitGetClient", 
                          lambda **kwargs: mock_bitget)
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.MarketConditionAnalyzer", 
                          lambda **kwargs: mock_market_analyzer)
        
        # Act
        trader = FibonacciProfileTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL,
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_pass",
            base_risk_percent=TestConfig.RISK_PERCENT,
            leverage=TestConfig.LEVERAGE
        )
        await trader.initialize()
        
        # Create a trading signal
        signal = TradingSignal(
            pattern_type="Bullish Gartley",
            entry_price=TestConfig.TEST_PRICE,
            stop_loss=TestConfig.TEST_PRICE * 0.95,
            take_profit=TestConfig.TEST_PRICE * 1.05,
            confidence=0.8,
            timeframe="1h",
            fibonacci_levels={
                "0": TestConfig.TEST_PRICE * 0.9,
                "0.236": TestConfig.TEST_PRICE * 0.95,
                "0.618": TestConfig.TEST_PRICE,
                "1.0": TestConfig.TEST_PRICE * 1.05
            },
            risk_percent=TestConfig.RISK_PERCENT,
            position_size=0.1,
            timestamp=datetime.now(timezone.utc)
        )
        
        # Execute trade
        success = await trader.execute_trade(signal)
        
        # Assert
        assert success is True
        mock_bitget.create_order.assert_called()
    
    @pytest.mark.asyncio
    async def test_position_management(self, monkeypatch, mock_bitget, mock_market_analyzer):
        """Test position management with Fibonacci levels."""
        # Import after monkeypatching
        from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
        
        # Arrange
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.BitGetClient", 
                          lambda **kwargs: mock_bitget)
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.MarketConditionAnalyzer", 
                          lambda **kwargs: mock_market_analyzer)
        
        # Mock positions
        mock_bitget.get_positions.return_value.set_result([{
            "symbol": TestConfig.SYMBOL,
            "side": "long",
            "size": 0.1,
            "entryPrice": TestConfig.TEST_PRICE * 0.95,
            "unrealizedPnl": 0.0
        }])
        
        # Act
        trader = FibonacciProfileTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL,
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_pass"
        )
        await trader.initialize()
        
        # Manage positions
        await trader.manage_positions()
        
        # Assert
        mock_bitget.get_positions.assert_called()
    
    @pytest.mark.asyncio
    async def test_market_condition_adaptation(self, monkeypatch, mock_bitget, mock_market_analyzer):
        """Test adaptation to market conditions with profile parameters."""
        # Import after monkeypatching
        from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
        
        # Arrange
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.BitGetClient", 
                          lambda **kwargs: mock_bitget)
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.MarketConditionAnalyzer", 
                          lambda **kwargs: mock_market_analyzer)
        
        # Act
        trader = FibonacciProfileTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL,
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_pass"
        )
        await trader.initialize()
        
        # Update market conditions
        await trader.update_market_conditions(TestConfig.TEST_PRICE)
        
        # Get adjusted params
        adjusted_params = trader.get_adjusted_parameters()
        
        # Assert
        assert adjusted_params is not None
        assert "fibonacci_adjustments" in adjusted_params
        assert "risk_adjustments" in adjusted_params
        mock_market_analyzer.update_market_conditions.assert_called_with(TestConfig.TEST_PRICE)
        mock_market_analyzer.get_market_adjustments.assert_called()
    
    @pytest.mark.asyncio
    async def test_profile_strategy_alignment(self, monkeypatch, mock_bitget, mock_market_analyzer):
        """Test alignment of Fibonacci strategy with profile strategy."""
        # Import after monkeypatching
        from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
        
        # Arrange
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.BitGetClient", 
                          lambda **kwargs: mock_bitget)
        monkeypatch.setattr("omega_ai.trading.fibonacci_profile_trader.MarketConditionAnalyzer", 
                          lambda **kwargs: mock_market_analyzer)
        
        # Act
        trader = FibonacciProfileTrader(
            symbol=TestConfig.SYMBOL,
            initial_capital=TestConfig.INITIAL_CAPITAL,
            api_key="test_key",
            api_secret="test_secret",
            passphrase="test_pass",
            profile_type="strategic"  # Explicitly set to strategic
        )
        await trader.initialize()
        
        # Assert profile is using Fibonacci settings
        assert trader.profile.fib_levels is not None
        assert len(trader.profile.fib_levels) > 0
        assert 0.618 in trader.profile.fib_levels  # Key Fibonacci level 