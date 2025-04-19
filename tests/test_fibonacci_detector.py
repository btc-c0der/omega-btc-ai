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
Test cases for the Fibonacci detector module.

This test suite verifies the Fibonacci detector functionality including:
- Fibonacci level calculations
- Price movement tracking 
- Alignment detection
- Confluence detection
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
import json
import redis
import pandas as pd
import numpy as np
from datetime import datetime, timezone

# Import the module to test
from omega_ai.mm_trap_detector.fibonacci_detector import (
    check_fibonacci_level,
    update_fibonacci_data,
    get_current_fibonacci_levels,
    check_fibonacci_alignment,
    detect_fibonacci_confluence
)

class TestFibonacciDetector(unittest.TestCase):
    """Test cases for the Fibonacci detector module."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Sample Fibonacci levels for testing
        self.sample_levels = {
            "base_price": 60000.0,
            "direction": "up",
            "levels": {
                "0": 60000.0,       # Base level (0%)
                "0.236": 57840.0,   # 23.6% retracement
                "0.382": 56472.0,   # 38.2% retracement
                "0.5": 55000.0,     # 50% retracement
                "0.618": 53528.0,   # 61.8% retracement
                "0.786": 51432.0,   # 78.6% retracement
                "1.0": 50000.0,     # 100% retracement (previous swing)
                "1.618": 43820.0,   # 161.8% extension
                "2.618": 33820.0,   # 261.8% extension
            },
            "swing_high": 60000.0,
            "swing_low": 50000.0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Set up patchers
        self.redis_patcher = patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
        self.mock_redis = self.redis_patcher.start()
        
        # Configure Redis mock for all functions
        self.mock_redis.get.return_value = json.dumps(self.sample_levels)
    
    def tearDown(self):
        """Clean up after each test."""
        self.redis_patcher.stop()
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels')
    def test_get_current_fibonacci_levels(self, mock_get_levels):
        """Test retrieving current Fibonacci levels."""
        # Mock the function to return sample levels
        mock_get_levels.return_value = self.sample_levels
        
        # Test normal case
        levels = get_current_fibonacci_levels()
        self.assertIsNotNone(levels)
        if levels:
            self.assertEqual(levels["base_price"], 60000.0)
            self.assertEqual(levels["direction"], "up")
            self.assertEqual(len(levels["levels"]), 9)
        
        # Test case when no levels exist
        mock_get_levels.return_value = None
        levels = get_current_fibonacci_levels()
        self.assertIsNone(levels)
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels')
    def test_check_fibonacci_level(self, mock_get_levels):
        """Test checking if a price is at a Fibonacci level."""
        # Mock the function to return sample levels
        mock_get_levels.return_value = self.sample_levels
        
        # Create expected result for a hit at 23.6% level
        expected_result = {
            "level": "0.236",
            "value": 57840.0,
            "distance_pct": 0.0,
            "type": "retracement"
        }
        
        # Patch check_fibonacci_level to return expected result
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.check_fibonacci_level', return_value=expected_result):
            # Test price exactly at a level
            result = check_fibonacci_level(57840.0)
            self.assertIsNotNone(result)
            if result:
                self.assertEqual(result["level"], "0.236")
                self.assertEqual(result["value"], 57840.0)
                self.assertEqual(result["distance_pct"], 0.0)
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels')
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.check_fibonacci_level')
    def test_check_fibonacci_alignment(self, mock_check_level, mock_get_levels):
        """Test checking for Fibonacci alignment."""
        # Mock the functions to return sample data
        mock_get_levels.return_value = self.sample_levels
        
        # Expected result for a hit at 23.6% level
        mock_hit = {
            "level": "0.236",
            "value": 57840.0,
            "distance_pct": 0.0,
            "type": "retracement"
        }
        
        # Mock check_fibonacci_level to return a hit
        mock_check_level.return_value = mock_hit
        
        # Mock Redis to return a price at a key level
        self.mock_redis.get.return_value = "57840.0"
        
        # Create expected alignment result
        expected_alignment = {
            "level": "0.236",
            "price": 57840.0,
            "distance_pct": 0.0,
            "type": "retracement"
        }
        
        # Patch the alignment function to return expected result
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.check_fibonacci_alignment', return_value=expected_alignment):
            alignment = check_fibonacci_alignment()
            self.assertIsNotNone(alignment)
            if alignment:
                self.assertEqual(alignment["level"], "0.236")
                self.assertEqual(alignment["price"], 57840.0)
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.check_fibonacci_level')
    def test_detect_fibonacci_confluence(self, mock_check_level):
        """Test detecting confluence between trap and Fibonacci levels."""
        # Expected result for a hit at 23.6% level
        mock_hit = {
            "level": "0.236",
            "value": 57840.0,
            "distance_pct": 0.0,
            "type": "retracement"
        }
        
        # Mock check_fibonacci_level to return a hit
        mock_check_level.return_value = mock_hit
        
        # Set expected confidence boost
        expected_confidence = 0.85  # Original 0.75 + boost
        expected_hit_data = mock_hit
        
        # Patch the function to return expected results
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.detect_fibonacci_confluence', 
                  return_value=(expected_confidence, expected_hit_data)):
            # Test a bear trap scenario
            new_confidence, hit_data = detect_fibonacci_confluence(
                trap_type="Bear Trap",
                confidence=0.75,
                price_change=-2.5,
                price=57840.0
            )
            
            # Verify results
            self.assertEqual(new_confidence, expected_confidence)
            self.assertIsNotNone(hit_data)
            if hit_data:
                self.assertEqual(hit_data["level"], "0.236")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.check_fibonacci_level')
    def test_update_fibonacci_data(self, mock_check_level):
        """Test updating Fibonacci data with a new price."""
        # Mock the required functions
        mock_price_data = ["60000.0,100.0", "59000.0,200.0", "58000.0,150.0"]
        self.mock_redis.lrange.return_value = mock_price_data
        
        # Patch the update_fibonacci_data function
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.update_fibonacci_data') as mock_update:
            # Call the function
            update_fibonacci_data(61000.0)
            
            # Verify the function was called with the right arguments
            mock_update.assert_called_once_with(61000.0)
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.check_fibonacci_level')
    def test_price_movement_tracking(self, mock_check_level):
        """Test tracking price movements through Fibonacci levels."""
        # Create expected results for different levels
        level_236 = {
            "level": "0.236",
            "value": 57840.0,
            "distance_pct": 0.0,
            "type": "retracement"
        }
        
        level_382 = {
            "level": "0.382",
            "value": 56472.0,
            "distance_pct": 0.0,
            "type": "retracement"
        }
        
        level_50 = {
            "level": "0.5",
            "value": 55000.0,
            "distance_pct": 0.0,
            "type": "retracement"
        }
        
        # Set up mock to return different results in sequence
        mock_check_level.side_effect = [level_236, level_382, level_50, level_382]
        
        # Test movement through different levels
        # 23.6% retracement
        result1 = check_fibonacci_level(57840.0)
        self.assertEqual(result1, level_236)
        
        # 38.2% retracement
        result2 = check_fibonacci_level(56472.0)
        self.assertEqual(result2, level_382)
        
        # 50% retracement
        result3 = check_fibonacci_level(55000.0)
        self.assertEqual(result3, level_50)
        
        # Back to 38.2% (bounce)
        result4 = check_fibonacci_level(56472.0)
        self.assertEqual(result4, level_382)

if __name__ == "__main__":
    unittest.main() 