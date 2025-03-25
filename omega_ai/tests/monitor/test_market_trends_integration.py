#!/usr/bin/env python3

import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock
import redis

# Add the project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from omega_ai.monitor.monitor_market_trends_fixed import (
    MarketTrendAnalyzer,
    detect_possible_mm_traps,
    check_system_warnings
)

class TestMarketTrendsIntegration(unittest.TestCase):
    """Integration tests for monitor_market_trends_fixed with fallback system."""

    @patch('omega_ai.monitor.monitor_market_trends_fixed.redis_conn')
    def test_analyzer_with_fallback(self, mock_redis):
        """Test the MarketTrendAnalyzer with fallback system."""
        # Set up mock Redis data with btc_trend_15min set to None to force fallback
        mock_data = {
            # Return None for primary data sources to trigger fallbacks
            "btc_trend_15min": None, 
            "btc_trend_1h": None,
            # Return data for fallback sources - specifically 5min should be available
            "btc_trend_5min": json.dumps({"trend": "Bullish", "strength": 0.8}),
            "btc_candle_15min": None,
            "btc_candle_5min": json.dumps({
                'o': 50000,  # Open price
                'c': 52000,  # Close price (4% increase)
                'h': 52500,  # High
                'l': 49800,  # Low
                'v': 1000,   # Volume
                't': 1615882800000  # Timestamp
            }),
            "last_btc_price": "51000.0",
            # Provide fibonacci data
            "fibonacci_levels": json.dumps({
                'base_price': 50000,
                'direction': 'up',
                'levels': {
                    '0': 50000,
                    '0.236': 47640,
                    '0.382': 46180,
                    '0.5': 45000,
                    '0.618': 43820,
                    '0.786': 42140,
                    '1.0': 40000
                },
                'timestamp': '2023-03-24T12:00:00'
            })
        }
        
        # Mock functions beyond the Redis get/exists
        def mock_ensure_trend_data(timeframe):
            if timeframe == "15min":
                return {
                    "data": "Bullish",
                    "source": "fallback_timeframe",
                    "timeframe": "5min"
                }
            elif timeframe == "1h":
                return {
                    "data": "Neutral",
                    "source": "fallback_timeframe",
                    "timeframe": "30min"
                }
            return {
                "data": "No Data",
                "source": "default",
                "timeframe": timeframe
            }
        
        mock_redis.get.side_effect = lambda key: mock_data.get(key, None)
        mock_redis.exists.return_value = True  # Ensure Redis connection check passes
        
        # Patch the ensure_trend_data function
        with patch('omega_ai.monitor.monitor_market_trends_fixed.ensure_trend_data', side_effect=mock_ensure_trend_data):
            # Create analyzer instance
            analyzer = MarketTrendAnalyzer()
            
            # Get analysis results
            results = analyzer.analyze_trends()
            
            # Verify primary results
            self.assertIsNotNone(results)
            self.assertEqual(results["current_price"], 51000.0)
            
            # Verify fallback was used for 15min timeframe
            self.assertTrue("15min" in results["trends"])
            self.assertTrue("sources" in results)
            self.assertTrue("15min" in results["sources"])
            
            # A proper fallback source should be indicated
            source_15min = results["sources"]["15min"]
            self.assertIsNotNone(source_15min)
            self.assertEqual(source_15min, "fallback_timeframe")
            
            # Test that 1h also has some fallback
            self.assertTrue("1h" in results["trends"])
            self.assertIsNotNone(results["trends"]["1h"])
            
            # Verify that sources were tracked
            self.assertTrue(any(source != "primary" for source in results["sources"].values()))

    @patch('omega_ai.monitor.monitor_market_trends_fixed.redis_conn')
    def test_trap_detection_with_fallback(self, mock_redis):
        """Test MM trap detection with fallback mechanisms."""
        # Set up mock Redis
        mock_data = {
            "btc_trend_15min": None,  # Force fallback
            "btc_candle_15min": json.dumps({
                'o': 50000,  # Open price
                'c': 48000,  # Close price (4% decrease)
                'h': 50100,  # High
                'l': 47500,  # Low
                'v': 1000,   # Volume
                't': 1615882800000
            }),
            "last_btc_price": "48500.0",
            "market_manipulation_history": json.dumps([
                {"timeframe": "15min", "pattern": "Bear Trap", "timestamp": 1615882700000},
                {"timeframe": "1h", "pattern": "Bull Trap", "timestamp": 1615879200000}
            ])
        }
        
        mock_redis.get.side_effect = lambda key: mock_data.get(key, None)
        mock_redis.exists.return_value = True  # Ensure Redis connection check passes
        
        # Calculate price move percent for the trap detection
        open_price = 50000
        close_price = 48000
        price_change_pct = (close_price - open_price) / open_price * 100  # -4.0%
        price_move = close_price - open_price  # -2000
        
        # Call trap detection with realistic data
        trap_type, confidence = detect_possible_mm_traps("15min", "Bearish", price_change_pct, price_move)
        
        # Verify fallback worked and detected a trap
        self.assertIsNotNone(trap_type)
        self.assertGreater(confidence, 0.3)
        self.assertEqual(trap_type, "Bear Trap")  # Expect Bear Trap pattern based on implementation

    @patch('omega_ai.monitor.monitor_market_trends_fixed.redis_conn')
    def test_system_warnings(self, mock_redis):
        """Test system warnings retrieval with fallback mechanisms."""
        # Set up mock Redis
        warning1 = json.dumps({
            "id": 1234567890,
            "type": "PRICE_ERROR",
            "message": "Invalid price data",
            "source": "fallback_helper",
            "timestamp": "2023-03-24T12:00:00"
        })
        
        warning2 = json.dumps({
            "id": 1234567891,
            "type": "TIMEFRAME_FALLBACK",
            "message": "Used 5min data for 15min",
            "source": "fallback_helper",
            "timestamp": "2023-03-24T12:01:00"
        })
        
        # Set up mock Redis responses for the correct keys
        mock_redis.lrange.side_effect = lambda key, start, end: {
            "system:warnings": ["1234567890", "1234567891"],
            "system:warnings:PRICE_ERROR": ["1234567890"],
            "system:warnings:TIMEFRAME_FALLBACK": ["1234567891"]
        }.get(key, [])
        
        mock_redis.llen.return_value = 2
        mock_redis.exists.return_value = True
        mock_redis.hgetall.return_value = {
            "PRICE_ERROR": "1", 
            "TIMEFRAME_FALLBACK": "1"
        }
        
        def mock_get_side_effect(key):
            if key == "warning:1234567890":
                return warning1
            elif key == "warning:1234567891":
                return warning2
            return None
        
        mock_redis.get.side_effect = mock_get_side_effect
        
        # Get the warning results directly instead of capturing stdout
        warning_results = check_system_warnings(limit=10)
        
        # Verify warnings were processed
        self.assertIsNotNone(warning_results)
        self.assertEqual(warning_results["total_warnings"], 2)
        self.assertEqual(len(warning_results["warnings"]), 2)
        
        # Now capture stdout for the display portion
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            # Ensure the function has a print statement inside
            with patch('omega_ai.monitor.monitor_market_trends_fixed.print') as mock_print:
                mock_print.side_effect = print  # Still print to our captured stdout
                check_system_warnings(limit=10)
        
        # Get the captured output
        output = f.getvalue()
        
        # The test doesn't match the implementation because check_system_warnings doesn't
        # print anything by itself - it only returns data. Let's test the data instead.
        self.assertEqual(warning_results["counts_by_type"]["PRICE_ERROR"], "1")

if __name__ == '__main__':
    unittest.main() 