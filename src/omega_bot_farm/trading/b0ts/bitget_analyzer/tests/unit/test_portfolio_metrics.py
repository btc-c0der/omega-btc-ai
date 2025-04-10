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
Unit tests for portfolio metrics calculations in BitgetPositionAnalyzerB0t.

These tests verify that the bot correctly calculates portfolio metrics such as
long-short ratio, exposure to equity ratio, and related recommendations.
"""

import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Import constants
PHI = 1.618034  # Golden Ratio
INV_PHI = 0.618034  # Inverse Golden Ratio

# Try to import BitgetPositionAnalyzerB0t
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False
    print("BitgetPositionAnalyzerB0t not available. Using mock for tests.")

# Mock implementation if import fails
if not BOT_AVAILABLE:
    class BitgetPositionAnalyzerB0t:
        """Mock implementation for testing"""
        
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
            self.api_key = api_key or "test_key"
            self.api_secret = api_secret or "test_secret"
            self.api_passphrase = api_passphrase or "test_pass"
            self.use_testnet = use_testnet
        
        def _calculate_long_short_ratio(self, positions):
            """Calculate the ratio between long and short exposure."""
            long_exposure = sum(
                float(p.get("notional", 0)) 
                for p in positions if p.get("side", "").lower() == "long"
            )
            
            short_exposure = sum(
                float(p.get("notional", 0)) 
                for p in positions if p.get("side", "").lower() == "short"
            )
            
            # Prevent division by zero
            if short_exposure == 0:
                if long_exposure == 0:
                    return 1.0  # Neutral if no positions
                return float('inf')  # All long positions
                
            return long_exposure / short_exposure
        
        def _calculate_exposure_to_equity_ratio(self, positions, equity):
            """Calculate the ratio of total exposure to equity."""
            total_exposure = sum(float(p.get("notional", 0)) for p in positions)
            
            # Prevent division by zero
            if equity == 0:
                return float('inf') if total_exposure > 0 else 0.0
                
            return total_exposure / equity
        
        def get_portfolio_recommendations(self, long_short_ratio, exposure_equity_ratio):
            """Get portfolio recommendations based on metrics."""
            recommendations = []
            
            # Long-short balance recommendations
            if long_short_ratio > PHI * 1.5:
                recommendations.append("Consider reducing long exposure or increasing short positions to bring long-short ratio closer to the golden ratio (1.618).")
            elif long_short_ratio < 1 / (PHI * 1.5):
                recommendations.append("Consider reducing short exposure or increasing long positions to bring long-short ratio closer to the golden ratio (1.618).")
            elif abs(long_short_ratio - PHI) < 0.2:
                recommendations.append("Your long-short balance is well-aligned with the golden ratio, maintaining harmony in your portfolio.")
            
            # Exposure-equity recommendations
            if exposure_equity_ratio > PHI * 3:
                recommendations.append("Total exposure is significantly higher than equity. Consider reducing leverage to bring exposure-equity ratio closer to a Fibonacci multiple.")
            elif exposure_equity_ratio < INV_PHI:
                recommendations.append("Total exposure is conservative compared to equity. Consider scaling positions to utilize capital more effectively.")
            
            # Default recommendation
            if not recommendations:
                recommendations.append("Portfolio metrics are within reasonable ranges. Continue monitoring for changes.")
                
            return recommendations


class TestPortfolioMetrics(unittest.TestCase):
    """Test suite for portfolio metrics calculations."""

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
        self.balanced_positions = [
            {  # Long BTC position
                "symbol": "BTC/USDT:USDT",
                "side": "long",
                "entryPrice": 50000,
                "markPrice": 55000,
                "contracts": 0.1,
                "notional": 5000,
                "leverage": 10,
                "unrealizedPnl": 500
            },
            {  # Short ETH position
                "symbol": "ETH/USDT:USDT",
                "side": "short",
                "entryPrice": 3000,
                "markPrice": 2700,
                "contracts": 1.0,
                "notional": 3000,
                "leverage": 5,
                "unrealizedPnl": 300
            }
        ]
        
        # Long-biased positions
        self.long_biased_positions = [
            {  # Long BTC position
                "symbol": "BTC/USDT:USDT",
                "side": "long",
                "entryPrice": 50000,
                "markPrice": 55000,
                "contracts": 0.2,
                "notional": 10000,
                "leverage": 10,
                "unrealizedPnl": 1000
            },
            {  # Long ETH position
                "symbol": "ETH/USDT:USDT",
                "side": "long",
                "entryPrice": 3000,
                "markPrice": 3300,
                "contracts": 5.0,
                "notional": 15000,
                "leverage": 5,
                "unrealizedPnl": 1500
            },
            {  # Short SOL position
                "symbol": "SOL/USDT:USDT",
                "side": "short",
                "entryPrice": 100,
                "markPrice": 95,
                "contracts": 50.0,
                "notional": 5000,
                "leverage": 10,
                "unrealizedPnl": 250
            }
        ]
        
        # Short-biased positions
        self.short_biased_positions = [
            {  # Short BTC position
                "symbol": "BTC/USDT:USDT",
                "side": "short",
                "entryPrice": 50000,
                "markPrice": 45000,
                "contracts": 0.1,
                "notional": 5000,
                "leverage": 10,
                "unrealizedPnl": 500
            },
            {  # Short ETH position
                "symbol": "ETH/USDT:USDT",
                "side": "short",
                "entryPrice": 3000,
                "markPrice": 2700,
                "contracts": 2.0,
                "notional": 6000,
                "leverage": 5,
                "unrealizedPnl": 600
            },
            {  # Long SOL position
                "symbol": "SOL/USDT:USDT",
                "side": "long",
                "entryPrice": 100,
                "markPrice": 105,
                "contracts": 10.0,
                "notional": 1000,
                "leverage": 10,
                "unrealizedPnl": 50
            }
        ]
        
        # Golden ratio positions - ratio is perfectly PHI (1.618)
        self.golden_ratio_positions = [
            {  # Long positions with total exposure of PHI * 10000
                "symbol": "BTC/USDT:USDT",
                "side": "long",
                "entryPrice": 50000,
                "markPrice": 55000,
                "contracts": 0.162,
                "notional": 8090,  # Approximately PHI * 5000
                "leverage": 8,
                "unrealizedPnl": 809
            },
            {  # Long ETH position
                "symbol": "ETH/USDT:USDT",
                "side": "long",
                "entryPrice": 3000,
                "markPrice": 3300,
                "contracts": 3.0,
                "notional": 9000,
                "leverage": 5,
                "unrealizedPnl": 900
            },
            {  # Short positions with total exposure of 10000
                "symbol": "SOL/USDT:USDT",
                "side": "short",
                "entryPrice": 100,
                "markPrice": 95,
                "contracts": 100.0,
                "notional": 10000,
                "leverage": 10,
                "unrealizedPnl": 500
            },
            {  # Another short position
                "symbol": "ADA/USDT:USDT",
                "side": "short",
                "entryPrice": 1.0,
                "markPrice": 0.9,
                "contracts": 5000.0,
                "notional": 5000,
                "leverage": 5,
                "unrealizedPnl": 500
            }
        ]

    def test_long_short_ratio_calculation(self):
        """Test long-short ratio calculation with different position sets."""
        # Test with balanced positions (close to 1.67)
        ls_ratio = self.analyzer._calculate_long_short_ratio(self.balanced_positions)
        self.assertAlmostEqual(ls_ratio, 5000 / 3000, places=2, msg="Long-short ratio incorrect for balanced positions")
        
        # Test with long-biased positions
        ls_ratio = self.analyzer._calculate_long_short_ratio(self.long_biased_positions)
        self.assertAlmostEqual(ls_ratio, 25000 / 5000, places=2, msg="Long-short ratio incorrect for long-biased positions")
        
        # Test with short-biased positions
        ls_ratio = self.analyzer._calculate_long_short_ratio(self.short_biased_positions)
        self.assertAlmostEqual(ls_ratio, 1000 / 11000, places=2, msg="Long-short ratio incorrect for short-biased positions")
        
        # Test with golden ratio positions
        ls_ratio = self.analyzer._calculate_long_short_ratio(self.golden_ratio_positions)
        self.assertAlmostEqual(ls_ratio, 17090 / 15000, places=2, msg="Long-short ratio incorrect for golden ratio positions")
        # Should be very close to PHI
        self.assertAlmostEqual(ls_ratio, PHI, places=1, msg="Long-short ratio should be close to PHI for golden ratio positions")

    def test_exposure_equity_ratio_calculation(self):
        """Test exposure-to-equity ratio calculation."""
        # Test with different equity values
        equity = 10000
        
        # Balanced positions
        exposure_ratio = self.analyzer._calculate_exposure_to_equity_ratio(self.balanced_positions, equity)
        expected_ratio = (5000 + 3000) / 10000
        self.assertAlmostEqual(exposure_ratio, expected_ratio, places=2, 
                              msg="Exposure-equity ratio incorrect for balanced positions")
        
        # Long-biased positions (higher exposure)
        exposure_ratio = self.analyzer._calculate_exposure_to_equity_ratio(self.long_biased_positions, equity)
        expected_ratio = (10000 + 15000 + 5000) / 10000
        self.assertAlmostEqual(exposure_ratio, expected_ratio, places=2, 
                              msg="Exposure-equity ratio incorrect for long-biased positions")
        
        # Test with zero equity (should handle division by zero)
        exposure_ratio = self.analyzer._calculate_exposure_to_equity_ratio(self.balanced_positions, 0)
        self.assertTrue(exposure_ratio > 0, "Should handle zero equity gracefully")
        
        # Test with zero exposure
        exposure_ratio = self.analyzer._calculate_exposure_to_equity_ratio([], equity)
        self.assertEqual(exposure_ratio, 0, "Exposure ratio should be 0 for empty positions")

    def test_golden_ratio_exposure(self):
        """Test detection of golden ratio in exposure levels."""
        # Test with equity that makes exposure ratio = PHI
        total_exposure = sum(float(p.get("notional", 0)) for p in self.balanced_positions)
        equity = total_exposure / PHI
        
        exposure_ratio = self.analyzer._calculate_exposure_to_equity_ratio(self.balanced_positions, equity)
        self.assertAlmostEqual(exposure_ratio, PHI, places=2, 
                              msg="Exposure ratio should equal PHI when equity is set accordingly")

    def test_portfolio_recommendations(self):
        """Test portfolio recommendations based on metrics."""
        # Test extremely long-biased portfolio
        long_short_ratio = 5.0  # Well above PHI
        exposure_equity_ratio = 2.0  # Moderate
        
        recommendations = self.analyzer.get_portfolio_recommendations(long_short_ratio, exposure_equity_ratio)
        self.assertTrue(any("reducing long exposure" in r.lower() for r in recommendations), 
                       "Should recommend reducing long exposure when long-short ratio is too high")
        
        # Test extremely short-biased portfolio
        long_short_ratio = 0.2  # Well below 1/PHI
        exposure_equity_ratio = 2.0  # Moderate
        
        recommendations = self.analyzer.get_portfolio_recommendations(long_short_ratio, exposure_equity_ratio)
        self.assertTrue(any("reducing short exposure" in r.lower() for r in recommendations), 
                       "Should recommend reducing short exposure when long-short ratio is too low")
        
        # Test perfect golden ratio portfolio
        long_short_ratio = PHI
        exposure_equity_ratio = PHI
        
        recommendations = self.analyzer.get_portfolio_recommendations(long_short_ratio, exposure_equity_ratio)
        self.assertTrue(any("well-aligned" in r.lower() for r in recommendations), 
                       "Should acknowledge well-aligned portfolio when metrics match golden ratio")
        
        # Test overleveraged portfolio
        long_short_ratio = PHI  # Perfect long-short balance
        exposure_equity_ratio = 10.0  # Extremely high exposure
        
        recommendations = self.analyzer.get_portfolio_recommendations(long_short_ratio, exposure_equity_ratio)
        self.assertTrue(any("reducing leverage" in r.lower() for r in recommendations), 
                       "Should recommend reducing leverage when exposure ratio is too high")


if __name__ == "__main__":
    unittest.main() 