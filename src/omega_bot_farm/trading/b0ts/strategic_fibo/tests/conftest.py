#!/usr/bin/env python3

"""
Test fixtures for StrategicTraderB0t tests.

This module contains pytest fixtures used across all StrategicTraderB0t tests.
"""

import pytest
from unittest.mock import MagicMock, patch

# Mock the dependencies
@pytest.fixture
def mock_trading_analyzer():
    """Create a mock TradingAnalyzerB0t."""
    analyzer = MagicMock()
    # Setup default behaviors
    analyzer.analyze_trend.return_value = "uptrend"
    analyzer.calculate_volatility.return_value = 0.02
    analyzer.detect_support_resistance.return_value = (49000, 51000)
    analyzer.analyze_market_regime.return_value = "bullish"
    analyzer.calculate_risk_factor.return_value = 0.6
    return analyzer

@pytest.fixture
def mock_redis_client():
    """Create a mock RedisClient."""
    redis_client = MagicMock()
    redis_client.get.return_value = None
    redis_client.set.return_value = True
    return redis_client

@pytest.fixture
def mock_cosmic_service():
    """Create a mock CosmicFactorService."""
    service = MagicMock()
    service.is_enabled.return_value = True
    service.calculate_cosmic_influences.return_value = {
        "moon_influence": 0.1,
        "schumann_influence": 0.05,
        "sentiment_influence": 0.2
    }
    service.apply_cosmic_factors.side_effect = lambda decision, influences: decision
    return service

@pytest.fixture
def sample_market_context():
    """Create a sample market context for testing."""
    return {
        "price": 50000.0,
        "trend": "uptrend",
        "regime": "bullish",
        "price_history": [49000, 49200, 49500, 49800, 50000, 50200, 50400, 50500, 50300, 50000],
        "volatility": 0.02,
        "volume": 1000,
        "moon_phase": "FULL_MOON",
        "schumann_frequency": "BASELINE",
        "market_liquidity": "NORMAL",
        "global_sentiment": "NEUTRAL",
        "mercury_retrograde": False,
        "trader_latitude": 40.0,
        "trader_longitude": -74.0,
        "day_of_week": 1,
        "hour_of_day": 12
    }

@pytest.fixture
def strategic_trader(mock_trading_analyzer, mock_redis_client, mock_cosmic_service):
    """Create a StrategicTraderB0t with mocked dependencies."""
    with patch('src.omega_bot_farm.trading.b0ts.trading_analyser.trading_analyzer_b0t.TradingAnalyzerB0t', 
               return_value=mock_trading_analyzer):
        with patch('src.omega_bot_farm.utils.cosmic_factor_service.CosmicFactorService', 
                   return_value=mock_cosmic_service):
            from src.omega_bot_farm.trading.b0ts.strategic_fibo.strategic_b0t import StrategicTraderB0t
            
            trader = StrategicTraderB0t(
                initial_capital=10000.0,
                name="TestTrader",
                redis_client=mock_redis_client
            )
            
            # Configure initial trader state
            trader.state.risk_appetite = 0.5
            trader.state.emotional_state = "neutral"
            
            return trader 