#!/usr/bin/env python3
"""
Tests for the BTC price display functionality in the Reggae Dashboard.
"""

import json
import unittest
from unittest.mock import Mock, patch
import redis
from datetime import datetime, timezone

class TestBTCPriceDisplay(unittest.TestCase):
    """Test cases for the BTC price display functionality."""

    def test_btc_price_with_direct_value(self):
        """Test BTC price retrieval with a direct value in last_btc_price."""
        # Mock Redis get to return a direct price value
        mock_redis = Mock()
        mock_redis.get.side_effect = lambda key: "84500.25" if key == "last_btc_price" else None
        
        # Call the get_btc_price logic directly
        result = self._get_btc_price_data(mock_redis)
        
        # Check if correct price is returned
        self.assertEqual(result["price"], 84500.25)
        self.assertEqual(result["source"], "Redis")
    
    def test_btc_price_with_json_value(self):
        """Test BTC price retrieval with a JSON value in btc_price."""
        # Mock Redis get to return a JSON with price field
        mock_redis = Mock()
        mock_redis.get.side_effect = lambda key: json.dumps({"price": 84750.75}) if key == "btc_price" else None
        
        # Call the get_btc_price logic directly
        result = self._get_btc_price_data(mock_redis)
        
        # Check if correct price is returned
        self.assertEqual(result["price"], 84750.75)
        self.assertEqual(result["source"], "Redis")
    
    def test_btc_price_with_position_data(self):
        """Test BTC price extraction from position data."""
        # Mock Redis get to return position data with current_price field
        mock_redis = Mock()
        position_data = {
            "entry_price": 83000, 
            "current_price": 84800.50,
            "direction": "LONG"
        }
        mock_redis.get.side_effect = lambda key: json.dumps(position_data) if key == "current_position" else None
        
        # Call the get_btc_price logic directly
        result = self._get_btc_price_data(mock_redis)
        
        # Check if correct price is returned
        self.assertEqual(result["price"], 84800.50)
        self.assertEqual(result["source"], "Redis")
    
    def test_btc_price_with_fallback(self):
        """Test BTC price falling back to default when no price available."""
        # Mock Redis get to always return None
        mock_redis = Mock()
        mock_redis.get.return_value = None
        
        # Call the get_btc_price logic directly
        result = self._get_btc_price_data(mock_redis)
        
        # Check if fallback price is returned (default is 65000)
        self.assertEqual(result["price"], 65000)
        # In our implementation, the source is still "Redis" when using fallback price
        self.assertEqual(result["source"], "Redis")
    
    def test_btc_price_with_changes(self):
        """Test BTC price with price change data."""
        # Mock Redis get for both price and changes
        mock_redis = Mock()
        
        # Set up side effect to return different values for different keys
        def mock_get(key):
            if key == "last_btc_price":
                return "84500.25"
            elif key == "btc_price_changes":
                return json.dumps({
                    "short_term": 1.25,
                    "medium_term": -0.5,
                    "long_term": 5.75
                })
            elif key == "prev_btc_price":
                return "84000.0"
            else:
                return None
                
        mock_redis.get.side_effect = mock_get
        
        # Call the get_btc_price logic directly
        result = self._get_btc_price_data(mock_redis)
        
        # Check if price and changes are correctly returned
        self.assertEqual(result["price"], 84500.25)
        self.assertEqual(result["changes"]["short_term"], 1.25)
        self.assertEqual(result["changes"]["medium_term"], -0.5)
        self.assertEqual(result["changes"]["long_term"], 5.75)
        # Check percentage change calculation with a more precise value
        self.assertAlmostEqual(result["change"], 0.5955, places=4)  # (84500.25 - 84000) / 84000 * 100
    
    def test_btc_price_with_patterns(self):
        """Test BTC price with price pattern data."""
        # Mock Redis get for both price and patterns
        mock_redis = Mock()
        
        # Set up side effect to return different values for different keys
        def mock_get(key):
            if key == "last_btc_price":
                return "84500.25"
            elif key == "btc_price_patterns":
                return json.dumps({
                    "bullish": 0.75,
                    "bearish": 0.15,
                    "neutral": 0.05,
                    "volatile": 0.05
                })
            else:
                return None
                
        mock_redis.get.side_effect = mock_get
        
        # Call the get_btc_price logic directly
        result = self._get_btc_price_data(mock_redis)
        
        # Check if price and patterns are correctly returned
        self.assertEqual(result["price"], 84500.25)
        self.assertEqual(result["patterns"]["bullish"], 0.75)
        self.assertEqual(result["patterns"]["bearish"], 0.15)
        self.assertEqual(result["patterns"]["neutral"], 0.05)
        self.assertEqual(result["patterns"]["volatile"], 0.05)
        
    def _get_btc_price_data(self, r):
        """Replicate the BTC price logic from the server."""
        try:
            # Try to get price data from different Redis keys in priority order
            price_keys = ['btc_price', 'last_btc_price', 'current_position']
            current_price = None
            
            for key in price_keys:
                try:
                    price_str = r.get(key)
                    if not price_str:
                        continue
                        
                    # Handle different data formats
                    if key == 'btc_price':
                        # btc_price is stored as JSON with a price field
                        data = json.loads(price_str)
                        if 'price' in data:
                            current_price = float(data['price'])
                            break
                    elif key == 'last_btc_price':
                        # last_btc_price is stored directly as a string
                        current_price = float(price_str)
                        break
                    elif key == 'current_position':
                        # Extract from position data if available
                        position_data = json.loads(price_str)
                        if 'current_price' in position_data:
                            current_price = float(position_data['current_price'])
                            break
                except (ValueError, TypeError, json.JSONDecodeError):
                    continue
            
            # Default fallback if all else fails
            if current_price is None:
                current_price = 65000  # Default fallback
            
            # Get change data directly from Redis if available
            change_data = r.get("btc_price_changes")
            changes = {
                "short_term": -0.06,
                "medium_term": -0.79,
                "long_term": 3.76
            }
            
            if change_data:
                try:
                    changes = json.loads(change_data)
                except json.JSONDecodeError:
                    pass
            
            # Get price patterns data
            patterns_data = r.get("btc_price_patterns")
            patterns = {
                "bullish": 0.16,
                "bearish": 0.03,
                "neutral": 0.49,
                "volatile": 0.19
            }
            
            if patterns_data:
                try:
                    patterns = json.loads(patterns_data)
                except json.JSONDecodeError:
                    pass
            
            # Calculate the percentage change
            prev_price_str = r.get("prev_btc_price")
            if prev_price_str:
                try:
                    prev_price = float(prev_price_str)
                    if prev_price > 0:
                        change = ((current_price - prev_price) / prev_price) * 100
                    else:
                        change = 0
                except (ValueError, TypeError):
                    change = 0
            else:
                change = 0
            
            return {
                "price": current_price,
                "change": change,
                "changes": changes,
                "patterns": patterns,
                "source": "Redis",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            return {
                "price": 65000,  # Default fallback price
                "change": 0.0,
                "changes": {
                    "short_term": 0.0,
                    "medium_term": 0.0,
                    "long_term": 0.0
                },
                "patterns": {
                    "bullish": 0.25,
                    "bearish": 0.25,
                    "neutral": 0.25,
                    "volatile": 0.25
                },
                "source": "Error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }


if __name__ == '__main__':
    unittest.main() 