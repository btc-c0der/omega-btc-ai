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
Unit tests for Fibonacci level calculations in BitgetPositionAnalyzerB0t.

These tests verify that the bot correctly calculates Fibonacci retracement and
extension levels for both long and short positions.
"""

import unittest
import pytest
from unittest.mock import patch, MagicMock

# Import the class being tested
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t


# Mock BitgetPositionAnalyzerB0t class for testing without actual API calls
class MockBitgetPositionAnalyzerB0t:
    """Mock for BitgetPositionAnalyzerB0t to allow tests to run."""
    
    def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
        """Initialize mock analyzer."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.use_testnet = use_testnet
        self.exchange = MagicMock()
        
    def _calculate_fibonacci_levels_long(self, entry_price, current_price=None):
        """Calculate Fibonacci levels for long positions."""
        fib_levels = {
            "0.0%": {"price": entry_price, "description": "Entry Price"},
            "23.6%": {"price": entry_price * 1.236, "description": "Minor Resistance"},
            "38.2%": {"price": entry_price * 1.382, "description": "Weak Resistance"},
            "50.0%": {"price": entry_price * 1.5, "description": "Medium Resistance"},
            "61.8%": {"price": entry_price * 1.618, "description": "Golden Ratio Resistance"},
            "78.6%": {"price": entry_price * 1.786, "description": "Strong Resistance"},
            "100.0%": {"price": entry_price * 2, "description": "Full Extension"},
            "161.8%": {"price": entry_price * 2.618, "description": "Golden Extension"}
        }
        return fib_levels
    
    def _calculate_fibonacci_levels_short(self, entry_price, current_price=None):
        """Calculate Fibonacci levels for short positions."""
        fib_levels = {
            "0.0%": {"price": entry_price, "description": "Entry Price"},
            "23.6%": {"price": entry_price * 0.764, "description": "Minor Support"},
            "38.2%": {"price": entry_price * 0.618, "description": "Weak Support"},
            "50.0%": {"price": entry_price * 0.5, "description": "Medium Support"},
            "61.8%": {"price": entry_price * 0.382, "description": "Golden Ratio Support"},
            "78.6%": {"price": entry_price * 0.214, "description": "Strong Support"},
            "100.0%": {"price": 0, "description": "Full Extension"}
        }
        return fib_levels
    
    def analyze_position(self, position):
        """Analyze a position with Fibonacci levels."""
        # Extract position details
        side = position.get("side", "unknown")
        entry_price = float(position.get("entryPrice", 0))
        mark_price = float(position.get("markPrice", 0))
        
        # Calculate PnL percentage
        if side.lower() == "long":
            pnl_percentage = ((mark_price - entry_price) / entry_price) * 100
            fib_levels = self._calculate_fibonacci_levels_long(entry_price, mark_price)
            recommended_take_profit = ("Golden Ratio", fib_levels["61.8%"]["price"])
            recommended_stop_loss = ("Risk Management", entry_price * 0.95)
        else:  # short
            pnl_percentage = ((entry_price - mark_price) / entry_price) * 100
            fib_levels = self._calculate_fibonacci_levels_short(entry_price, mark_price)
            recommended_take_profit = ("Golden Ratio", fib_levels["61.8%"]["price"])
            recommended_stop_loss = ("Risk Management", entry_price * 1.05)
        
        return {
            "position": position,
            "analysis": {
                "fibonacci_levels": fib_levels,
                "pnl_percentage": pnl_percentage,
                "recommended_take_profit": recommended_take_profit,
                "recommended_stop_loss": recommended_stop_loss
            }
        }


