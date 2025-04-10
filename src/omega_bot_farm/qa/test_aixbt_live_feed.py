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
Unit tests for AIXBT Live Feed V1
================================

This module contains unit tests for the AIXBT Live Feed functionality.
Tests include correlation calculation, message handling, and Redis operations.
"""

import sys
import os
import json
import unittest
import asyncio
from unittest import mock
from datetime import datetime, timezone
import numpy as np

# Add parent directory to path to import the module under test
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module to test
from aixbt_live_feed_v1 import (
    calculate_correlation, 
    price_movement_indicator,
    virgil_abloh_print,
    AixbtLiveFeedV1
)

class TestAixbtCorrelationCalculation(unittest.TestCase):
    """Test the correlation calculation between AIXBT and BTC."""
    
    def test_correlation_calculation_positive(self):
        """Test correlation calculation with positively correlated data."""
        aixbt_prices = [100, 102, 105, 107, 110]
        btc_prices = [40000, 40500, 41000, 41200, 42000]
        
        correlation = calculate_correlation(aixbt_prices, btc_prices)
        
        # Should be very close to 1.0 (strong positive correlation)
        self.assertGreater(correlation, 0.95)
        self.assertLessEqual(correlation, 1.0)
    
    def test_correlation_calculation_negative(self):
        """Test correlation calculation with negatively correlated data."""
        aixbt_prices = [110, 108, 105, 103, 100]
        btc_prices = [40000, 40500, 41000, 41200, 42000]
        
        correlation = calculate_correlation(aixbt_prices, btc_prices)
        
        # Should be very close to -1.0 (strong negative correlation)
        self.assertLess(correlation, -0.95)
        self.assertGreaterEqual(correlation, -1.0)
    
    def test_correlation_calculation_no_correlation(self):
        """Test correlation calculation with uncorrelated data."""
        aixbt_prices = [100, 90, 110, 95, 105]
        btc_prices = [40000, 40500, 41000, 41200, 42000]
        
        correlation = calculate_correlation(aixbt_prices, btc_prices)
        
        # Should be close to 0 (weak or no correlation)
        self.assertGreater(correlation, -0.5)
        self.assertLess(correlation, 0.5)
    
    def test_correlation_insufficient_data(self):
        """Test correlation calculation with insufficient data points."""
        aixbt_prices = [100, 105]
        btc_prices = [40000, 40500]
        
        correlation = calculate_correlation(aixbt_prices, btc_prices)
        
        # Should return 0 when insufficient data
        self.assertEqual(correlation, 0.0)
    
    def test_correlation_error_handling(self):
        """Test correlation calculation error handling."""
        # Invalid inputs should return 0.0
        aixbt_prices = None
        btc_prices = [40000, 40500, 41000]
        
        with self.assertRaises(TypeError):
            calculate_correlation(aixbt_prices, btc_prices)

class TestPriceMovementIndicator(unittest.TestCase):
    """Test the price movement indicator function."""
    
    def test_price_increase(self):
        """Test indicator for price increase."""
        old_price = 100
        new_price = 105
        
        indicator = price_movement_indicator(old_price, new_price)
        
        # Should contain a green up triangle
        self.assertIn("▲", indicator)
    
    def test_price_decrease(self):
        """Test indicator for price decrease."""
        old_price = 105
        new_price = 100
        
        indicator = price_movement_indicator(old_price, new_price)
        
        # Should contain a red down triangle
        self.assertIn("▼", indicator)
    
    def test_price_unchanged(self):
        """Test indicator for unchanged price."""
        old_price = 100
        new_price = 100
        
        indicator = price_movement_indicator(old_price, new_price)
        
        # Should contain a blue square
        self.assertIn("■", indicator)

class TestAixbtLiveFeedV1(unittest.IsolatedAsyncioTestCase):
    """Test the AixbtLiveFeedV1 class functionality."""
    
    async def asyncSetUp(self):
        """Set up the test environment."""
        # Create a mock Redis client
        self.redis_patcher = mock.patch('redis.Redis')
        self.mock_redis = self.redis_patcher.start()
        
        # Create a mock instance for the Redis client
        self.mock_redis_instance = mock.MagicMock()
        self.mock_redis.return_value = self.mock_redis_instance
        
        # Create an instance of AixbtLiveFeedV1 with the mocked Redis
        self.feed = AixbtLiveFeedV1()
        
        # Replace the actual Redis client with our mock
        if not hasattr(self.feed, 'redis_client'):
            self.feed.redis_client = self.mock_redis_instance
        
        # Mock some initial data
        self.feed.aixbt_prices = [100, 101, 102, 103, 104]
        self.feed.btc_prices = [40000, 40100, 40200, 40300, 40400]
        self.feed.last_aixbt_price = 104
        self.feed.last_btc_price = 40400
    
    async def asyncTearDown(self):
        """Clean up resources after tests."""
        self.redis_patcher.stop()
    
    async def test_handle_aixbt_message(self):
        """Test handling of AIXBT websocket messages."""
        # Create a sample message
        message = json.dumps({
            'p': '105.00000000',
            'q': '10.00000000',
            't': 12345,
            's': 'AIXBTUSDT',
            'T': 1655555555555,
            'a': 67890
        })
        
        # Mock the Redis helper methods
        self.feed._redis_set = mock.AsyncMock(return_value=True)
        self.feed._redis_lpush = mock.AsyncMock(return_value=True)
        
        # Process the message
        await self.feed._handle_aixbt_message(message)
        
        # Verify the price was updated
        self.assertEqual(self.feed.last_aixbt_price, 105.0)
        self.assertEqual(len(self.feed.aixbt_prices), 6)  # Original 5 + new one
        self.assertEqual(self.feed.aixbt_prices[-1], 105.0)
        
        # Verify Redis operations were called via our new helper methods
        self.feed._redis_set.assert_any_call("last_aixbt_price", "105.0")
        self.feed._redis_set.assert_any_call("last_aixbt_update_time", mock.ANY)
        self.feed._redis_lpush.assert_called_with("aixbt_movement_history", mock.ANY, trim=True)
    
    async def test_handle_btc_message(self):
        """Test handling of BTC websocket messages."""
        # Create a sample message
        message = json.dumps({
            'p': '40500.00000000',
            'q': '0.05000000',
            't': 12345,
            's': 'BTCUSDT',
            'T': 1655555555555,
            'a': 67890
        })
        
        # Mock the Redis helper methods
        self.feed._redis_set = mock.AsyncMock(return_value=True)
        
        # Process the message
        await self.feed._handle_btc_message(message)
        
        # Verify the price was updated
        self.assertEqual(self.feed.last_btc_price, 40500.0)
        self.assertEqual(len(self.feed.btc_prices), 6)  # Original 5 + new one
        self.assertEqual(self.feed.btc_prices[-1], 40500.0)
        
        # Verify Redis operations were called via our new helper methods
        self.feed._redis_set.assert_any_call("last_btc_price", "40500.0")
        self.feed._redis_set.assert_any_call("last_btc_update_time", mock.ANY)

if __name__ == '__main__':
    unittest.main() 