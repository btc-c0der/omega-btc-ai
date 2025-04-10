
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

import unittest
from unittest.mock import patch, MagicMock
import json
import pandas as pd
import numpy as np
from datetime import datetime, timezone

from omega_ai.ml.market_trends_model import MarketTrendsModel


class TestMarketTrendsModel(unittest.TestCase):
    """Test cases for the MarketTrendsModel class."""

    def setUp(self):
        """Set up test data and mocks."""
        # Mock Redis connection and data
        self.redis_mock = MagicMock()
        self.redis_mock.get.side_effect = self._mock_redis_get
        self.redis_mock.lrange.return_value = self._mock_price_history()
        
        # Set up price and trend data
        self.current_price = 80000.0
        self.current_volume = 1000.0
        
        # Create test dataframe
        self.test_df = self._create_test_dataframe()
        
        # Patch the Redis connection
        patcher = patch('redis.StrictRedis', return_value=self.redis_mock)
        self.addCleanup(patcher.stop)
        patcher.start()
        
        # Initialize model with mock redis
        self.model = MarketTrendsModel(redis_host='fake_host', redis_port=1234)
        self.model.redis_conn = self.redis_mock
        
        # Mock the model's internal methods
        self.model._engineer_features = MagicMock(return_value=self.test_df)
        
        # Set up model components with simple mocks
        self.model.trend_classifier = MagicMock()
        self.model.trend_classifier.predict.return_value = [1]  # Bullish
        self.model.trend_classifier.predict_proba.return_value = [[0.2, 0.7, 0.1]]
        
        self.model.price_regressor = MagicMock()
        self.model.price_regressor.predict.return_value = [0.75]  # Scaled prediction
        self.model.price_regressor.score.return_value = 0.85
        
        self.model.trap_classifier = MagicMock()
        self.model.trap_classifier.predict.return_value = [1]  # Trap detected
        self.model.trap_classifier.predict_proba.return_value = [[0.25, 0.75]]
        
        # Mock the scaler
        self.model.price_scaler = MagicMock()
        self.model.price_scaler.inverse_transform.return_value = [[84000.0]]  # 5% up
    
    def _mock_redis_get(self, key):
        """Mocked Redis get method."""
        data = {
            "last_btc_price": str(self.current_price),
            "last_btc_volume": str(self.current_volume),
            "btc_trend_15min": json.dumps({
                "trend": "Bullish",
                "change": 1.5,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }),
            "btc_trend_60min": json.dumps({
                "trend": "Strongly Bullish",
                "change": 2.5,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        }
        return data.get(key)
    
    def _mock_price_history(self):
        """Generate mock price history data."""
        # Create 100 price points with slight uptrend
        prices = []
        base_price = 75000.0
        for i in range(100):
            price = base_price * (1 + 0.0001 * i) + (np.random.random() - 0.5) * 100
            volume = 500 + np.random.random() * 1000
            prices.append(f"{price},{volume}")
        return prices
    
    def _create_test_dataframe(self):
        """Create a test dataframe for model training and prediction."""
        # Create a basic dataframe with price and volume
        data = {
            "price": [self.current_price],
            "volume": [self.current_volume],
            "trend_15min": [1],  # Bullish
            "change_15min": [1.5],
            "trend_60min": [1],  # Bullish
            "change_60min": [2.5],
            "ma_21": [self.current_price * 0.98],  # Price is above MA
            "vol_21": [500.0],
            "rsi_14": [65.0],  # Slightly overbought
        }
        return pd.DataFrame(data)
    
    def test_get_historical_data(self):
        """Test retrieving historical data from Redis."""
        # Override the engineered features function for this test
        self.model._engineer_features = lambda df: df
        
        # Get historical data
        df = self.model.get_historical_data(days_back=1)
        
        # Verify the data was retrieved and processed correctly
        self.assertFalse(df.empty)
        self.assertIn("price", df.columns)
        self.assertIn("volume", df.columns)
        
        # Verify Redis was called correctly
        self.redis_mock.lrange.assert_called_with("btc_movement_history", 0, -1)
    
    def test_predict_trend(self):
        """Test trend prediction."""
        # Make a prediction
        prediction = self.model.predict_trend()
        
        # Verify prediction format and values
        self.assertIn("trend", prediction)
        self.assertIn("confidence", prediction)
        self.assertEqual(prediction["trend"], "Bullish")
        self.assertGreater(prediction["confidence"], 0.0)
        
        # Verify values were stored in Redis
        self.redis_mock.set.assert_called()
        call_args = self.redis_mock.set.call_args[0]
        self.assertEqual(call_args[0], "ai_trend_prediction")
        self.assertIn("trend", json.loads(call_args[1]))
    
    def test_predict_price(self):
        """Test price prediction."""
        # Make a prediction
        prediction = self.model.predict_price()
        
        # Verify prediction format and values
        self.assertIn("price", prediction)
        self.assertIn("current_price", prediction)
        self.assertIn("pct_change", prediction)
        self.assertIn("confidence", prediction)
        
        # Calculated values should match our mocked data
        self.assertEqual(prediction["current_price"], self.current_price)
        self.assertEqual(prediction["price"], 84000.0)
        
        # Verify values were stored in Redis
        self.redis_mock.set.assert_called()
    
    def test_predict_mm_trap(self):
        """Test market maker trap prediction."""
        # Make a prediction
        prediction = self.model.predict_mm_trap()
        
        # Verify prediction format and values
        self.assertIn("trap_detected", prediction)
        self.assertIn("confidence", prediction)
        
        # Our mock is set to detect a trap
        self.assertTrue(prediction["trap_detected"])
        self.assertEqual(prediction["trap_type"], "Bull Trap")
        
        # Verify values were stored in Redis
        self.redis_mock.set.assert_called()
    
    def test_generate_predictions(self):
        """Test generating comprehensive predictions."""
        # Generate all predictions
        predictions = self.model.generate_predictions()
        
        # Verify the prediction format
        self.assertIn("timestamp", predictions)
        self.assertIn("trend", predictions)
        self.assertIn("price", predictions)
        self.assertIn("trap", predictions)
        
        # Verify combined predictions were stored in Redis
        self.redis_mock.set.assert_called_with("ai_predictions", 
                                             json.dumps(predictions))
    
    def test_encode_trend(self):
        """Test trend encoding function."""
        self.assertEqual(self.model._encode_trend("Bullish"), 1)
        self.assertEqual(self.model._encode_trend("Strongly Bullish"), 1)
        self.assertEqual(self.model._encode_trend("Bearish"), -1)
        self.assertEqual(self.model._encode_trend("Strongly Bearish"), -1)
        self.assertEqual(self.model._encode_trend("Neutral"), 0)
    
    @patch('omega_ai.ml.market_trends_model.RandomForestClassifier')
    def test_train_trend_model(self, rf_mock):
        """Test training the trend classification model."""
        # Mock the prepare_training_data method
        self.model.prepare_training_data = MagicMock(return_value=(
            pd.DataFrame({"feature1": [1, 2, 3]}),  # X_train
            pd.DataFrame({"feature1": [4, 5, 6]}),  # X_test
            pd.Series([1, 1, -1]),                  # y_train
            pd.Series([1, -1, 0])                   # y_test
        ))
        
        # Mock the classifier
        rf_instance = MagicMock()
        rf_instance.predict.return_value = [1, -1, 0]
        rf_mock.return_value = rf_instance
        
        # Mock the save_models method
        self.model.save_models = MagicMock()
        
        # Train the model
        self.model.train_trend_model(self.test_df, forecast_period=3)
        
        # Verify the model was trained
        rf_instance.fit.assert_called_once()
        self.model.save_models.assert_called_once()
    
    def test_calculate_harmony_score(self):
        """Test calculating the Fibonacci harmony score."""
        predictions = {
            "trend": {"trend": "Bullish", "confidence": 0.8},
            "price": {"price": 84000.0, "current_price": 80000.0, 
                     "pct_change": 5.0, "confidence": 0.7},
            "trap": {"trap_detected": False, "confidence": 0.9}
        }
        
        # Calculate harmony score
        score = self.model._calculate_harmony_score(predictions)
        
        # Score should be positive and within expected range
        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 10.0)
        
        # Test with trap detected - score should be lower
        predictions["trap"]["trap_detected"] = True
        trap_score = self.model._calculate_harmony_score(predictions)
        self.assertLess(trap_score, score)
    
    def test_generate_divine_wisdom(self):
        """Test generating divine wisdom based on predictions."""
        predictions = {
            "trend": {"trend": "Bullish", "confidence": 0.8},
            "price": {"price": 84000.0, "current_price": 80000.0, 
                     "pct_change": 5.0, "confidence": 0.7},
            "trap": {"trap_detected": False, "confidence": 0.9}
        }
        
        # Generate wisdom
        wisdom = self.model._generate_divine_wisdom(predictions)
        
        # Wisdom should be a non-empty string
        self.assertIsInstance(wisdom, str)
        self.assertTrue(len(wisdom) > 0)
        
        # Test with trap detected - wisdom should mention trap
        predictions["trap"]["trap_detected"] = True
        predictions["trap"]["trap_type"] = "Bull Trap"
        predictions["trap"]["confidence"] = 0.8
        trap_wisdom = self.model._generate_divine_wisdom(predictions)
        self.assertIn("trap", trap_wisdom.lower())


if __name__ == '__main__':
    unittest.main() 