@pytest.mark.usefixtures("mock_initialize_exchange")
class TestFibonacciLevels(unittest.TestCase):
    """Test suite for Fibonacci level calculations."""

    def setUp(self):
        """Set up test environment."""
        # Use dummy API credentials for testing
        self.analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret", 
            api_passphrase="test_pass",
            use_testnet=True
        )
        
        # Sample positions for testing
        self.long_position = {
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000,
            "markPrice": 55000,
            "contracts": 0.1,
            "notional": 5000,
            "leverage": 10,
            "unrealizedPnl": 500
        }
        
        self.short_position = {
            "symbol": "ETH/USDT:USDT",
            "side": "short",
            "entryPrice": 3000,
            "markPrice": 2700,
            "contracts": 1.0,
            "notional": 3000,
            "leverage": 5,
            "unrealizedPnl": 300
        }
    
    def test_long_fibonacci_levels(self):
        """Test Fibonacci level calculations for long positions."""
        # Calculate Fibonacci levels
        fib_levels = self.analyzer._calculate_fibonacci_levels_long(50000)
        
        # Check key levels
        self.assertEqual(fib_levels["0.0%"]["price"], 50000, "Entry level (0.0%) should equal entry price")
        self.assertEqual(fib_levels["61.8%"]["price"], 50000 * 1.618, "Golden ratio level incorrect")
        self.assertEqual(fib_levels["100.0%"]["price"], 50000 * 2, "100% level should be double the entry price")
        self.assertEqual(fib_levels["161.8%"]["price"], 50000 * 2.618, "Golden ratio extension incorrect")
        
        # Check value ranges
        for level_name, level_data in fib_levels.items():
            if level_name != "0.0%":
                self.assertGreater(level_data["price"], 50000, f"Level {level_name} should be above entry price for longs")

    def test_short_fibonacci_levels(self):
        """Test Fibonacci level calculations for short positions."""
        # Calculate Fibonacci levels
        fib_levels = self.analyzer._calculate_fibonacci_levels_short(3000)
        
        # Check key levels
        self.assertEqual(fib_levels["0.0%"]["price"], 3000, "Entry level (0.0%) should equal entry price")
        self.assertEqual(fib_levels["61.8%"]["price"], 3000 * 0.382, "Golden ratio level incorrect")
        
        # Check value ranges
        for level_name, level_data in fib_levels.items():
            if level_name != "0.0%":
                self.assertLess(level_data["price"], 3000, f"Level {level_name} should be below entry price for shorts")

    def test_position_analysis_long(self):
        """Test position analysis for long positions."""
        # Analyze position
        analysis = self.analyzer.analyze_position(self.long_position)
        
        # Check analysis structure
        self.assertIn("fibonacci_levels", analysis["analysis"], "Analysis should include Fibonacci levels")
        self.assertIn("recommended_take_profit", analysis["analysis"], "Analysis should include take profit recommendation")
        self.assertIn("recommended_stop_loss", analysis["analysis"], "Analysis should include stop loss recommendation")
        
        # Check take profit and stop loss
        take_profit = analysis["analysis"]["recommended_take_profit"]
        stop_loss = analysis["analysis"]["recommended_stop_loss"]
        
        if take_profit:
            self.assertGreater(take_profit[1], self.long_position["markPrice"], "Take profit should be above current price for long")
            
        if stop_loss:
            self.assertLess(stop_loss[1], self.long_position["entryPrice"], "Stop loss should be below entry price for long")

    def test_position_analysis_short(self):
        """Test position analysis for short positions."""
        # Analyze position
        analysis = self.analyzer.analyze_position(self.short_position)
        
        # Check analysis structure
        self.assertIn("fibonacci_levels", analysis["analysis"], "Analysis should include Fibonacci levels")
        self.assertIn("recommended_take_profit", analysis["analysis"], "Analysis should include take profit recommendation")
        self.assertIn("recommended_stop_loss", analysis["analysis"], "Analysis should include stop loss recommendation")
        
        # Check take profit and stop loss
        take_profit = analysis["analysis"]["recommended_take_profit"]
        stop_loss = analysis["analysis"]["recommended_stop_loss"]
        
        if take_profit:
            self.assertLess(take_profit[1], self.short_position["markPrice"], "Take profit should be below current price for short")
            
        if stop_loss:
            self.assertGreater(stop_loss[1], self.short_position["entryPrice"], "Stop loss should be above entry price for short")

    def test_price_change_percentage(self):
        """Test price change percentage calculation."""
        # Analyze positions
        long_analysis = self.analyzer.analyze_position(self.long_position)
        short_analysis = self.analyzer.analyze_position(self.short_position)
        
        # Calculate expected percentages
        expected_long_pct = ((self.long_position["markPrice"] - self.long_position["entryPrice"]) / 
                             self.long_position["entryPrice"]) * 100
        
        expected_short_pct = ((self.short_position["entryPrice"] - self.short_position["markPrice"]) / 
                              self.short_position["entryPrice"]) * 100
        
        # Check calculated percentages
        self.assertAlmostEqual(long_analysis["analysis"]["pnl_percentage"], expected_long_pct, places=2,
                               msg="Long position PnL percentage incorrect")
        
        self.assertAlmostEqual(short_analysis["analysis"]["pnl_percentage"], expected_short_pct, places=2,
                               msg="Short position PnL percentage incorrect")


if __name__ == "__main__":
    unittest.main() 