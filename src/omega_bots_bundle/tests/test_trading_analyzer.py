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
Test file for the TradingAnalyzerB0t class
"""

import unittest
import random
from omega_bots_bundle.analyzers.trading_analyzer import TradingAnalyzerB0t

class TestTradingAnalyzer(unittest.TestCase):
    """Test suite for the TradingAnalyzerB0t."""
    
    def setUp(self):
        """Set up test environment."""
        # Use a fixed seed for reproducibility
        self.analyzer = TradingAnalyzerB0t(seed=42)
        
        # Sample price data for testing
        self.uptrend_prices = [
            9000.0, 9050.0, 9100.0, 9080.0, 9150.0, 9200.0, 9250.0, 9300.0,
            9280.0, 9320.0, 9380.0, 9400.0, 9450.0, 9500.0, 9550.0, 9600.0,
            9650.0, 9700.0, 9750.0, 9800.0, 9850.0, 9900.0, 9950.0, 10000.0
        ]
        
        self.downtrend_prices = self.uptrend_prices[::-1]  # Reversed uptrend
        
        self.sideways_prices = [
            9500.0, 9520.0, 9480.0, 9510.0, 9490.0, 9505.0, 9495.0, 9515.0,
            9485.0, 9500.0, 9510.0, 9490.0, 9500.0, 9505.0, 9495.0, 9500.0,
            9510.0, 9490.0, 9500.0, 9505.0, 9495.0, 9500.0, 9495.0, 9505.0
        ]
    
    def test_analyze_trend(self):
        """Test trend analysis functionality."""
        # Test uptrend detection
        self.assertEqual(self.analyzer.analyze_trend(self.uptrend_prices), "uptrend")
        
        # Test downtrend detection
        self.assertEqual(self.analyzer.analyze_trend(self.downtrend_prices), "downtrend")
        
        # Test sideways detection
        self.assertEqual(self.analyzer.analyze_trend(self.sideways_prices), "sideways")
        
        # Test with insufficient data
        self.assertEqual(self.analyzer.analyze_trend([9500.0, 9600.0]), "sideways")
    
    def test_calculate_volatility(self):
        """Test volatility calculation."""
        # Uptrend should have significant volatility
        uptrend_vol = self.analyzer.calculate_volatility(self.uptrend_prices)
        self.assertGreater(uptrend_vol, 0.0)
        
        # Sideways should have lower volatility than uptrend
        sideways_vol = self.analyzer.calculate_volatility(self.sideways_prices)
        self.assertLess(sideways_vol, uptrend_vol)
        
        # Test with insufficient data
        self.assertEqual(self.analyzer.calculate_volatility([9500.0]), 0.0)
    
    def test_support_resistance(self):
        """Test support and resistance detection."""
        support, resistance = self.analyzer.detect_support_resistance(self.uptrend_prices)
        
        # Support should be less than resistance
        self.assertLess(support, resistance)
        
        # In uptrend, support should be first value and resistance should be last
        self.assertEqual(support, min(self.uptrend_prices))
        self.assertEqual(resistance, max(self.uptrend_prices))
        
        # Test with insufficient data
        current = 9500.0
        s, r = self.analyzer.detect_support_resistance([current])
        self.assertAlmostEqual(s, current * 0.98)
        self.assertAlmostEqual(r, current * 1.02)
    
    def test_market_regime(self):
        """Test market regime analysis."""
        # Uptrend should be detected as bullish
        regime = self.analyzer.analyze_market_regime(self.uptrend_prices)
        self.assertIn("bullish", regime)
        
        # Downtrend should be detected as bearish
        regime = self.analyzer.analyze_market_regime(self.downtrend_prices)
        self.assertIn("bearish", regime)
        
        # Sideways should be detected as neutral
        regime = self.analyzer.analyze_market_regime(self.sideways_prices)
        self.assertIn("neutral", regime)
    
    def test_risk_factor(self):
        """Test risk factor calculation."""
        # Create market context
        uptrend_context = {
            "trend": "uptrend",
            "recent_volatility": 100.0,
            "price": 10000.0
        }
        
        downtrend_context = {
            "trend": "downtrend",
            "recent_volatility": 100.0,
            "price": 10000.0
        }
        
        # Risk factor should be higher in uptrend
        uptrend_risk = self.analyzer.calculate_risk_factor(uptrend_context)
        downtrend_risk = self.analyzer.calculate_risk_factor(downtrend_context)
        
        self.assertGreater(uptrend_risk, downtrend_risk)
    
    def test_should_enter_market(self):
        """Test market entry decision."""
        # Create market and trader contexts
        uptrend_context = {"trend": "uptrend", "price": 10000.0}
        downtrend_context = {"trend": "downtrend", "price": 10000.0}
        sideways_context = {"trend": "sideways", "price": 10000.0}
        
        neutral_trader = {"emotional_state": "neutral"}
        greedy_trader = {"emotional_state": "greedy"}
        fearful_trader = {"emotional_state": "fearful"}
        
        # Test that decisions are of the correct type
        should_enter, direction, confidence = self.analyzer.should_enter_market(
            uptrend_context, neutral_trader
        )
        
        self.assertIsInstance(should_enter, bool)
        self.assertIn(direction, ["long", "short"])
        self.assertGreaterEqual(confidence, 0.1)
        self.assertLessEqual(confidence, 0.9)
        
        # Test that uptrend tends to favor "long" direction
        if should_enter and direction == "long":
            self.assertEqual(direction, "long")
    
    def test_safe_float_convert(self):
        """Test safe float conversion."""
        self.assertEqual(self.analyzer.safe_float_convert("10.5"), 10.5)
        self.assertEqual(self.analyzer.safe_float_convert("invalid"), 0.0)
        self.assertEqual(self.analyzer.safe_float_convert(None), 0.0)
        self.assertEqual(self.analyzer.safe_float_convert("invalid", 5.0), 5.0)
    
    def test_version(self):
        """Test version information."""
        self.assertEqual(self.analyzer.get_version(), "1.0.0")


if __name__ == "__main__":
    unittest.main() 