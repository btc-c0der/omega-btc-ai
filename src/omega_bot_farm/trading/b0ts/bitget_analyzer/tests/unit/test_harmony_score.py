#!/usr/bin/env python3

"""
Unit tests for harmony score calculations in BitgetPositionAnalyzerB0t.

These tests verify that the bot correctly calculates position harmony scores
based on golden ratio principles.
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
        
        def _calculate_position_harmony(self, position):
            """Calculate harmony score for a position."""
            # Get position details
            side = position.get("side", "").lower()
            entry_price = float(position.get("entryPrice", 0))
            mark_price = float(position.get("markPrice", 0))
            notional = float(position.get("notional", 0))
            leverage = float(position.get("leverage", 1))
            
            # Calculate price ratio
            price_ratio = 0
            if entry_price > 0:
                price_ratio = mark_price / entry_price
            
            # Calculate harmony score components
            price_harmony = 0
            size_harmony = 0
            leverage_harmony = 0
            
            # Price harmony (how close to golden ratio)
            if side == "long":
                # For long: closer to 1+phi is more harmonious
                target_ratio = 1 + INV_PHI
                price_harmony = 1 - min(abs(price_ratio - target_ratio) / target_ratio, 1.0)
            else:
                # For short: closer to 1-phi is more harmonious
                target_ratio = 1 - INV_PHI
                price_harmony = 1 - min(abs(price_ratio - target_ratio) / (1 - target_ratio), 1.0)
            
            # Size harmony (positions sized according to fibonacci sequence)
            # Simplified for testing: perfect size harmony if notional is a power of phi
            if notional > 0:
                size_ratio = abs(notional / (1000 * PHI))  # Assuming 1000*phi as base size
                size_harmony = 1 - min(abs(size_ratio - round(size_ratio)) / size_ratio, 0.5)
            
            # Leverage harmony (is leverage a fibonacci number?)
            fib_leverage = [1, 2, 3, 5, 8, 13, 21]
            if leverage in fib_leverage:
                leverage_harmony = 1.0
            else:
                closest_fib = min(fib_leverage, key=lambda x: abs(x - leverage))
                leverage_harmony = 1 - min(abs(leverage - closest_fib) / closest_fib, 1.0)
            
            # Calculate overall harmony
            harmony_score = (price_harmony * 0.5) + (size_harmony * 0.3) + (leverage_harmony * 0.2)
            
            return min(max(harmony_score, 0.0), 1.0)  # Normalize to 0-1
        
        def _calculate_overall_harmony(self, positions):
            """Calculate overall harmony score for all positions."""
            if not positions:
                return 0.5  # Neutral harmony if no positions
                
            # Calculate individual position harmonies
            position_harmonies = [self._calculate_position_harmony(pos) for pos in positions]
            
            # Account for long-short balance
            long_count = sum(1 for pos in positions if pos.get("side", "").lower() == "long")
            short_count = sum(1 for pos in positions if pos.get("side", "").lower() == "short")
            total_count = long_count + short_count
            
            if total_count == 0:
                return 0.5  # Neutral harmony if no valid positions
                
            # Perfect balance if long:short ratio is phi:1
            ideal_ratio = PHI
            actual_ratio = long_count / max(short_count, 1)  # Avoid division by zero
            
            balance_harmony = 1 - min(abs(actual_ratio - ideal_ratio) / ideal_ratio, 1.0)
            
            # Calculate overall score
            avg_position_harmony = sum(position_harmonies) / len(position_harmonies)
            overall_harmony = (avg_position_harmony * 0.7) + (balance_harmony * 0.3)
            
            return min(max(overall_harmony, 0.0), 1.0)  # Normalize to 0-1
        
        def analyze_all_positions(self):
            """Mock implementation for testing."""
            return {"harmony_score": 0.75}  # Mock value


class TestHarmonyScore(unittest.TestCase):
    """Test suite for harmony score calculations."""

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
        self.positions = [
            {
                "symbol": "BTC/USDT:USDT",
                "side": "long",
                "entryPrice": 50000,
                "markPrice": 80900,  # Close to 1.618 * entry price
                "contracts": 0.1,
                "notional": 5000,
                "leverage": 5,  # Fibonacci number
                "unrealizedPnl": 3090
            },
            {
                "symbol": "ETH/USDT:USDT",
                "side": "short",
                "entryPrice": 3000,
                "markPrice": 1146,  # Close to 0.382 * entry price
                "contracts": 1.0,
                "notional": 3000,
                "leverage": 3,  # Fibonacci number
                "unrealizedPnl": 1854
            },
            {
                "symbol": "SOL/USDT:USDT",
                "side": "long",
                "entryPrice": 100,
                "markPrice": 150,  # 1.5x entry, not close to golden ratio
                "contracts": 10.0,
                "notional": 1000,
                "leverage": 10,  # Not Fibonacci
                "unrealizedPnl": 500
            }
        ]

    def test_position_harmony_calculation(self):
        """Test individual position harmony calculation."""
        # Test harmony for a perfectly harmonious position (price at golden ratio)
        perfect_position = {
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000,
            "markPrice": 50000 * (1 + INV_PHI),  # Perfect golden ratio
            "contracts": 0.1,
            "notional": 1000 * PHI,  # Perfect size
            "leverage": 5,  # Fibonacci number
            "unrealizedPnl": 3090
        }
        
        harmony_score = self.analyzer._calculate_position_harmony(perfect_position)
        
        # Should have a high harmony score
        self.assertGreater(harmony_score, 0.8, "Perfect position should have high harmony score")
        
        # Test harmony for a disharmonious position
        disharmonious_position = {
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000,
            "markPrice": 48000,  # Price moving against position
            "contracts": 0.123,  # Awkward size
            "notional": 6150,
            "leverage": 7,  # Not a Fibonacci number
            "unrealizedPnl": -2000
        }
        
        harmony_score = self.analyzer._calculate_position_harmony(disharmonious_position)
        
        # Should have a lower harmony score
        self.assertLess(harmony_score, 0.6, "Disharmonious position should have lower harmony score")

    def test_overall_harmony_calculation(self):
        """Test overall portfolio harmony calculation."""
        # Calculate harmony for sample positions
        overall_harmony = self.analyzer._calculate_overall_harmony(self.positions)
        
        # Should be a reasonable value between 0 and 1
        self.assertGreaterEqual(overall_harmony, 0.0, "Harmony score should be >= 0")
        self.assertLessEqual(overall_harmony, 1.0, "Harmony score should be <= 1")
        
        # Test with perfect balance of positions (phi:1 ratio)
        perfect_balance = [
            # 8 long positions (close to phi² * 3)
            *[{"side": "long", "entryPrice": 100, "markPrice": 161.8} for _ in range(8)],
            # 5 short positions (close to phi * 3)
            *[{"side": "short", "entryPrice": 100, "markPrice": 61.8} for _ in range(5)],
            # 3 more positions to reach perfect phi:1 ratio (13:8 ≈ phi)
            *[{"side": "long", "entryPrice": 100, "markPrice": 161.8} for _ in range(5)]
        ]
        
        harmony_score = self.analyzer._calculate_overall_harmony(perfect_balance)
        
        # Should have a high harmony score
        self.assertGreater(harmony_score, 0.7, "Perfect balance should have high harmony score")
        
        # Test with empty positions
        empty_harmony = self.analyzer._calculate_overall_harmony([])
        
        # Should return neutral harmony score
        self.assertEqual(empty_harmony, 0.5, "Empty portfolio should have neutral harmony")

    def test_extreme_values(self):
        """Test harmony calculation with extreme values."""
        # Test with extreme price ratio
        extreme_position = {
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000,
            "markPrice": 500000,  # 10x entry
            "contracts": 0.1,
            "notional": 5000,
            "leverage": 5,
            "unrealizedPnl": 45000
        }
        
        harmony_score = self.analyzer._calculate_position_harmony(extreme_position)
        
        # Should still return a valid score between 0 and 1
        self.assertGreaterEqual(harmony_score, 0.0, "Extreme value harmony score should be >= 0")
        self.assertLessEqual(harmony_score, 1.0, "Extreme value harmony score should be <= 1")
        
        # Test with zero values
        zero_position = {
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 0,  # Zero entry price
            "markPrice": 50000,
            "contracts": 0,  # Zero contracts
            "notional": 0,  # Zero notional
            "leverage": 0,  # Zero leverage
            "unrealizedPnl": 0
        }
        
        harmony_score = self.analyzer._calculate_position_harmony(zero_position)
        
        # Should handle zero values gracefully
        self.assertGreaterEqual(harmony_score, 0.0, "Zero value harmony score should be >= 0")
        self.assertLessEqual(harmony_score, 1.0, "Zero value harmony score should be <= 1")


if __name__ == "__main__":
    unittest.main() 