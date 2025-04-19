
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
import sys
import os
import json
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timezone

# Set up path for imports
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import module to test
from omega_ai.ml.market_trends_model import MarketTrendsModel

class TestMarketTrendsAIModel(unittest.TestCase):
    """Test cases for the Market Trends AI Model"""

    def setUp(self):
        """Set up test environment"""
        # Mock Redis
        self.redis_patcher = patch('redis.StrictRedis')
        self.mock_redis = self.redis_patcher.start()
        self.mock_redis_instance = MagicMock()
        self.mock_redis.return_value = self.mock_redis_instance
        
        # Mock joblib.load
        self.joblib_load_patcher = patch('joblib.load')
        self.mock_joblib_load = self.joblib_load_patcher.start()
        
        # Mock models
        self.mock_trend_classifier = MagicMock()
        self.mock_price_regressor = MagicMock()
        self.mock_trap_classifier = MagicMock()
        
        # Set up model mock returns
        self.mock_joblib_load.side_effect = lambda path: {
            os.path.join('omega_ai/ml/models', 'trend_classifier.joblib'): self.mock_trend_classifier,
            os.path.join('omega_ai/ml/models', 'price_regressor.joblib'): self.mock_price_regressor,
            os.path.join('omega_ai/ml/models', 'trap_classifier.joblib'): self.mock_trap_classifier
        }.get(path, None)
        
        # Mock model predictions
        self.mock_trend_classifier.predict.return_value = np.array([1])  # 1 = Bullish
        self.mock_trend_classifier.predict_proba.return_value = np.array([[0.1, 0.8, 0.1]])
        self.mock_price_regressor.predict.return_value = np.array([0.6])  # Scaled price
        self.mock_trap_classifier.predict.return_value = np.array([0])  # 0 = No trap
        self.mock_trap_classifier.predict_proba.return_value = np.array([[0.9, 0.1]])
        
        # Set up feature names for model validation
        self.mock_trend_classifier.feature_names_in_ = np.array(['price', 'volume', 'change_1min', 'change_5min'])
        self.mock_price_regressor.feature_names_in_ = np.array(['price', 'volume', 'change_1min', 'change_5min'])
        self.mock_trap_classifier.feature_names_in_ = np.array(['price', 'volume', 'change_1min', 'change_5min'])
        
        # Initialize model for testing
        with patch('os.makedirs'):
            with patch('os.path.exists', return_value=True):
                self.model = MarketTrendsModel(redis_host='localhost', redis_port=6379)
                
        # Mock price scaler
        self.model.price_scaler.transform = MagicMock(return_value=np.array([[0.5]]))
        self.model.price_scaler.inverse_transform = MagicMock(return_value=np.array([[85000.0]]))

    def tearDown(self):
        """Clean up after tests"""
        self.redis_patcher.stop()
        self.joblib_load_patcher.stop()

    @patch('pandas.DataFrame')
    def test_get_latest_data_success(self, mock_df):
        """Test getting latest data for prediction when all data is available"""
        # Mock Redis data
        self.mock_redis_instance.get.side_effect = lambda key: {
            'last_btc_price': '60000.0',
            'last_btc_volume': '1000.0',
            'btc_trend_1min': json.dumps({
                'trend': 'Bullish',
                'change': 0.5,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }),
            'btc_trend_5min': json.dumps({
                'trend': 'Strongly Bullish',
                'change': 1.5,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        }.get(key)
        
        # Mock DataFrame
        mock_df_instance = pd.DataFrame({
            'price': [60000.0],
            'volume': [1000.0],
            'trend_1min': [1],  # 1 = Bullish
            'change_1min': [0.5],
            'trend_5min': [2],  # 2 = Strongly Bullish
            'change_5min': [1.5]
        })
        mock_df.return_value = mock_df_instance
        
        # Mock get_historical_data
        with patch.object(self.model, 'get_historical_data', return_value=pd.DataFrame()):
            # Test
            result = self.model.get_latest_data()
            
            # Assertions
            self.assertIsInstance(result, pd.DataFrame)
            self.assertFalse(result.empty)
            
    def test_get_latest_data_missing_price(self):
        """Test getting latest data when price data is missing"""
        # Mock Redis data - missing price
        self.mock_redis_instance.get.return_value = None
        
        # Test
        result = self.model.get_latest_data()
        
        # Assertions
        self.assertTrue(result.empty)
        
    def test_predict_trend_success(self):
        """Test trend prediction when model and data are available"""
        # Mock get_latest_data
        mock_df = pd.DataFrame({
            'price': [60000.0],
            'volume': [1000.0],
            'change_1min': [0.5],
            'change_5min': [1.5]
        })
        with patch.object(self.model, 'get_latest_data', return_value=mock_df):
            # Test
            result = self.model.predict_trend()
            
            # Assertions
            self.assertEqual(result['trend'], 'Bullish')
            self.assertAlmostEqual(result['confidence'], 0.8)
            
    def test_predict_trend_no_model(self):
        """Test trend prediction when model is not available"""
        # Set model to None
        self.model.trend_classifier = None
        
        # Test
        result = self.model.predict_trend()
        
        # Assertions
        self.assertEqual(result['trend'], 'Unknown')
        self.assertEqual(result['confidence'], 0.0)
        
    def test_predict_trend_no_data(self):
        """Test trend prediction when data is not available"""
        # Mock get_latest_data to return empty DataFrame
        with patch.object(self.model, 'get_latest_data', return_value=pd.DataFrame()):
            # Test
            result = self.model.predict_trend()
            
            # Assertions
            self.assertEqual(result['trend'], 'Unknown')
            self.assertEqual(result['confidence'], 0.0)
            
    def test_predict_price_success(self):
        """Test price prediction when model and data are available"""
        # Mock get_latest_data
        mock_df = pd.DataFrame({
            'price': [60000.0],
            'volume': [1000.0],
            'change_1min': [0.5],
            'change_5min': [1.5]
        })
        with patch.object(self.model, 'get_latest_data', return_value=mock_df):
            # Test
            result = self.model.predict_price()
            
            # Assertions
            self.assertEqual(result['price'], 85000.0)
            self.assertEqual(result['current_price'], 60000.0)
            self.assertAlmostEqual(result['pct_change'], 41.67, places=2)
            
    def test_predict_mm_trap_success(self):
        """Test MM trap prediction when model and data are available"""
        # Mock get_latest_data
        mock_df = pd.DataFrame({
            'price': [60000.0],
            'volume': [1000.0],
            'change_1min': [0.5],
            'change_5min': [1.5]
        })
        with patch.object(self.model, 'get_latest_data', return_value=mock_df):
            # Test
            result = self.model.predict_mm_trap()
            
            # Assertions
            self.assertEqual(result['trap_detected'], False)
            self.assertAlmostEqual(result['confidence'], 0.9)
            
    def test_generate_predictions_all_components(self):
        """Test generating all predictions when all components are available"""
        # Mock individual prediction methods
        with patch.object(self.model, 'predict_trend', return_value={'trend': 'Bullish', 'confidence': 0.8}):
            with patch.object(self.model, 'predict_price', return_value={
                'price': 65000.0,
                'current_price': 60000.0,
                'pct_change': 8.33,
                'confidence': 0.7
            }):
                with patch.object(self.model, 'predict_mm_trap', return_value={
                    'trap_detected': False,
                    'confidence': 0.9
                }):
                    # Test
                    result = self.model.generate_predictions()
                    
                    # Assertions
                    self.assertIn('trend', result)
                    self.assertIn('price', result)
                    self.assertIn('trap', result)
                    self.assertIn('divine_wisdom', result)
                    self.assertEqual(result['trend']['trend'], 'Bullish')
                    self.assertEqual(result['price']['price'], 65000.0)
                    self.assertEqual(result['trap']['trap_detected'], False)
                    
    def test_calculate_harmony_score(self):
        """Test calculation of Fibonacci harmony score"""
        # Mock predictions
        predictions = {
            'trend': {'trend': 'Bullish', 'confidence': 0.8},
            'price': {
                'price': 65000.0,
                'current_price': 60000.0,
                'pct_change': 8.33,
                'confidence': 0.7
            },
            'trap': {'trap_detected': False, 'confidence': 0.9}
        }
        
        # Test
        score = self.model._calculate_harmony_score(predictions)
        
        # Assertions - score should be between 0 and 1
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        
    def test_encode_trend(self):
        """Test encoding of trend string to integer"""
        # Test various trend values
        self.assertEqual(self.model._encode_trend('Strongly Bullish'), 2)
        self.assertEqual(self.model._encode_trend('Bullish'), 1)
        self.assertEqual(self.model._encode_trend('Neutral'), 0)
        self.assertEqual(self.model._encode_trend('Bearish'), -1)
        self.assertEqual(self.model._encode_trend('Strongly Bearish'), -2)
        self.assertEqual(self.model._encode_trend('Unknown'), 0)  # Default to neutral

if __name__ == '__main__':
    unittest.main() 