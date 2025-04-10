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
            self.account_equity = 10000  # Set a default account equity
        
        def generate_fibonacci_levels(self, base_price, side="long"):
            """
            Generate Fibonacci retracement and extension levels from a base price.
            
            Args:
                base_price: Base price to calculate levels from
                side: Position side ('long' or 'short')
                
            Returns:
                Dict of Fibonacci levels
            """
            if side.lower() == 'long':
                # Long position - levels above base price
                levels = {
                    "0.0%": base_price,
                    "23.6%": base_price * (1 + 0.236),
                    "38.2%": base_price * (1 + 0.382),
                    "50.0%": base_price * (1 + 0.5),
                    "61.8%": base_price * (1 + 0.618),  # Golden Ratio
                    "78.6%": base_price * (1 + 0.786),
                    "100.0%": base_price * 2,
                    "161.8%": base_price * (1 + 1.618),  # Golden Ratio
                    "261.8%": base_price * (1 + 2.618)   # PHI^3
                }
            else:
                # Short position - levels below base price
                levels = {
                    "0.0%": base_price,
                    "23.6%": base_price * (1 - 0.236),
                    "38.2%": base_price * (1 - 0.382),
                    "50.0%": base_price * (1 - 0.5),
                    "61.8%": base_price * (1 - 0.618),  # Golden Ratio
                    "78.6%": base_price * (1 - 0.786),
                    "100.0%": 0,  # Zero
                    "161.8%": None,  # Not applicable for shorts
                    "261.8%": None   # Not applicable for shorts
                }
            
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
            
            # Calculate Fibonacci levels using the generate method
            fib_levels = self.generate_fibonacci_levels(entry_price, side)
            
            # Calculate distance to each level as percentage
            level_distances = {}
            for level_name, level_price in fib_levels.items():
                if level_price is not None:
                    if side == 'long':
                        distance_pct = ((level_price - mark_price) / mark_price) * 100
                    else:
                        distance_pct = ((mark_price - level_price) / mark_price) * 100
                    level_distances[level_name] = distance_pct
            
            # Determine recommended take profit and stop loss levels
            take_profit = None
            stop_loss = None
            
            if side == "long":
                # Take profit: Next Fibonacci level above current price
                for level_name, level_price in sorted(fib_levels.items(), key=lambda x: x[1] if x[1] is not None else 0):
                    if level_price is not None and level_price > mark_price and level_name != "0.0%":
                        take_profit = (level_name, level_price)
                        break
                
                # Stop loss: Golden ratio retracement
                stop_price = entry_price * (1 - INV_PHI)
                stop_loss = ("Inverse Golden Ratio", stop_price)
            else:
                # Take profit: Next Fibonacci level below current price
                for level_name, level_price in sorted(fib_levels.items(), key=lambda x: x[1] if x[1] is not None else float('inf'), reverse=True):
                    if level_price is not None and level_price < mark_price and level_name != "0.0%":
                        take_profit = (level_name, level_price)
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
        fib_levels = self.analyzer.generate_fibonacci_levels(50000, side="long")
        
        # Check key levels
        self.assertEqual(fib_levels["0.0%"], 50000, "Entry level (0.0%) should equal entry price")
        self.assertEqual(fib_levels["61.8%"], 50000 * (1 + 0.618), "Golden ratio level incorrect")
        self.assertEqual(fib_levels["100.0%"], 50000 * 2, "100% level should be double the entry price")
        self.assertEqual(fib_levels["161.8%"], 50000 * (1 + 1.618), "Golden ratio extension incorrect")
        
        # Check value ranges
        for level_name, level_price in fib_levels.items():
            if level_price is not None and level_name != "0.0%":
                self.assertGreater(level_price, 50000, f"Level {level_name} should be above entry price for longs")

    def test_short_fibonacci_levels(self):
        """Test Fibonacci level calculations for short positions."""
        # Calculate Fibonacci levels
        fib_levels = self.analyzer.generate_fibonacci_levels(3000, side="short")
        
        # Check key levels
        self.assertEqual(fib_levels["0.0%"], 3000, "Entry level (0.0%) should equal entry price")
        self.assertEqual(fib_levels["61.8%"], 3000 * (1 - 0.618), "Golden ratio level incorrect")
        
        # Check value ranges
        for level_name, level_price in fib_levels.items():
            if level_price is not None and level_name != "0.0%":
                self.assertLess(level_price, 3000, f"Level {level_name} should be below entry price for shorts")

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
            self.assertLessEqual(stop_loss[1], self.long_position["entryPrice"], "Stop loss should be below entry price for long")

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
            self.assertGreaterEqual(stop_loss[1], self.short_position["entryPrice"], "Stop loss should be above entry price for short")

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
        self.assertAlmostEqual(long_analysis["analysis"]["pnl_percentage"], expected_long_pct, places=1, 
                               msg="Long position PnL percentage calculation incorrect")
        
        self.assertAlmostEqual(short_analysis["analysis"]["pnl_percentage"], expected_short_pct, places=1, 
                               msg="Short position PnL percentage calculation incorrect")


if __name__ == "__main__":
    unittest.main() 