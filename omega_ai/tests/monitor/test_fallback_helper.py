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


import unittest
import json
import os
import sys
import redis
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timedelta

# Add the project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from omega_ai.monitor.fallback_helper import (
    validate_data, 
    ensure_trend_data, 
    ensure_fibonacci_levels,
    create_fibonacci_levels,
    get_redis_data,
    store_warning_in_redis,
    fibonacci_retry,
    CosmicAlignmentError,
    FibonacciViolation
)

class TestFallbackHelper(unittest.TestCase):
    """Test the fallback helper module functions."""

    def test_validate_data(self):
        """Test data validation function with various inputs."""
        # Test valid price
        valid, message = validate_data('price', 50000)
        self.assertTrue(valid)
        self.assertEqual(message, "")
        
        # Test invalid price (too high)
        valid, message = validate_data('price', 2000000)
        self.assertFalse(valid)
        self.assertEqual(message, "Unrealistic BTC price")
        
        # Test string input that should convert to valid price
        valid, message = validate_data('price', "35000")
        self.assertTrue(valid)
        self.assertEqual(message, "")
        
        # Test invalid input type
        valid, message = validate_data('price', "not_a_number")
        self.assertFalse(valid)
        self.assertTrue("Invalid price format" in message)
        
        # Test unknown data type
        valid, message = validate_data('unknown_type', 123)
        self.assertTrue(valid)
        self.assertEqual(message, "")

    @patch('omega_ai.monitor.fallback_helper.get_redis_data')
    def test_ensure_trend_data_primary(self, mock_get_redis_data):
        """Test ensuring trend data when primary source is available."""
        # Mock Redis to return trend data
        mock_get_redis_data.return_value = "Bullish"
        
        # Call the function
        result = ensure_trend_data('15min')
        
        # Verify the result
        self.assertEqual(result["data"], "Bullish")
        self.assertEqual(result["source"], "primary")
        self.assertEqual(result["timeframe"], "15min")
        
        # Verify Redis was called with the correct key
        mock_get_redis_data.assert_called_once_with("btc_trend_15min")

    @patch('omega_ai.monitor.fallback_helper.get_redis_data')
    def test_ensure_trend_data_fallback_timeframe(self, mock_get_redis_data):
        """Test ensuring trend data with fallback to another timeframe."""
        # Mock Redis to return None for primary, but data for fallback
        mock_get_redis_data.side_effect = lambda key: None if key == "btc_trend_15min" else "Bearish"
        
        # Call the function
        result = ensure_trend_data('15min')
        
        # Verify the result indicates fallback was used
        self.assertEqual(result["data"], "Bearish")
        self.assertEqual(result["source"], "fallback_timeframe")
        
        # At least two calls to Redis should have been made
        self.assertTrue(mock_get_redis_data.call_count >= 2)

    @patch('omega_ai.monitor.fallback_helper.get_redis_data')
    def test_ensure_trend_data_candle_inference(self, mock_get_redis_data):
        """Test ensuring trend data with fallback to candle inference."""
        # Mock Redis to return None for trend data but candle data available
        def side_effect(key):
            if key == "btc_trend_15min":
                return None
            elif key == "btc_candle_15min":
                return {'o': 50000, 'c': 52000, 'h': 52500, 'l': 49500, 'v': 100}
            elif key.startswith("btc_trend_"):
                return None
            return None
            
        mock_get_redis_data.side_effect = side_effect
        
        # Call the function
        result = ensure_trend_data('15min')
        
        # Verify the result indicates candle inference was used
        self.assertEqual(result["data"], "Bullish")
        self.assertEqual(result["source"], "candle_inference")
        self.assertEqual(result["timeframe"], "15min")

    @patch('omega_ai.monitor.fallback_helper.get_redis_data')
    def test_ensure_trend_data_default(self, mock_get_redis_data):
        """Test ensuring trend data defaulting to stable when no data available."""
        # Mock Redis to return None for all keys
        mock_get_redis_data.return_value = None
        
        # Call the function
        result = ensure_trend_data('15min')
        
        # Verify the result defaults to stable
        self.assertEqual(result["data"], "Stable")
        self.assertEqual(result["source"], "default")
        self.assertEqual(result["timeframe"], "15min")

    @patch('omega_ai.monitor.fallback_helper.get_redis_data')
    def test_ensure_fibonacci_levels_primary(self, mock_get_redis_data):
        """Test ensuring Fibonacci levels when valid levels are available."""
        # Create sample Fibonacci levels
        now = datetime.now()
        fib_levels = {
            'base_price': 50000,
            'direction': 'up',
            'levels': {
                '0': 50000,
                '0.236': 47640,
                '0.382': 46180,
                '0.5': 45000,
                '0.618': 43820,
                '0.786': 42140,
                '1.0': 40000,
                '1.618': 35280,
                '2.618': 27280
            },
            'swing_high': 50000,
            'swing_low': 40000,
            'timestamp': now.isoformat()
        }
        
        # Mock Redis to return Fibonacci levels
        mock_get_redis_data.return_value = fib_levels
        
        # Call the function
        result = ensure_fibonacci_levels()
        
        # Verify the result
        self.assertEqual(result["data"], fib_levels)
        self.assertEqual(result["source"], "primary")
        self.assertEqual(result["timestamp"], now.isoformat())

    @patch('omega_ai.monitor.fallback_helper.get_redis_data')
    @patch('omega_ai.monitor.fallback_helper.redis_conn')
    def test_ensure_fibonacci_levels_generated(self, mock_redis_conn, mock_get_redis_data):
        """Test ensuring Fibonacci levels when levels need to be generated."""
        # Mock Redis to return None for Fibonacci levels but price available
        mock_get_redis_data.side_effect = lambda key: 50000 if key == "last_btc_price" else None
        
        # Call the function
        result = ensure_fibonacci_levels()
        
        # Verify the result
        self.assertEqual(result["source"], "generated")
        self.assertIsNotNone(result["data"])
        self.assertIn("levels", result["data"])
        self.assertEqual(result["data"]["base_price"], 50000)
        
        # Verify Redis was called to store the new levels
        self.assertTrue(mock_redis_conn.set.called)

    def test_create_fibonacci_levels(self):
        """Test creation of Fibonacci levels with different inputs."""
        # Test with uptrend
        levels_up = create_fibonacci_levels(50000, direction="up")
        self.assertEqual(levels_up["base_price"], 50000)
        self.assertEqual(levels_up["direction"], "up")
        self.assertEqual(levels_up["swing_high"], 50000)
        self.assertEqual(levels_up["swing_low"], 45000)  # 10% below
        
        # Verify specific Fibonacci level calculations
        self.assertEqual(levels_up["levels"]["0"], 50000)  # High
        self.assertEqual(levels_up["levels"]["1.0"], 45000)  # Low
        
        # Test with downtrend
        levels_down = create_fibonacci_levels(50000, direction="down")
        self.assertEqual(levels_down["base_price"], 50000)
        self.assertEqual(levels_down["direction"], "down")
        self.assertAlmostEqual(levels_down["swing_high"], 55000, places=2)  # 10% above
        self.assertEqual(levels_down["swing_low"], 50000)

    @patch('omega_ai.monitor.fallback_helper.redis_conn')
    def test_store_warning_in_redis(self, mock_redis_conn):
        """Test storing warnings in Redis."""
        # Call the function
        store_warning_in_redis("TEST_WARNING", "This is a test warning")
        
        # Verify Redis calls
        self.assertTrue(mock_redis_conn.set.called)
        self.assertTrue(mock_redis_conn.lpush.called)
        self.assertTrue(mock_redis_conn.ltrim.called)
        
        # Verify the warning was stored with correct type and message
        call_args = mock_redis_conn.set.call_args[0]
        self.assertTrue(call_args[0].startswith("warning:"))
        warning_data = json.loads(call_args[1])
        self.assertEqual(warning_data["type"], "TEST_WARNING")
        self.assertEqual(warning_data["message"], "This is a test warning")
        self.assertEqual(warning_data["source"], "fallback_helper")

    @patch('omega_ai.monitor.fallback_helper.redis.Redis')
    @patch('time.sleep')
    def test_fibonacci_retry_decorator(self, mock_sleep, mock_redis):
        """Test the Fibonacci retry decorator."""
        # Mock Redis to raise exception on first call, then succeed
        redis_instance = MagicMock()
        redis_instance.get.side_effect = [
            redis.ConnectionError("Connection refused"),
            "success"
        ]
        mock_redis.return_value = redis_instance
        
        # Create a test function with the decorator
        @fibonacci_retry(max_attempts=3)
        def test_function():
            return redis_instance.get("test_key")
        
        # Call the function
        result = test_function()
        
        # Verify the function retried and eventually succeeded
        self.assertEqual(result, "success")
        self.assertEqual(redis_instance.get.call_count, 2)
        mock_sleep.assert_called_once_with(1)  # First retry delay is 1 second

    @patch('omega_ai.monitor.fallback_helper.redis.Redis')
    @patch('time.sleep')
    def test_fibonacci_retry_max_attempts(self, mock_sleep, mock_redis):
        """Test the Fibonacci retry decorator when max attempts is reached."""
        # Mock Redis to always raise an exception
        redis_instance = MagicMock()
        redis_instance.get.side_effect = redis.ConnectionError("Connection refused")
        mock_redis.return_value = redis_instance
        
        # Create a test function with the decorator
        @fibonacci_retry(max_attempts=3)
        def test_function():
            return redis_instance.get("test_key")
        
        # Call the function and expect an exception
        with self.assertRaises(redis.ConnectionError):
            test_function()
        
        # Verify the function retried the correct number of times
        self.assertEqual(redis_instance.get.call_count, 3)
        # Verify it slept with Fibonacci sequence
        mock_sleep.assert_has_calls([call(1), call(1)])

if __name__ == '__main__':
    unittest.main() 