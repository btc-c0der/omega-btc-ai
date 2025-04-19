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
Tests for the _get_redis_data method in the ReggaeDashboardServer class.
"""

import json
import unittest
from unittest.mock import Mock, patch
import asyncio
from pathlib import Path
import sys

# Add parent directory to the Python path
parent_dir = Path(__file__).parent.parent.parent
sys.path.append(str(parent_dir))

from omega_ai.visualizer.backend.reggae_dashboard_server import ReggaeDashboardServer


class TestGetRedisData(unittest.TestCase):
    """Test cases for the _get_redis_data method."""

    def setUp(self):
        """Set up mock objects for testing."""
        self.server = ReggaeDashboardServer()
        # Mock the redis client
        self.server.redis_client = Mock()

    async def _async_test_with_data(self):
        """Test _get_redis_data with data in the first Redis key."""
        # Configure redis_client.get to return mock data for 'long_trader_position'
        mock_data = {
            "entry_price": 85000,
            "size": 0.01,
            "leverage": 10
        }
        self.server.redis_client.get.side_effect = lambda key: json.dumps(mock_data) if key == 'long_trader_position' else None
        
        # Call the method
        result = await self.server._get_redis_data('long_position')
        
        # Check if correct data was returned
        self.assertEqual(result.get('entry_price'), 85000)
        self.assertEqual(result.get('size'), 0.01)
        self.assertEqual(result.get('leverage'), 10)
        self.assertTrue('_source' in result)
        self.assertEqual(result.get('_source'), 'redis:long_trader_position')
        
    async def _async_test_with_fallback(self):
        """Test _get_redis_data falling back to mock data."""
        # Configure redis_client.get to always return None
        self.server.redis_client.get.return_value = None
        
        # Call the method
        result = await self.server._get_redis_data('long_position')
        
        # Check if mock data was returned
        self.assertTrue('entry_price' in result)
        self.assertTrue('size' in result)
        self.assertTrue('leverage' in result)
        self.assertTrue('_source' in result)
        self.assertEqual(result.get('_source'), 'mock')
        
    async def _async_test_with_non_json(self):
        """Test _get_redis_data with non-JSON data."""
        # Configure redis_client.get to return a number
        self.server.redis_client.get.side_effect = lambda key: "42.5" if key == 'btc_price' else None
        
        # Call the method
        result = await self.server._get_redis_data('btc_price')
        
        # Check if number was returned
        self.assertEqual(result, 42.5)
        
    async def _async_test_with_exception(self):
        """Test _get_redis_data when an exception occurs."""
        # Configure redis_client.get to raise an exception
        self.server.redis_client.get.side_effect = Exception("Redis connection error")
        
        # Call the method
        result = await self.server._get_redis_data('long_position')
        
        # Check if mock data was returned with error info
        self.assertTrue('_source' in result)
        self.assertEqual(result.get('_source'), 'mock:error')
        self.assertTrue('_error' in result)
        
    def test_get_redis_data_with_data(self):
        """Run the async test for successful Redis data retrieval."""
        asyncio.run(self._async_test_with_data())
        
    def test_get_redis_data_with_fallback(self):
        """Run the async test for fallback to mock data."""
        asyncio.run(self._async_test_with_fallback())
        
    def test_get_redis_data_with_non_json(self):
        """Run the async test for non-JSON data."""
        asyncio.run(self._async_test_with_non_json())
        
    def test_get_redis_data_with_exception(self):
        """Run the async test for exception handling."""
        asyncio.run(self._async_test_with_exception())


if __name__ == '__main__':
    unittest.main() 