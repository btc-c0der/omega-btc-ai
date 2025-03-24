#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC Data Handler Tests
====================================

Test cases for the BTC Data Handler module.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import redis
import json
from btc_data_handler import BTCDataHandler

class TestBTCDataHandler(unittest.TestCase):
    """Test cases for BTCDataHandler."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a mock Redis client
        self.mock_redis = Mock(spec=redis.Redis)
        self.mock_redis.get.return_value = None
        self.mock_redis.set.return_value = True
        
        # Create test data with proper DatetimeIndex
        dates = pd.date_range(start='2024-01-01', periods=5, freq='D')
        self.test_data = pd.DataFrame({
            'open': np.random.random(5),
            'high': np.random.random(5),
            'low': np.random.random(5),
            'close': np.random.random(5),
            'volume': np.random.random(5)
        }, index=dates)
        
        # Create handler with mock Redis
        self.handler = BTCDataHandler()
        self.handler.redis_client = self.mock_redis
    
    def test_store_in_redis(self):
        """Test storing data in Redis."""
        try:
            self.handler._store_in_redis(self.test_data)
            # Verify Redis set was called for each row
            self.assertEqual(self.mock_redis.set.call_count, len(self.test_data))
            
            # Verify the data format in Redis
            for i, (date, row) in enumerate(self.test_data.iterrows()):
                # Ensure date is a datetime object
                if not isinstance(date, pd.Timestamp):
                    date = pd.Timestamp(date)
                expected_key = f"btc:{date.strftime('%Y-%m-%d')}"
                call_args = self.mock_redis.set.call_args_list[i]
                
                # Check key
                self.assertEqual(call_args[0][0], expected_key)
                
                # Check data format
                stored_data = json.loads(call_args[0][1])
                self.assertIn('date', stored_data)
                self.assertEqual(stored_data['date'], date.strftime('%Y-%m-%d'))
                self.assertIn('open', stored_data)
                self.assertIn('high', stored_data)
                self.assertIn('low', stored_data)
                self.assertIn('close', stored_data)
                self.assertIn('volume', stored_data)
                
        except Exception as e:
            self.fail(f"test_store_in_redis raised {type(e).__name__} unexpectedly!")
    
    def test_store_in_redis_with_missing_date(self):
        """Test storing data in Redis when date column is missing."""
        # Create data without date column
        data_without_date = self.test_data.copy()
        data_without_date.index.name = None
        
        try:
            self.handler._store_in_redis(data_without_date)
            # Verify Redis set was called for each row
            self.assertEqual(self.mock_redis.set.call_count, len(data_without_date))
            
            # Verify the data format in Redis
            for i, (date, row) in enumerate(data_without_date.iterrows()):
                # Ensure date is a datetime object
                if not isinstance(date, pd.Timestamp):
                    date = pd.Timestamp(date)
                expected_key = f"btc:{date.strftime('%Y-%m-%d')}"
                call_args = self.mock_redis.set.call_args_list[i]
                
                # Check key
                self.assertEqual(call_args[0][0], expected_key)
                
                # Check data format
                stored_data = json.loads(call_args[0][1])
                self.assertIn('date', stored_data)
                self.assertEqual(stored_data['date'], date.strftime('%Y-%m-%d'))
                
        except Exception as e:
            self.fail(f"test_store_in_redis_with_missing_date raised {type(e).__name__} unexpectedly!")
    
    def test_get_from_redis(self):
        """Test retrieving data from Redis."""
        # Mock Redis keys
        self.mock_redis.keys.return_value = [
            b"btc:2024-01-01",
            b"btc:2024-01-02",
            b"btc:2024-01-03"
        ]
        
        # Mock Redis get responses
        mock_data = [
            json.dumps({
                'date': '2024-01-01',
                'open': 100.0,
                'high': 101.0,
                'low': 99.0,
                'close': 100.5,
                'volume': 1000.0
            }),
            json.dumps({
                'date': '2024-01-02',
                'open': 100.5,
                'high': 102.0,
                'low': 100.0,
                'close': 101.5,
                'volume': 1100.0
            }),
            json.dumps({
                'date': '2024-01-03',
                'open': 101.5,
                'high': 103.0,
                'low': 101.0,
                'close': 102.5,
                'volume': 1200.0
            })
        ]
        self.mock_redis.get.side_effect = mock_data
        
        # Get data from Redis with start date
        start_date = "2024-01-01"
        df = self.handler._get_from_redis(start_date)
        
        # Verify DataFrame structure
        self.assertIsInstance(df, pd.DataFrame)
        if df is not None:
            self.assertEqual(len(df), 3)
            self.assertTrue(all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume']))
            self.assertTrue(isinstance(df.index, pd.DatetimeIndex))
    
    def test_get_btc_data_with_redis_failure(self):
        """Test getting BTC data when Redis fails."""
        # Mock Redis to return None for keys
        self.mock_redis.keys.return_value = []
        
        # Mock yfinance download
        with patch('yfinance.download') as mock_yf:
            mock_yf.return_value = self.test_data
            
            # Get data
            df = self.handler.get_btc_data()
            
            # Verify data was retrieved from yfinance
            self.assertIsNotNone(df)
            if df is not None:
                self.assertEqual(len(df), len(self.test_data))
                self.assertTrue(all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume']))
                # Verify data was stored in Redis
                self.assertEqual(self.mock_redis.set.call_count, len(df))

if __name__ == '__main__':
    unittest.main() 