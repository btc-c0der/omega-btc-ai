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
Test script for the market trends monitor
"""

import sys
import os
import time
import logging
import redis
import unittest
import json
from unittest.mock import patch, MagicMock
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Try to import the monitor module
try:
    from omega_ai.monitor.monitor_market_trends_fixed import (
        MarketTrendAnalyzer, 
        monitor_market_trends,
        redis_conn,
        analyze_price_trend,
        update_fibonacci_data,
        get_current_fibonacci_levels
    )
    logger.info("Successfully imported monitor_market_trends_fixed")
except ImportError as e:
    logger.error(f"Failed to import market trends monitor: {e}")
    logger.error("Make sure you're running this from the project root directory")
    sys.exit(1)

class TestMarketTrendsMonitor(unittest.TestCase):
    """Test cases for market trends monitor"""
    
    def setUp(self):
        # Configure Redis connection for testing
        try:
            self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.redis.ping()
            logger.info("Connected to Redis successfully")
        except redis.ConnectionError as e:
            logger.error(f"Could not connect to Redis: {e}")
            logger.error("Please ensure Redis is running on localhost:6379")
            sys.exit(1)
            
        # Create a sample BTC price
        self.price = 50000.0
        
        # Save to Redis for testing
        self.redis.set("last_btc_price", str(self.price))
        logger.info(f"Set test BTC price in Redis: ${self.price}")
        
        # Create analyzer instance
        self.analyzer = MarketTrendAnalyzer()
        
    def test_redis_connection(self):
        """Test that Redis connection works"""
        try:
            result = self.redis.ping()
            self.assertTrue(result)
            logger.info("✓ Redis connection test passed")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.fail(f"Redis connection failed: {e}")
    
    def test_btc_price_available(self):
        """Test that BTC price is available in Redis"""
        price_str: Optional[str] = self.redis.get("last_btc_price")
        self.assertIsNotNone(price_str)
        # Convert to float only if price_str is not None
        if price_str is not None:
            price = float(price_str)
            self.assertEqual(price, self.price)
            logger.info("✓ BTC price retrieval test passed")
    
    def test_fibonacci_update(self):
        """Test Fibonacci data update"""
        try:
            update_fibonacci_data(self.price)
            fib_data = get_current_fibonacci_levels()
            self.assertIsNotNone(fib_data)
            logger.info("✓ Fibonacci data update test passed")
            logger.info(f"Fibonacci levels: {json.dumps(fib_data, indent=2)}")
        except Exception as e:
            logger.error(f"Fibonacci update failed: {e}")
            self.fail(f"Fibonacci update failed: {e}")
    
    def test_trend_analysis(self):
        """Test trend analysis for different timeframes"""
        try:
            results = self.analyzer.analyze_trends()
            self.assertIsNotNone(results)
            self.assertIn("current_price", results)
            logger.info("✓ Trend analysis test passed")
            
            # Check if any timeframes were analyzed
            timeframes_found = False
            for key in results:
                if "min" in key:
                    timeframes_found = True
                    logger.info(f"Timeframe {key}: {results[key]}")
            
            if not timeframes_found:
                logger.warning("No timeframes were found in the analysis results")
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            self.fail(f"Trend analysis failed: {e}")
    
    @patch('omega_ai.monitor.monitor_market_trends_fixed.clear_screen')
    @patch('omega_ai.monitor.monitor_market_trends_fixed.display_fibonacci_levels')
    def test_fixed_display_mode(self, mock_display_fib, mock_clear):
        """Test fixed display mode with mocks to avoid actual display"""
        # Patch environment to simulate fixed display mode
        with patch.dict(os.environ, {"FIXED_DISPLAY": "true"}):
            # Create a dummy analyzer that just returns some data
            mock_analyzer = MagicMock()
            mock_analyzer.analyze_trends.return_value = {
                "current_price": self.price,
                "5min": {"trend": "bullish", "change": 1.5},
                "15min": {"trend": "bearish", "change": -0.8}
            }
            
            # Test just one iteration by overriding the infinite loop
            with patch('omega_ai.monitor.monitor_market_trends_fixed.MarketTrendAnalyzer', 
                       return_value=mock_analyzer):
                with patch('omega_ai.monitor.monitor_market_trends_fixed.time.sleep', 
                           side_effect=KeyboardInterrupt):
                    try:
                        monitor_market_trends()
                    except KeyboardInterrupt:
                        pass
            
            # Verify function calls
            self.assertTrue(mock_clear.called)
            logger.info("✓ Fixed display mode test passed")
    
    def tearDown(self):
        # Clean up test data
        self.redis.delete("fibonacci_levels")
        self.redis.delete("last_btc_price")
        logger.info("Cleaned up test data")

if __name__ == "__main__":
    logger.info("Starting market trends monitor tests")
    unittest.main(verbosity=2) 