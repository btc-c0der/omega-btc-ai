
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
MIT License

Copyright (c) 2024 OMEGA BTC AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import unittest
import json
import datetime
import time
from unittest.mock import patch, MagicMock
import redis
import sys
import os

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the module to test
from omega_ai.mm_trap_detector.redis_time_series import (
    store_time_series_data,
    compress_historical_data,
    get_time_series_data,
    TimeSeriesGranularity,
    cleanup_old_data
)

class TestRedisTimeSeries(unittest.TestCase):
    """Tests for the Redis time series optimization"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Redis connection
        self.redis_mock = MagicMock()
        self.redis_patcher = patch('omega_ai.mm_trap_detector.redis_time_series.redis_conn', self.redis_mock)
        self.redis_patcher.start()

        # Sample data
        self.current_time = datetime.datetime(2024, 5, 1, 14, 30, 0, tzinfo=datetime.UTC)
        self.sample_price_data = {
            "timestamp": self.current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "price": 85000.0,
            "change_pct": 0.05,
            "regime": "Moderate Volatility Bullish"
        }

    def tearDown(self):
        """Tear down test fixtures"""
        self.redis_patcher.stop()

    def test_store_time_series_minute_data(self):
        """Test storing minute-level time series data"""
        # Act
        store_time_series_data(
            "price_history", 
            self.sample_price_data, 
            self.current_time,
            granularity=TimeSeriesGranularity.MINUTE
        )

        # Assert
        expected_key = f"sim_price_history:{self.current_time.date().isoformat()}:minute"
        self.redis_mock.rpush.assert_called_with(expected_key, json.dumps(self.sample_price_data))
        self.redis_mock.expire.assert_called_with(expected_key, 86400 * 7)  # 7 days retention

    def test_store_time_series_hourly_data(self):
        """Test storing hourly time series data"""
        # Act
        store_time_series_data(
            "price_history", 
            self.sample_price_data, 
            self.current_time,
            granularity=TimeSeriesGranularity.HOURLY
        )

        # Assert
        expected_key = f"sim_price_history:{self.current_time.date().isoformat()}:hourly"
        self.redis_mock.rpush.assert_called_with(expected_key, json.dumps(self.sample_price_data))
        self.redis_mock.expire.assert_called_with(expected_key, 86400 * 30)  # 30 days retention

    def test_store_time_series_daily_data(self):
        """Test storing daily time series data"""
        # Act
        store_time_series_data(
            "price_history", 
            self.sample_price_data, 
            self.current_time,
            granularity=TimeSeriesGranularity.DAILY
        )

        # Assert
        expected_key = f"sim_price_history:{self.current_time.date().isoformat()}:daily"
        self.redis_mock.rpush.assert_called_with(expected_key, json.dumps(self.sample_price_data))
        self.redis_mock.expire.assert_called_with(expected_key, 86400 * 90)  # 90 days retention

    def test_compress_historical_data(self):
        """Test compressing historical minute data to hourly"""
        # Arrange
        minute_key = f"sim_price_history:{self.current_time.date().isoformat()}:minute"
        hourly_key = f"sim_price_history:{self.current_time.date().isoformat()}:hourly"
        
        # Create mock minute data (60 entries for 1 hour)
        minute_data = []
        base_time = datetime.datetime(2024, 5, 1, 14, 0, 0, tzinfo=datetime.UTC)
        for i in range(60):
            entry_time = base_time + datetime.timedelta(minutes=i)
            minute_data.append(json.dumps({
                "timestamp": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                "price": 85000.0 + (i * 10),  # Price changes every minute
                "change_pct": 0.01 * i,
                "regime": "Moderate Volatility Bullish"
            }))
        
        # Mock Redis.lrange to return our minute data
        self.redis_mock.lrange.return_value = minute_data
        
        # Act
        compress_historical_data(
            "price_history",
            self.current_time.date(),
            source_granularity=TimeSeriesGranularity.MINUTE,
            target_granularity=TimeSeriesGranularity.HOURLY
        )
        
        # Assert
        # Check that lrange was called to get minute data
        self.redis_mock.lrange.assert_called_with(minute_key, 0, -1)
        
        # Verify call to rpush with compressed data
        # The mock.call_args contains the args and kwargs of the last call
        rpush_args = self.redis_mock.rpush.call_args
        self.assertEqual(rpush_args[0][0], hourly_key)
        
        # Parse the compressed data from the JSON string
        compressed_data = json.loads(rpush_args[0][1])
        
        # Verify the compressed data structure
        self.assertIn("timestamp", compressed_data)
        self.assertIn("price_avg", compressed_data)
        self.assertIn("price_min", compressed_data)
        self.assertIn("price_max", compressed_data)
        self.assertIn("price_open", compressed_data)
        self.assertIn("price_close", compressed_data)
        self.assertIn("change_pct_cumulative", compressed_data)
        self.assertIn("data_points", compressed_data)
        
        # Check that data was properly aggregated
        self.assertEqual(compressed_data["price_open"], 85000.0)  # First price
        self.assertEqual(compressed_data["price_close"], 85590.0)  # Last price (85000 + 59*10)
        self.assertEqual(compressed_data["data_points"], 60)  # 60 minutes of data

    def test_get_time_series_data(self):
        """Test retrieving time series data"""
        # Arrange
        minute_key = f"sim_price_history:{self.current_time.date().isoformat()}:minute"
        hour_14_data = json.dumps({
            "timestamp": "2024-05-01 14:30:00",
            "price": 85000.0,
            "change_pct": 0.05,
            "regime": "Moderate Volatility Bullish"
        })
        self.redis_mock.lrange.return_value = [hour_14_data]
        
        # Act
        result = get_time_series_data(
            "price_history",
            self.current_time.date(),
            TimeSeriesGranularity.MINUTE
        )
        
        # Assert
        self.redis_mock.lrange.assert_called_with(minute_key, 0, -1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["price"], 85000.0)

    def test_cleanup_old_data(self):
        """Test cleaning up old data beyond retention periods"""
        # Arrange
        current_date = datetime.date(2024, 5, 15)
        
        # Mock Redis.keys to return some old keys
        old_keys = [
            "sim_price_history:2024-04-01:minute",  # >30 days old
            "sim_price_history:2024-05-01:minute",  # >14 days old
            "sim_price_history:2024-05-14:minute",  # 1 day old
        ]
        self.redis_mock.keys.return_value = old_keys
        
        # Act
        cleanup_old_data("price_history", current_date)
        
        # Assert
        # Check that keys method was called correctly
        self.redis_mock.keys.assert_called_with("sim_price_history:*")
        
        # Check that delete was called for old keys
        self.assertTrue(self.redis_mock.delete.called)
        
        # Delete should be called at least once with the oldest key
        self.redis_mock.delete.assert_any_call("sim_price_history:2024-04-01:minute")

if __name__ == '__main__':
    unittest.main() 