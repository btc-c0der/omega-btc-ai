import unittest
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os
import pandas as pd
import logging

# Add the project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from omega_ai.ml.market_trends_model import MarketTrendsModel

class TestMarketTrendsModelFallback(unittest.TestCase):
    """Test the fallback mechanisms for market trends model when scaler is not fitted."""

    @patch('omega_ai.ml.market_trends_model.redis.StrictRedis')
    def test_predict_price_with_unfitted_scaler(self, mock_redis):
        """Test that price prediction works even when scaler is not fitted."""
        # Create a mock Redis connection
        redis_instance = MagicMock()
        redis_instance.get.return_value = "50000"  # Current BTC price
        redis_instance.lrange.return_value = ["49000,1500", "48000,1200"]  # Price history
        mock_redis.return_value = redis_instance
        
        # Create the model with mocked Redis
        model = MarketTrendsModel(redis_host='localhost', redis_port=6379)
        
        # Mock the model components
        model.price_regressor = MagicMock()
        model.price_regressor.predict.return_value = np.array([0.05])  # 5% increase prediction
        model.price_regressor.score.return_value = 0.75  # 75% confidence
        model.price_regressor.feature_names_in_ = ["feature1", "feature2"]
        
        # Create a basic dataframe for testing
        df = pd.DataFrame({
            "price": [50000],
            "feature1": [1.0],
            "feature2": [2.0]
        })
        
        # Mock get_latest_data to return our test dataframe
        model.get_latest_data = MagicMock(return_value=df)
        
        # Call predict_price method which should use the fallback due to unfitted scaler
        with self.assertLogs(level=logging.WARNING):  # Should log a warning
            result = model.predict_price()
        
        # Verify the fallback calculation was used correctly (current_price * (1 + scaled_pred))
        self.assertAlmostEqual(result["price"], 50000 * 1.05, delta=1)
        self.assertEqual(result["confidence"], 0.75)
        self.assertAlmostEqual(result["pct_change"], 5.0, delta=0.1)
        
        # Verify Redis was called to store the prediction
        redis_instance.set.assert_called()

    @patch('omega_ai.ml.market_trends_model.redis.StrictRedis')
    def test_predict_price_with_fitted_scaler(self, mock_redis):
        """Test that price prediction works normally when scaler is fitted."""
        # Create a mock Redis connection
        redis_instance = MagicMock()
        redis_instance.get.return_value = "50000"  # Current BTC price
        redis_instance.lrange.return_value = ["49000,1500", "48000,1200"]  # Price history
        mock_redis.return_value = redis_instance
        
        # Create the model with mocked Redis
        model = MarketTrendsModel(redis_host='localhost', redis_port=6379)
        
        # Mock the model components
        model.price_regressor = MagicMock()
        model.price_regressor.predict.return_value = np.array([0.75])  # Scaled prediction
        model.price_regressor.score.return_value = 0.8  # 80% confidence
        model.price_regressor.feature_names_in_ = ["feature1", "feature2"]
        
        # Create a basic dataframe for testing
        df = pd.DataFrame({
            "price": [50000],
            "feature1": [1.0],
            "feature2": [2.0]
        })
        
        # Mock get_latest_data to return our test dataframe
        model.get_latest_data = MagicMock(return_value=df)
        
        # Initialize price_scaler (normally done during training)
        model.price_scaler.fit(np.array([[0.5], [0.75], [1.0]]))
        
        # Configure the scaler to return a specific value for testing
        model.price_scaler.inverse_transform = MagicMock(return_value=np.array([[55000]]))
        
        # Call predict_price method - should use the normal scaler path
        result = model.predict_price()
        
        # Verify the normal prediction path was used
        self.assertEqual(result["price"], 55000)
        self.assertEqual(result["confidence"], 0.8)
        
        # Ensure price_scaler.inverse_transform was called
        model.price_scaler.inverse_transform.assert_called_once()
        
        # Verify Redis was called to store the prediction
        redis_instance.set.assert_called()

    @patch('omega_ai.ml.market_trends_model.redis.StrictRedis')
    def test_generate_predictions_with_trap_conf(self, mock_redis):
        """Test that the divine wisdom generator uses trap_conf correctly."""
        # Create a mock Redis connection
        redis_instance = MagicMock()
        mock_redis.return_value = redis_instance
        
        # Create the model with mocked Redis
        model = MarketTrendsModel(redis_host='localhost', redis_port=6379)
        
        # Mock the prediction methods
        model.predict_trend = MagicMock(return_value={"trend": "Bullish", "confidence": 0.9})
        model.predict_price = MagicMock(return_value={
            "price": 55000, 
            "current_price": 50000, 
            "pct_change": 10.0, 
            "confidence": 0.8
        })
        model.predict_mm_trap = MagicMock(return_value={
            "trap_detected": True, 
            "trap_type": "Bull Trap", 
            "confidence": 0.85
        })
        
        # Call generate_predictions which should then call _generate_divine_wisdom
        predictions = model.generate_predictions()
        
        # Generate divine wisdom directly for testing
        wisdom = model._generate_divine_wisdom(predictions)
        
        # Verify the wisdom reflects the trap with high confidence
        self.assertIn("trap", wisdom.lower())
        
        # Change to no trap detected and verify trap isn't mentioned
        model.predict_mm_trap = MagicMock(return_value={
            "trap_detected": False, 
            "trap_type": None, 
            "confidence": 0.1
        })
        
        predictions = model.generate_predictions()
        wisdom = model._generate_divine_wisdom(predictions)
        
        # Verify no trap is mentioned when confidence is low
        self.assertNotIn("trap", wisdom.lower())

if __name__ == '__main__':
    unittest.main() 