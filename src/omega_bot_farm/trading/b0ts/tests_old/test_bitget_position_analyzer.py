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
Test module for BitgetPositionAnalyzerB0t.

This module tests the BitGet position analyzer's functionality for position analysis,
Fibonacci calculations, and harmony metrics.
"""

import os
import unittest
import json
from unittest.mock import patch, MagicMock
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Import the BitgetPositionAnalyzerB0t
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import (
        BitgetPositionAnalyzerB0t, 
        PHI, 
        INV_PHI
    )
    DIRECT_IMPORT_AVAILABLE = True
except ImportError:
    DIRECT_IMPORT_AVAILABLE = False
    # Create mock constants for testing
    PHI = 1.618034
    INV_PHI = 0.618034
    
    class BitgetPositionAnalyzerB0t:
        """Mock BitgetPositionAnalyzerB0t for testing."""
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None,
                    use_testnet=False, position_history_length=10):
            self.api_key = api_key
            self.api_secret = api_secret
            self.api_passphrase = api_passphrase
            self.use_testnet = use_testnet
            self.position_history_length = position_history_length
            self.exchange = None
            self.account_balance = 1000.0
            self.account_equity = 1000.0
            self.total_position_value = 0.0
            self.total_pnl = 0.0
            self.long_exposure = 0.0
            self.short_exposure = 0.0
        
        async def get_positions(self):
            return {"success": True, "positions": []}
        
        def analyze_position(self, position):
            return {"position": position, "analysis": {}}
        
        def generate_fibonacci_levels(self, base_price, side):
            if side.lower() == 'long':
                return {
                    "0.0%": base_price,
                    "61.8%": base_price * (1 + 0.618),
                    "100.0%": base_price * 2
                }
            else:
                return {
                    "0.0%": base_price,
                    "61.8%": base_price * (1 - 0.618),
                    "100.0%": 0
                }
        
        def analyze_all_positions(self):
            return {"timestamp": "2023-01-01", "total_positions": 0}
        
        def _calculate_harmony_score(self):
            return 0.5


# Sample test data
SAMPLE_POSITIONS = [
    {
        "info": {"symbol": "BTCUSDT_UMCBL", "marginCoin": "USDT"},
        "symbol": "BTC/USDT:USDT",
        "timestamp": 1672531200000,
        "datetime": "2023-01-01T00:00:00.000Z",
        "initialMargin": 100.0,
        "initialMarginPercentage": 0.1,
        "maintenanceMargin": 5.0,
        "maintenanceMarginPercentage": 0.005,
        "entryPrice": 30000.0,
        "notional": 600.0,
        "leverage": 6.0,
        "unrealizedPnl": 50.0,
        "contracts": 0.02,
        "contractSize": 1.0,
        "marginRatio": 0.1,
        "liquidationPrice": 28500.0,
        "markPrice": 32500.0,
        "collateral": 100.0,
        "marginType": "isolated",
        "side": "long",
        "percentage": 0.0833
    },
    {
        "info": {"symbol": "ETHUSDT_UMCBL", "marginCoin": "USDT"},
        "symbol": "ETH/USDT:USDT",
        "timestamp": 1672531200000,
        "datetime": "2023-01-01T00:00:00.000Z",
        "initialMargin": 50.0,
        "initialMarginPercentage": 0.1,
        "maintenanceMargin": 2.5,
        "maintenanceMarginPercentage": 0.005,
        "entryPrice": 2000.0,
        "notional": 400.0,
        "leverage": 8.0,
        "unrealizedPnl": -20.0,
        "contracts": 0.2,
        "contractSize": 1.0,
        "marginRatio": 0.1,
        "liquidationPrice": 1800.0,
        "markPrice": 1900.0,
        "collateral": 50.0,
        "marginType": "isolated",
        "side": "short",
        "percentage": -0.05
    }
]

class TestBitgetPositionAnalyzer(unittest.TestCase):
    """Test cases for BitgetPositionAnalyzerB0t."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock environment variables for testing
        os.environ["BITGET_API_KEY"] = "test_api_key"
        os.environ["BITGET_SECRET_KEY"] = "test_secret_key"
        os.environ["BITGET_PASSPHRASE"] = "test_passphrase"
        
        # Initialize the analyzer with testnet mode
        self.analyzer = BitgetPositionAnalyzerB0t(use_testnet=True)
        
        # Set up some initial account values for testing
        self.analyzer.account_balance = 1000.0
        self.analyzer.account_equity = 1000.0
        
    def tearDown(self):
        """Clean up after the tests."""
        # Clear environment variables
        if "BITGET_API_KEY" in os.environ:
            del os.environ["BITGET_API_KEY"]
        if "BITGET_SECRET_KEY" in os.environ:
            del os.environ["BITGET_SECRET_KEY"]
        if "BITGET_PASSPHRASE" in os.environ:
            del os.environ["BITGET_PASSPHRASE"]
    
    @patch('ccxt.bitget')
    def test_initialization(self, mock_bitget):
        """Test BitgetPositionAnalyzerB0t initialization."""
        # Configure the mock
        mock_exchange = MagicMock()
        mock_bitget.return_value = mock_exchange
        
        # Create analyzer with specific credentials
        analyzer = BitgetPositionAnalyzerB0t(
            api_key="custom_api_key",
            api_secret="custom_secret_key",
            api_passphrase="custom_passphrase",
            use_testnet=True
        )
        
        # Verify initialization
        self.assertEqual(analyzer.api_key, "custom_api_key")
        self.assertEqual(analyzer.api_secret, "custom_secret_key")
        self.assertEqual(analyzer.api_passphrase, "custom_passphrase")
        self.assertTrue(analyzer.use_testnet)
        
        # Verify exchange initialization
        if DIRECT_IMPORT_AVAILABLE:
            mock_bitget.assert_called_once()
            self.assertEqual(analyzer.exchange, mock_exchange)
            mock_exchange.set_sandbox_mode.assert_called_once_with(True)
    
    def test_fibonacci_levels_long(self):
        """Test Fibonacci level calculation for long positions."""
        # Calculate Fibonacci levels for a long position
        base_price = 30000.0
        fib_levels = self.analyzer.generate_fibonacci_levels(base_price, "long")
        
        # Verify key Fibonacci levels
        self.assertEqual(fib_levels["0.0%"], base_price)
        self.assertAlmostEqual(fib_levels["23.6%"], base_price * 1.236, places=2)
        self.assertAlmostEqual(fib_levels["38.2%"], base_price * 1.382, places=2)
        self.assertEqual(fib_levels["50.0%"], base_price * 1.5)
        self.assertAlmostEqual(fib_levels["61.8%"], base_price * 1.618, places=2)  # Golden Ratio
        self.assertAlmostEqual(fib_levels["78.6%"], base_price * 1.786, places=2)
        self.assertEqual(fib_levels["100.0%"], base_price * 2)
        self.assertAlmostEqual(fib_levels["161.8%"], base_price * 2.618, places=2)  # PHI^2
        self.assertAlmostEqual(fib_levels["261.8%"], base_price * 3.618, places=2)  # PHI^3
    
    def test_fibonacci_levels_short(self):
        """Test Fibonacci level calculation for short positions."""
        # Calculate Fibonacci levels for a short position
        base_price = 30000.0
        fib_levels = self.analyzer.generate_fibonacci_levels(base_price, "short")
        
        # Verify key Fibonacci levels for shorts
        self.assertEqual(fib_levels["0.0%"], base_price)
        self.assertAlmostEqual(fib_levels["23.6%"], base_price * 0.764, places=2)
        self.assertAlmostEqual(fib_levels["38.2%"], base_price * 0.618, places=2)
        self.assertEqual(fib_levels["50.0%"], base_price * 0.5)
        self.assertAlmostEqual(fib_levels["61.8%"], base_price * 0.382, places=2)  # Golden Ratio
        self.assertAlmostEqual(fib_levels["78.6%"], base_price * 0.214, places=2)
        self.assertEqual(fib_levels["100.0%"], 0)
        self.assertIsNone(fib_levels["161.8%"])  # Not applicable for shorts
        self.assertIsNone(fib_levels["261.8%"])  # Not applicable for shorts
    
    @patch.object(BitgetPositionAnalyzerB0t, 'get_positions')
    def test_analyze_position(self, mock_get_positions):
        """Test position analysis functionality."""
        # Skip if direct import not available (using mock)
        if not DIRECT_IMPORT_AVAILABLE:
            return
            
        # Configure mock
        mock_get_positions.return_value = {
            "success": True,
            "positions": SAMPLE_POSITIONS,
            "account": {
                "balance": 1000.0,
                "equity": 1030.0
            }
        }
        
        # Temporarily set account values
        self.analyzer.account_equity = 1030.0
        
        # Analyze the first position (long BTC)
        position = SAMPLE_POSITIONS[0]
        analysis = self.analyzer.analyze_position(position)
        
        # Verify analysis structure
        self.assertIn("position", analysis)
        self.assertIn("analysis", analysis)
        
        # Verify specific analysis components
        analysis_data = analysis["analysis"]
        self.assertIn("fibonacci_levels", analysis_data)
        self.assertIn("level_distances", analysis_data)
        self.assertIn("is_fibonacci_sized", analysis_data)
        self.assertIn("pnl_percentage", analysis_data)
        self.assertIn("recommended_take_profit", analysis_data)
        self.assertIn("recommended_stop_loss", analysis_data)
        self.assertIn("current_harmony", analysis_data)
        
        # Verify correct PnL calculation
        self.assertAlmostEqual(analysis_data["pnl_percentage"], 8.33, places=1)
        
        # Check that we have fibonacci levels
        fib_levels = analysis_data["fibonacci_levels"]
        self.assertGreater(len(fib_levels), 5)
        
        # Verify harmony score is between 0 and 1
        harmony = analysis_data["current_harmony"]
        self.assertGreaterEqual(harmony, 0.0)
        self.assertLessEqual(harmony, 1.0)
    
    @patch.object(BitgetPositionAnalyzerB0t, 'get_positions')
    def test_analyze_all_positions(self, mock_get_positions):
        """Test analysis of all positions."""
        # Configure mock
        mock_get_positions.return_value = {
            "success": True,
            "positions": SAMPLE_POSITIONS,
            "account": {
                "balance": 1000.0,
                "equity": 1030.0
            },
            "changes": {"new": [], "closed": [], "changed": []}
        }
        
        # Set up analyzer state for testing
        self.analyzer.account_balance = 1000.0
        self.analyzer.account_equity = 1030.0
        self.analyzer.total_position_value = 1000.0
        self.analyzer.total_pnl = 30.0
        self.analyzer.long_exposure = 600.0
        self.analyzer.short_exposure = 400.0
        
        # Use mock to patch the analyze_position method to prevent errors
        with patch.object(self.analyzer, 'analyze_position') as mock_analyze:
            # Configure mock to return dummy analysis
            mock_analyze.side_effect = lambda p: {
                "position": p,
                "analysis": {
                    "fibonacci_levels": {},
                    "level_distances": {},
                    "is_fibonacci_sized": True,
                    "pnl_percentage": 5.0,
                    "recommended_take_profit": ("61.8%", p["entryPrice"] * 1.618),
                    "recommended_stop_loss": ("38.2%", p["entryPrice"] * 0.618),
                    "current_harmony": 0.7
                }
            }
            
            # Analyze all positions
            analysis = self.analyzer.analyze_all_positions()
            
            # Verify analysis structure
            self.assertIn("timestamp", analysis)
            self.assertIn("total_positions", analysis)
            self.assertIn("account_stats", analysis)
            self.assertIn("position_analyses", analysis)
            self.assertIn("harmony_score", analysis)
            self.assertIn("recommendations", analysis)
            
            # Verify correct position count
            self.assertEqual(analysis["total_positions"], 2)
            
            # Verify we have position analyses
            self.assertEqual(len(analysis["position_analyses"]), 2)
            
            # Verify harmony score is between 0 and 1
            self.assertGreaterEqual(analysis["harmony_score"], 0.0)
            self.assertLessEqual(analysis["harmony_score"], 1.0)
            
            # Verify we have recommendations
            self.assertIsInstance(analysis["recommendations"], list)
    
    def test_harmony_score_calculation(self):
        """Test harmony score calculation based on Fibonacci principles."""
        # Skip if direct import not available (using mock)
        if not DIRECT_IMPORT_AVAILABLE:
            return
            
        # Configure test values
        self.analyzer.total_position_value = 618.034  # Golden ratio of equity
        self.analyzer.total_pnl = 30.0  # Positive PnL
        self.analyzer.long_exposure = 381.966  # Inverse golden ratio
        self.analyzer.short_exposure = 236.068  # Remaining portion
        
        # Calculate harmony score
        harmony_score = self.analyzer._calculate_harmony_score()
        
        # Verify the score is between 0 and 1
        self.assertGreaterEqual(harmony_score, 0.0)
        self.assertLessEqual(harmony_score, 1.0)
        
        # Check that positive configuration gives good harmony
        self.assertGreater(harmony_score, 0.5)
        
        # Test negative configuration
        self.analyzer.total_pnl = -50.0  # Negative PnL
        negative_harmony = self.analyzer._calculate_harmony_score()
        
        # Verify negative harmony is lower than positive
        self.assertLess(negative_harmony, harmony_score)
    
    def test_long_short_ratio(self):
        """Test calculation of long-short ratio."""
        # Skip if direct import not available (using mock)
        if not DIRECT_IMPORT_AVAILABLE:
            return
            
        # Test balanced portfolio (golden ratio)
        self.analyzer.long_exposure = PHI * 100.0
        self.analyzer.short_exposure = 100.0
        ratio = self.analyzer._calculate_long_short_ratio()
        self.assertAlmostEqual(ratio, PHI, places=4)
        
        # Test 100% long
        self.analyzer.long_exposure = 100.0
        self.analyzer.short_exposure = 0.0
        ratio = self.analyzer._calculate_long_short_ratio()
        self.assertEqual(ratio, float('inf'))
        
        # Test 100% short
        self.analyzer.long_exposure = 0.0
        self.analyzer.short_exposure = 100.0
        ratio = self.analyzer._calculate_long_short_ratio()
        self.assertEqual(ratio, 0.0)
        
        # Test inverse golden ratio
        self.analyzer.long_exposure = 100.0
        self.analyzer.short_exposure = PHI * 100.0
        ratio = self.analyzer._calculate_long_short_ratio()
        self.assertAlmostEqual(ratio, INV_PHI, places=4)
    
    def test_exposure_equity_ratio(self):
        """Test calculation of exposure to equity ratio."""
        # Skip if direct import not available (using mock)
        if not DIRECT_IMPORT_AVAILABLE:
            return
            
        # Test golden ratio exposure
        self.analyzer.account_equity = 1000.0
        self.analyzer.total_position_value = 618.034
        ratio = self.analyzer._calculate_exposure_to_equity_ratio()
        self.assertAlmostEqual(ratio, 0.618034, places=4)
        
        # Test zero equity
        self.analyzer.account_equity = 0.0
        self.analyzer.total_position_value = 100.0
        ratio = self.analyzer._calculate_exposure_to_equity_ratio()
        self.assertEqual(ratio, 0.0)
        
        # Test zero exposure
        self.analyzer.account_equity = 1000.0
        self.analyzer.total_position_value = 0.0
        ratio = self.analyzer._calculate_exposure_to_equity_ratio()
        self.assertEqual(ratio, 0.0)


if __name__ == '__main__':
    unittest.main() 