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
Test the Fibonacci level handling with various data formats from Redis.
"""

import unittest
import json
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.db_manager.database import format_percentage
from omega_ai.mm_trap_detector.fibonacci_detector import get_current_fibonacci_levels, check_fibonacci_alignment


class TestFibonacciHandling(unittest.TestCase):
    """Test the Fibonacci level handling with various data formats."""

    def setUp(self):
        """Set up the test case."""
        self.mock_redis = MagicMock()
        self.mock_redis_patcher = patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn', self.mock_redis)
        self.mock_redis_patcher.start()
        
        # Test data
        self.fibonacci_levels = {
            "0": 30000.0,
            "0.236": 31000.0,
            "0.382": 32000.0,
            "0.5": 33000.0,
            "0.618": 34000.0,
            "0.786": 35000.0,
            "1.0": 36000.0,
            "1.618": 37000.0,
            "2.618": 38000.0
        }
        
        # Current price near a Fibonacci level
        self.current_price = 33100.0  # Near 0.5 level

    def tearDown(self):
        """Clean up after the test."""
        self.mock_redis_patcher.stop()

    def test_format_percentage_handles_none(self):
        """Test that format_percentage handles None values."""
        # Test with None
        formatted = format_percentage(None)
        self.assertEqual(formatted, "0.00%")
        
        # Test with actual percentage
        formatted = format_percentage(12.345)
        self.assertEqual(formatted, "12.35%")

    def test_format_percentage_handles_string(self):
        """Test that format_percentage handles string values."""
        # Test with string
        formatted = format_percentage("12.345")
        self.assertEqual(formatted, "12.35%")
        
        # Test with invalid string
        formatted = format_percentage("not a number")
        self.assertEqual(formatted, "0.00%")

    def test_get_current_fibonacci_levels_handles_cached_data(self):
        """Test that get_current_fibonacci_levels handles cached data from Redis."""
        # Mock Redis to return cached Fibonacci levels
        self.mock_redis.get.return_value = json.dumps(self.fibonacci_levels)
        
        # Get Fibonacci levels
        levels = get_current_fibonacci_levels()
        
        # Verify levels match mock data
        self.assertEqual(levels, self.fibonacci_levels)
        
        # Verify Redis was called with correct key
        self.mock_redis.get.assert_called_with("fibonacci_levels")

    def test_get_current_fibonacci_levels_handles_invalid_json(self):
        """Test that get_current_fibonacci_levels handles invalid JSON."""
        # Mock Redis to return invalid JSON
        self.mock_redis.get.return_value = "not valid json"
        
        # Patch fibonacci_detector.generate_fibonacci_levels to return known data
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.fibonacci_detector.generate_fibonacci_levels') as mock_generate:
            mock_generate.return_value = self.fibonacci_levels
            
            # Get Fibonacci levels
            levels = get_current_fibonacci_levels()
            
            # Verify fallback to generate_fibonacci_levels
            self.assertEqual(levels, self.fibonacci_levels)
            mock_generate.assert_called_once()

    def test_get_current_fibonacci_levels_handles_none(self):
        """Test that get_current_fibonacci_levels handles None from Redis."""
        # Mock Redis to return None
        self.mock_redis.get.return_value = None
        
        # Patch fibonacci_detector.generate_fibonacci_levels to return known data
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.fibonacci_detector.generate_fibonacci_levels') as mock_generate:
            mock_generate.return_value = self.fibonacci_levels
            
            # Get Fibonacci levels
            levels = get_current_fibonacci_levels()
            
            # Verify fallback to generate_fibonacci_levels
            self.assertEqual(levels, self.fibonacci_levels)
            mock_generate.assert_called_once()

    def test_get_current_fibonacci_levels_handles_empty_dict(self):
        """Test that get_current_fibonacci_levels handles empty dict result."""
        # Mock Redis to return None
        self.mock_redis.get.return_value = None
        
        # Patch fibonacci_detector.generate_fibonacci_levels to return None
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.fibonacci_detector.generate_fibonacci_levels') as mock_generate:
            mock_generate.return_value = None
            
            # Get Fibonacci levels
            levels = get_current_fibonacci_levels()
            
            # Verify empty dict is returned
            self.assertEqual(levels, {})
            mock_generate.assert_called_once()

    def test_check_fibonacci_alignment_near_level(self):
        """Test that check_fibonacci_alignment finds alignment with a nearby level."""
        # Mock Redis to return current price and Fibonacci levels
        self.mock_redis.get.side_effect = lambda key: {
            "last_btc_price": str(self.current_price),
            "fibonacci_levels": json.dumps(self.fibonacci_levels)
        }.get(key)
        
        # Check alignment
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels') as mock_get_levels:
            mock_get_levels.return_value = self.fibonacci_levels
            alignment = check_fibonacci_alignment()
            
            # Verify alignment
            self.assertIsNotNone(alignment)
            if alignment is not None:  # Add null check to avoid linting errors
                self.assertEqual(alignment["level"], "0.5")
                self.assertEqual(alignment["price"], 33000.0)
                self.assertLess(alignment["distance_pct"], 0.5)  # Should be about 0.3%
                self.assertGreater(alignment["confidence"], 0.9)  # Should be high confidence

    def test_check_fibonacci_alignment_handles_string_price(self):
        """Test that check_fibonacci_alignment handles string price value."""
        # Mock Redis to return string current price and Fibonacci levels
        self.mock_redis.get.side_effect = lambda key: {
            "last_btc_price": "33100.0",  # String price
            "fibonacci_levels": json.dumps(self.fibonacci_levels)
        }.get(key)
        
        # Check alignment
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels') as mock_get_levels:
            mock_get_levels.return_value = self.fibonacci_levels
            alignment = check_fibonacci_alignment()
            
            # Verify alignment
            self.assertIsNotNone(alignment)
            if alignment is not None:  # Add null check to avoid linting errors
                self.assertEqual(alignment["level"], "0.5")
                self.assertEqual(alignment["price"], 33000.0)

    def test_check_fibonacci_alignment_handles_missing_price(self):
        """Test that check_fibonacci_alignment handles missing price."""
        # Mock Redis to return None for current price
        self.mock_redis.get.side_effect = lambda key: {
            "last_btc_price": None,
            "fibonacci_levels": json.dumps(self.fibonacci_levels)
        }.get(key)
        
        # Check alignment
        alignment = check_fibonacci_alignment()
        
        # Verify no alignment found
        self.assertIsNone(alignment)

    def test_fibonacci_levels_with_string_values(self):
        """Test handling Fibonacci levels with string values to prevent subtract error."""
        # Create Fibonacci levels with string values
        string_fibonacci_levels = {
            "0": 30000.0,
            "0.236": "31000.0",  # String value
            "0.382": 32000.0,
            "0.5": "33000.0",    # String value
            "0.618": 34000.0,
            "0.786": 35000.0,
            "1.0": "36000.0",    # String value
            "1.618": 37000.0,
            "2.618": "invalid"   # Invalid string
        }
        
        # Mock Redis to return current price and string Fibonacci levels
        self.mock_redis.get.side_effect = lambda key: {
            "last_btc_price": str(self.current_price),
            "fibonacci_levels": json.dumps(string_fibonacci_levels)
        }.get(key)
        
        # Check alignment
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels') as mock_get_levels:
            mock_get_levels.return_value = string_fibonacci_levels
            alignment = check_fibonacci_alignment()
            
            # Verify alignment
            self.assertIsNotNone(alignment)
            if alignment is not None:  # Add null check to avoid linting errors
                # Should find 0.5 level despite it being a string
                self.assertEqual(alignment["level"], "0.5")
                # Should convert string price to float
                self.assertEqual(alignment["price"], 33000.0)
                self.assertLess(alignment["distance_pct"], 0.5)


if __name__ == "__main__":
    unittest.main() 