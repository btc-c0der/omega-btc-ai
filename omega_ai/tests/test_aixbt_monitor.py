#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌌 AIXBT Divine Monitor Tests - GBU2™ Integration
-----------------------------------------------
Test suite for the AIXBT Divine Monitor implementation.
"""

import unittest
import asyncio
import aiohttp
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from omega_ai.scripts.monitor_aixbt import AIXBTDivineMonitor

class TestAIXBTDivineMonitor(unittest.TestCase):
    """Test cases for the AIXBT Divine Monitor."""
    
    def setUp(self):
        """Set up test environment."""
        self.monitor = AIXBTDivineMonitor()
        self.monitor.redis = Mock()
        self.monitor.divine_metrics = Mock()
        self.monitor.fibonacci_healing = Mock()
        self.monitor.gamon_matrix = Mock()
        self.monitor.trap_tracker = Mock()
        
    @patch('aiohttp.ClientSession.get')
    async def test_fetch_divine_data(self, mock_get):
        """Test fetching divine data from BitGet."""
        # Mock response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = Mock(return_value={
            'data': [{
                'symbol': 'AIXBTUSDT',
                'last': '1.2345',
                'volume': '1000.0'
            }]
        })
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Test fetch
        data = await self.monitor.fetch_divine_data()
        
        # Assertions
        self.assertIsNotNone(data)
        self.assertEqual(data['price'], 1.2345)
        self.assertEqual(data['volume'], 1000.0)
        self.assertIsInstance(data['timestamp'], int)
        
    def test_calculate_divine_alignment(self):
        """Test calculation of divine alignment score."""
        # Mock component returns
        self.monitor.fibonacci_healing.get_fibonacci_levels.return_value = {
            '0.236': 1.0,
            '0.382': 1.1,
            '0.5': 1.2,
            '0.618': 1.3,
            '0.786': 1.4
        }
        self.monitor.gamon_matrix.get_current_state.return_value = {
            'state': 'MARKUP',
            'confidence': 0.8
        }
        self.monitor.trap_tracker.analyze_trap_formation.return_value = {
            'trap_detected': False,
            'confidence': 0.9
        }
        
        # Mock metric calculations
        self.monitor.divine_metrics.calculate_price_harmony.return_value = 0.8
        self.monitor.divine_metrics.calculate_volume_harmony.return_value = 0.7
        self.monitor.divine_metrics.calculate_trap_harmony.return_value = 0.9
        
        # Test calculation
        price_data = {
            'price': 1.2345,
            'volume': 1000.0,
            'timestamp': int(datetime.now().timestamp())
        }
        alignment = self.monitor.calculate_divine_alignment(price_data)
        
        # Assertions
        self.assertIsInstance(alignment, float)
        self.assertGreaterEqual(alignment, 0.0)
        self.assertLessEqual(alignment, 1.0)
        
    def test_store_divine_metrics(self):
        """Test storing divine metrics in Redis."""
        # Test data
        price_data = {
            'price': 1.2345,
            'volume': 1000.0,
            'timestamp': int(datetime.now().timestamp())
        }
        alignment = 0.85
        
        # Test storage
        self.monitor.store_divine_metrics(price_data, alignment)
        
        # Assert Redis calls
        self.monitor.redis.hset.assert_any_call(
            f"{self.monitor.REDIS_KEY_PREFIX}price",
            mapping={
                'value': price_data['price'],
                'volume': price_data['volume'],
                'timestamp': price_data['timestamp']
            }
        )
        self.monitor.redis.hset.assert_any_call(
            f"{self.monitor.REDIS_KEY_PREFIX}alignment",
            mapping={
                'score': alignment,
                'timestamp': price_data['timestamp']
            }
        )
        self.monitor.redis.zadd.assert_called_once()
        
    def test_get_divine_summary(self):
        """Test getting divine summary."""
        # Mock component returns
        self.monitor.last_price = 1.2345
        self.monitor.last_volume = 1000.0
        self.monitor.last_update = int(datetime.now().timestamp())
        self.monitor.divine_alignment = 0.85
        
        self.monitor.fibonacci_healing.get_fibonacci_levels.return_value = {
            '0.236': 1.0,
            '0.382': 1.1,
            '0.5': 1.2,
            '0.618': 1.3,
            '0.786': 1.4
        }
        self.monitor.gamon_matrix.get_current_state.return_value = {
            'state': 'MARKUP',
            'confidence': 0.8
        }
        self.monitor.trap_tracker.analyze_trap_formation.return_value = {
            'trap_detected': False,
            'confidence': 0.9
        }
        
        # Test summary
        summary = self.monitor.get_divine_summary()
        
        # Assertions
        self.assertIsInstance(summary, dict)
        self.assertEqual(summary['price'], self.monitor.last_price)
        self.assertEqual(summary['volume'], self.monitor.last_volume)
        self.assertEqual(summary['last_update'], self.monitor.last_update)
        self.assertEqual(summary['divine_alignment'], self.monitor.divine_alignment)
        self.assertIn('fibonacci_levels', summary)
        self.assertIn('gamon_state', summary)
        self.assertIn('trap_analysis', summary)

if __name__ == '__main__':
    unittest.main() 