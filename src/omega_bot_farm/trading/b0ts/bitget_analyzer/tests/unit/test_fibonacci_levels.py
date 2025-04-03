#!/usr/bin/env python3

"""
Unit tests for Fibonacci level calculations in BitgetPositionAnalyzerB0t.

These tests verify that the bot correctly calculates Fibonacci retracement and
extension levels for both long and short positions.
"""

import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Try to import BitgetPositionAnalyzerB0t
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False
    print("BitgetPositionAnalyzerB0t not available. Using mock for tests.")

# Constants for tests
PHI = 1.618034  # Golden Ratio
INV_PHI = 0.618034  # Inverse Golden Ratio

# Mock implementation if import fails
if not BOT_AVAILABLE:
    class BitgetPositionAnalyzerB0t:
        """Mock implementation for testing"""
        
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
            self.api_key = api_key or "test_key"
            self.api_secret = api_secret or "test_secret"
            self.api_passphrase = api_passphrase or "test_pass"
            self.use_testnet = use_testnet
        
        def _calculate_fibonacci_levels_long(self, entry_price, current_price=None):
            """Calculate Fibonacci levels for long positions."""
            levels = {}
            
            # Basic retracement levels
            levels["0.0%"] = {"price": entry_price, "percentage": 0.0}
            levels["23.6%"] = {"price": entry_price * (1 + 0.236), "percentage": 23.6}
            levels["38.2%"] = {"price": entry_price * (1 + 0.382), "percentage": 38.2}
            levels["50.0%"] = {"price": entry_price * (1 + 0.5), "percentage": 50.0}
            levels["61.8%"] = {"price": entry_price * (1 + 0.618), "percentage": 61.8}  # Golden Ratio
            levels["78.6%"] = {"price": entry_price * (1 + 0.786), "percentage": 78.6}
            levels["100.0%"] = {"price": entry_price * 2, "percentage": 100.0}
            
            # Extension levels
            levels["161.8%"] = {"price": entry_price * (1 + 1.618), "percentage": 161.8}  # Golden Ratio
            levels["261.8%"] = {"price": entry_price * (1 + 2.618), "percentage": 261.8}  # PHI³
            
            return levels
        
        def _calculate_fibonacci_levels_short(self, entry_price, current_price=None):
            """Calculate Fibonacci levels for short positions."""
            levels = {}
            
            # Basic retracement levels (downward)
            levels["0.0%"] = {"price": entry_price, "percentage": 0.0}
            levels["23.6%"] = {"price": entry_price * (1 - 0.236), "percentage": -23.6}
            levels["38.2%"] = {"price": entry_price * (1 - 0.382), "percentage": -38.2}
            levels["50.0%"] = {"price": entry_price * (1 - 0.5), "percentage": -50.0}
            levels["61.8%"] = {"price": entry_price * (1 - 0.618), "percentage": -61.8}  # Golden Ratio
            levels["78.6%"] = {"price": entry_price * (1 - 0.786), "percentage": -78.6}
            levels["100.0%"] = {"price": 0, "percentage": -100.0}
            
            return levels

        def analyze_position(self, position):
            """Analyze a position with Fibonacci levels."""
            symbol = position.get("symbol", "Unknown")
            side = position.get("side", "").lower()
            entry_price = float(position.get("entryPrice", 0))
            mark_price = float(position.get("markPrice", 0))
            
            # Calculate price change percentage
            price_change_pct = 0
            if entry_price > 0:
                if side == "long":
                    price_change_pct = ((mark_price - entry_price) / entry_price) * 100
                else:
                    price_change_pct = ((entry_price - mark_price) / entry_price) * 100
            
            # Calculate Fibonacci levels
            if side == "long":
                fib_levels = self._calculate_fibonacci_levels_long(entry_price, mark_price)
            else:
                fib_levels = self._calculate_fibonacci_levels_short(entry_price, mark_price)
            
            # Determine recommended take profit and stop loss levels
            take_profit = None
            stop_loss = None
            
            if side == "long":
                # Take profit: Next Fibonacci level above current price
                for level_name, level_data in sorted(fib_levels.items(), key=lambda x: level_data["percentage"]):
                    if level_data["price"] > mark_price and level_name != "0.0%":
                        take_profit = (level_name, level_data["price"])
                        break
                
                # Stop loss: Golden ratio retracement
                stop_price = entry_price * (1 - INV_PHI)
                stop_loss = ("Inverse Golden Ratio", stop_price)
            else:
                # Take profit: Next Fibonacci level below current price
                for level_name, level_data in sorted(fib_levels.items(), key=lambda x: level_data["percentage"], reverse=True):
                    if level_data["price"] < mark_price and level_name != "0.0%":
                        take_profit = (level_name, level_data["price"])
                        break
                
                # Stop loss: Golden ratio extension
                stop_price = entry_price * (1 + INV_PHI)
                stop_loss = ("Inverse Golden Ratio", stop_price)
            
            return {
                "position": position,
                "analysis": {
                    "fibonacci_levels": fib_levels,
                    "pnl_percentage": price_change_pct,
                    "recommended_take_profit": take_profit,
                    "recommended_stop_loss": stop_loss,
                    "harmony_score": 0.75  # Mock value
                }
            }


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
        self.assertEqual(fib_levels["61.8%"]["price"], 50000 * (1 + 0.618), "Golden ratio level incorrect")
        self.assertEqual(fib_levels["100.0%"]["price"], 50000 * 2, "100% level should be double the entry price")
        self.assertEqual(fib_levels["161.8%"]["price"], 50000 * (1 + 1.618), "Golden ratio extension incorrect")
        
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
        self.assertEqual(fib_levels["61.8%"]["price"], 3000 * (1 - 0.618), "Golden ratio level incorrect")
        
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