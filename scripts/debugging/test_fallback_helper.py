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
Test script for the fallback helper module
"""

import sys
import logging
import unittest
import json
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import the fallback helper module
try:
    from omega_ai.db_manager.fallback_helper import (
        ensure_trend_data,
        get_fallback_from_nearby_timeframes,
        ensure_fibonacci_levels,
        create_fibonacci_levels,
        get_redis_connection
    )
    logger.info("Successfully imported fallback_helper module")
except ImportError as e:
    logger.error(f"Failed to import fallback_helper module: {e}")
    logger.error("Make sure you're running this from the project root directory")
    sys.exit(1)

class TestFallbackHelper(unittest.TestCase):
    """Test cases for the fallback helper module"""
    
    def setUp(self):
        """Set up the test environment"""
        # Create a mock Redis connection
        self.redis_mock = MagicMock()
        
        # Mock the get_redis_connection function
        patcher = patch('omega_ai.db_manager.fallback_helper.get_redis_connection', return_value=self.redis_mock)
        self.mock_get_redis = patcher.start()
        self.addCleanup(patcher.stop)
        
        # Set up common test data
        self.timeframe = 15  # 15min timeframe
        self.current_price = 50000.0
        
        # Sample candle data
        self.candle_data = [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "open": 49000.0,
                "high": 50500.0,
                "low": 48800.0,
                "close": 50000.0,
                "volume": 100.0
            },
            {
                "timestamp": (datetime.now(timezone.utc)).isoformat(),
                "open": 48000.0,
                "high": 49500.0,
                "low": 47800.0,
                "close": 49000.0,
                "volume": 90.0
            }
        ]
        
        # Sample trend data
        self.trend_data = {
            "trend": "Bullish",
            "change_pct": 2.0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Sample Fibonacci levels
        self.fib_levels = {
            "high": 60000.0,
            "low": 40000.0,
            "fib_0": 40000.0,
            "fib_0.236": 44720.0,
            "fib_0.382": 47640.0,
            "fib_0.5": 50000.0,
            "fib_0.618": 52360.0,
            "fib_0.786": 55720.0,
            "fib_1": 60000.0,
            "fib_1.272": 65440.0,
            "fib_1.618": 72360.0,
            "last_update": datetime.now(timezone.utc).isoformat()
        }
    
    def test_ensure_trend_data_existing(self):
        """Test ensure_trend_data when trend data exists"""
        # Mock Redis to return existing trend data
        self.redis_mock.get.return_value = json.dumps(self.trend_data)
        
        # Call the function
        trend, change_pct = ensure_trend_data(self.timeframe)
        
        # Check the results
        self.assertEqual(trend, "Bullish")
        self.assertEqual(change_pct, 2.0)
        
        # Verify the Redis calls
        self.redis_mock.get.assert_called_once_with(f"btc_trend_{self.timeframe}min")
    
    def test_ensure_trend_data_from_candles(self):
        """Test ensure_trend_data when trend data needs to be created from candles"""
        # Mock Redis to return no trend data but valid candle data
        self.redis_mock.get.side_effect = [None, json.dumps(self.candle_data)]
        
        # Call the function
        trend, change_pct = ensure_trend_data(self.timeframe)
        
        # Check the results
        self.assertIn(trend, ["Bullish", "Bearish", "Neutral", "Strongly Bullish", "Strongly Bearish"])
        self.assertIsInstance(change_pct, float)
        
        # Verify the Redis calls
        self.redis_mock.get.assert_any_call(f"btc_trend_{self.timeframe}min")
        self.redis_mock.get.assert_any_call(f"btc_candles_{self.timeframe}min")
    
    def test_ensure_trend_data_fallback(self):
        """Test ensure_trend_data when fallback is needed"""
        # Mock Redis to return no trend data and no candle data
        self.redis_mock.get.side_effect = [None, None]
        
        # Mock get_fallback_from_nearby_timeframes to return a known value
        with patch('omega_ai.db_manager.fallback_helper.get_fallback_from_nearby_timeframes') as mock_fallback:
            mock_fallback.return_value = ("Neutral", 0.0)
            
            # Call the function
            trend, change_pct = ensure_trend_data(self.timeframe)
            
            # Check the results
            self.assertEqual(trend, "Neutral")
            self.assertEqual(change_pct, 0.0)
            
            # Verify the fallback was called
            mock_fallback.assert_called_once_with(self.timeframe)
    
    def test_get_fallback_from_nearby_timeframes(self):
        """Test get_fallback_from_nearby_timeframes"""
        # Mock Redis to return trend data for a nearby timeframe (5min)
        nearby_trend_data = {
            "trend": "Bearish",
            "change_pct": -1.5,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Set up the Redis mock to return data for different timeframes
        def mock_get(key):
            if key == "btc_trend_5min":
                return json.dumps(nearby_trend_data)
            return None
        
        self.redis_mock.get.side_effect = mock_get
        
        # Call the function
        trend, change_pct = get_fallback_from_nearby_timeframes(self.timeframe)
        
        # Check the results
        self.assertEqual(trend, "Bearish")
        self.assertEqual(change_pct, -1.5)
        
        # Verify the Redis calls for setting the fallback data
        self.redis_mock.set.assert_called_once()
    
    def test_get_fallback_default(self):
        """Test get_fallback_from_nearby_timeframes when no data is available"""
        # Mock Redis to return no data for any timeframe
        self.redis_mock.get.return_value = None
        
        # Call the function
        trend, change_pct = get_fallback_from_nearby_timeframes(self.timeframe)
        
        # Check the results
        self.assertEqual(trend, "Neutral")
        self.assertEqual(change_pct, 0.0)
        
        # Verify the Redis calls for setting the default data
        self.redis_mock.set.assert_called_once()
    
    def test_ensure_fibonacci_levels_existing(self):
        """Test ensure_fibonacci_levels when levels exist"""
        # Mock Redis to return existing Fibonacci levels
        self.redis_mock.get.return_value = json.dumps(self.fib_levels)
        
        # Call the function
        result = ensure_fibonacci_levels(self.current_price)
        
        # Check the results
        self.assertEqual(result["high"], 60000.0)
        self.assertEqual(result["low"], 40000.0)
        self.assertEqual(result["fib_0.618"], 52360.0)
        
        # Verify the Redis calls
        self.redis_mock.get.assert_called_once_with("fibonacci_levels")
    
    def test_ensure_fibonacci_levels_missing_fields(self):
        """Test ensure_fibonacci_levels when some fields are missing"""
        # Create incomplete Fibonacci data
        incomplete_fib = {
            "high": 60000.0,
            "low": 40000.0,
            "last_update": datetime.now(timezone.utc).isoformat()
        }
        
        # Mock Redis to return incomplete Fibonacci levels
        self.redis_mock.get.return_value = json.dumps(incomplete_fib)
        
        # Call the function
        result = ensure_fibonacci_levels(self.current_price)
        
        # Check the results
        self.assertEqual(result["high"], 60000.0)
        self.assertEqual(result["low"], 40000.0)
        self.assertIn("fib_0.618", result)
        self.assertIn("fib_0.5", result)
        
        # Verify the Redis calls for setting the complete levels
        self.redis_mock.set.assert_called_once_with("fibonacci_levels", json.dumps(result))
    
    def test_ensure_fibonacci_levels_no_data(self):
        """Test ensure_fibonacci_levels when no levels exist"""
        # Mock Redis to return no Fibonacci levels
        self.redis_mock.get.return_value = None
        
        # Call the function
        result = ensure_fibonacci_levels(self.current_price)
        
        # Check the results
        self.assertEqual(result["high"], self.current_price * 1.2)
        self.assertEqual(result["low"], self.current_price * 0.8)
        self.assertIn("fib_0.618", result)
        
        # Verify the Redis calls for setting the new levels
        self.redis_mock.set.assert_called_once_with("fibonacci_levels", json.dumps(result))
    
    def test_create_fibonacci_levels(self):
        """Test create_fibonacci_levels function"""
        high = 60000.0
        low = 40000.0
        
        # Call the function
        result = create_fibonacci_levels(high, low)
        
        # Check the results
        self.assertEqual(result["high"], high)
        self.assertEqual(result["low"], low)
        self.assertEqual(result["fib_0"], low)
        self.assertEqual(result["fib_1"], high)
        self.assertEqual(result["fib_0.5"], (high + low) / 2)
        self.assertEqual(result["fib_0.618"], low + 0.618 * (high - low))
        self.assertIn("last_update", result)

if __name__ == "__main__":
    logger.info("Starting fallback helper tests...")
    unittest.main(verbosity=2) 