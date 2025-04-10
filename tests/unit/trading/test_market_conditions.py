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
Test suite for Dynamic Market Condition Adjustments module.
Tests the dynamic adjustment of Fibonacci levels and risk parameters
based on market volatility and trend strength.
"""

import os
import sys
import pytest
import numpy as np
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from unittest.mock import patch, MagicMock, AsyncMock

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.trading.market_conditions import (
    MarketConditionAnalyzer,
    VolatilityState,
    TrendState,
    MarketState
)

class TestConfig:
    """Test configuration constants"""
    SYMBOL = "BTCUSDT"
    TIMEFRAME = "1h"
    LOOKBACK_PERIODS = 20
    VOLATILITY_WINDOW = 14
    TREND_WINDOW = 14
    
    # Test price data
    STABLE_PRICES = [50000.0 + i * 10 for i in range(20)]  # Small, consistent moves
    VOLATILE_PRICES = [50000.0 + (i * 100 * (-1 if i % 2 else 1)) for i in range(20)]  # Large swings
    UPTREND_PRICES = [50000.0 + i * 100 for i in range(20)]  # Strong uptrend
    DOWNTREND_PRICES = [50000.0 - i * 100 for i in range(20)]  # Strong downtrend

@pytest.fixture
def market_analyzer():
    """Create MarketConditionAnalyzer instance"""
    analyzer = MarketConditionAnalyzer(
        symbol=TestConfig.SYMBOL,
        timeframe=TestConfig.TIMEFRAME,
        lookback_periods=TestConfig.LOOKBACK_PERIODS
    )
    return analyzer

@pytest.fixture
def price_data():
    """Generate test price data with timestamps"""
    def generate_prices(prices: List[float]) -> List[Dict]:
        base_time = datetime.now(timezone.utc)
        return [
            {
                'timestamp': int((base_time + timedelta(hours=i)).timestamp() * 1000),
                'price': price,
                'volume': 1000.0 * (1 + 0.1 * (i % 5))  # Add some volume variation
            }
            for i, price in enumerate(prices)
        ]
    return {
        'stable': generate_prices(TestConfig.STABLE_PRICES),
        'volatile': generate_prices(TestConfig.VOLATILE_PRICES),
        'uptrend': generate_prices(TestConfig.UPTREND_PRICES),
        'downtrend': generate_prices(TestConfig.DOWNTREND_PRICES)
    }

class TestMarketConditionAnalyzer:
    """Test suite for market condition analysis"""
    
    def test_initialization(self, market_analyzer):
        """Test analyzer initialization"""
        assert market_analyzer.symbol == TestConfig.SYMBOL
        assert market_analyzer.timeframe == TestConfig.TIMEFRAME
        assert market_analyzer.lookback_periods == TestConfig.LOOKBACK_PERIODS
        assert isinstance(market_analyzer.price_history, list)
    
    def test_volatility_calculation(self, market_analyzer, price_data):
        """Test volatility calculation under different market conditions"""
        # Test stable market
        market_analyzer.update_price_history(price_data['stable'])
        stable_volatility = market_analyzer.calculate_volatility()
        assert stable_volatility is not None
        assert stable_volatility < 0.01  # Low volatility
        
        # Test volatile market
        market_analyzer.update_price_history(price_data['volatile'])
        volatile_volatility = market_analyzer.calculate_volatility()
        assert volatile_volatility is not None
        assert volatile_volatility > 0.02  # High volatility
        
        # Verify volatile market has higher volatility
        assert volatile_volatility > stable_volatility * 2
    
    def test_trend_strength_calculation(self, market_analyzer, price_data):
        """Test trend strength calculation"""
        # Test uptrend
        market_analyzer.update_price_history(price_data['uptrend'])
        uptrend_strength = market_analyzer.calculate_trend_strength()
        assert uptrend_strength > 0.7  # Strong uptrend
        
        # Test downtrend
        market_analyzer.update_price_history(price_data['downtrend'])
        downtrend_strength = market_analyzer.calculate_trend_strength()
        assert downtrend_strength < -0.7  # Strong downtrend
        
        # Test sideways/stable market
        market_analyzer.update_price_history(price_data['stable'])
        stable_trend = market_analyzer.calculate_trend_strength()
        assert abs(stable_trend) < 0.3  # Weak trend
    
    def test_market_state_classification(self, market_analyzer, price_data):
        """Test market state classification"""
        # Test volatile uptrend
        market_analyzer.update_price_history(price_data['volatile'])
        market_analyzer._volatility = 0.05  # High volatility
        market_analyzer._trend_strength = 0.8  # Strong uptrend
        
        state = market_analyzer.get_market_state()
        assert isinstance(state, MarketState)
        assert state.volatility == VolatilityState.HIGH
        assert state.trend == TrendState.STRONG_UPTREND
        
        # Test stable downtrend
        market_analyzer.update_price_history(price_data['stable'])
        market_analyzer._volatility = 0.005  # Low volatility
        market_analyzer._trend_strength = -0.8  # Strong downtrend
        
        state = market_analyzer.get_market_state()
        assert state.volatility == VolatilityState.LOW
        assert state.trend == TrendState.STRONG_DOWNTREND
    
    def test_fibonacci_level_adjustment(self, market_analyzer, price_data):
        """Test Fibonacci level adjustments based on market conditions"""
        # Test volatile market adjustments
        market_analyzer.update_price_history(price_data['volatile'])
        volatile_adjustments = market_analyzer.get_fibonacci_adjustments()
        
        assert 'extension_multiplier' in volatile_adjustments
        assert 'retracement_multiplier' in volatile_adjustments
        assert volatile_adjustments['extension_multiplier'] > 1.0  # Wider targets in volatile markets
        assert volatile_adjustments['retracement_multiplier'] > 1.0  # Wider stops in volatile markets
        
        # Test stable market adjustments
        market_analyzer.update_price_history(price_data['stable'])
        stable_adjustments = market_analyzer.get_fibonacci_adjustments()
        
        assert stable_adjustments['extension_multiplier'] < volatile_adjustments['extension_multiplier']
        assert stable_adjustments['retracement_multiplier'] < volatile_adjustments['retracement_multiplier']
    
    def test_risk_adjustment(self, market_analyzer, price_data):
        """Test risk parameter adjustments"""
        # Test high volatility risk reduction
        market_analyzer.update_price_history(price_data['volatile'])
        volatile_risk = market_analyzer.get_risk_adjustments(base_risk_percent=1.0)
        
        assert volatile_risk['risk_percent'] < 1.0  # Reduce risk in volatile markets
        assert volatile_risk['position_size_multiplier'] < 1.0
        
        # Test strong trend risk increase
        market_analyzer.update_price_history(price_data['uptrend'])
        trend_risk = market_analyzer.get_risk_adjustments(base_risk_percent=1.0)
        
        assert trend_risk['risk_percent'] >= 1.0  # Maintain or increase risk in strong trends
        assert trend_risk['position_size_multiplier'] >= 1.0
    
    def test_dynamic_adjustment_integration(self, market_analyzer, price_data):
        """Test integration of all dynamic adjustments"""
        # Update with recent price data
        market_analyzer.update_price_history(price_data['volatile'])
        
        # Get comprehensive market adjustments
        adjustments = market_analyzer.get_market_adjustments(base_risk_percent=1.0)
        
        assert 'market_state' in adjustments
        assert 'fibonacci_adjustments' in adjustments
        assert 'risk_adjustments' in adjustments
        assert isinstance(adjustments['market_state'], MarketState)
        
        # Verify adjustments are coherent
        if adjustments['market_state'].volatility == VolatilityState.HIGH:
            assert adjustments['risk_adjustments']['risk_percent'] < 1.0
            assert adjustments['fibonacci_adjustments']['extension_multiplier'] > 1.0
    
    @pytest.mark.asyncio
    async def test_real_time_updates(self, market_analyzer):
        """Test real-time market condition updates"""
        current_price = 50000.0
        
        # Simulate real-time price updates
        for i in range(5):
            price_change = 100 * (-1 if i % 2 else 1)
            await market_analyzer.update_market_conditions(current_price + price_change)
            
            # Verify state is updated
            state = market_analyzer.get_market_state()
            assert isinstance(state, MarketState)
            
            current_price += price_change

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 