import unittest
import pandas as pd
import numpy as np
from typing import Dict, List
from unittest.mock import Mock, patch, MagicMock
from gamon_trinity_predictor import GAMONTrinityPredictor

class TestGAMONTrinityPredictor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create mock models
        mock_hmm = Mock()
        mock_hmm.predict.return_value = pd.DataFrame({'state': [0] * 100})
        mock_hmm.model = Mock()
        mock_hmm.model.predict_proba.return_value = np.array([[0.7, 0.2, 0.1]] * 100)
        
        mock_eigenwave = Mock()
        mock_eigenwave.get_projections.return_value = pd.DataFrame(np.random.randn(100, 3))
        
        mock_cycle = Mock()
        mock_cycle.predict.return_value = pd.DataFrame({'state': [0] * 100})
        
        # Create predictor with mock models
        self.predictor = GAMONTrinityPredictor()
        self.predictor.hmm_mapper = mock_hmm
        self.predictor.eigenwave_detector = mock_eigenwave
        self.predictor.cycle_approximator = mock_cycle
        
        # Create sample test data with 100 days
        dates = pd.date_range(start='2023-01-01', end='2023-04-10', freq='D')
        np.random.seed(42)  # For reproducible test data
        
        # Generate more realistic price data with a trend and some volatility
        base_price = 30000
        trend = np.linspace(0, 5000, len(dates))  # Upward trend
        noise = np.random.randn(len(dates)) * 500  # Daily volatility
        
        close_prices = base_price + trend + noise
        high_prices = close_prices + np.abs(np.random.randn(len(dates)) * 200)
        low_prices = close_prices - np.abs(np.random.randn(len(dates)) * 200)
        open_prices = close_prices + np.random.randn(len(dates)) * 100
        volumes = np.random.randint(5000, 15000, size=len(dates))
        
        self.test_data = pd.DataFrame({
            'close': close_prices,
            'high': high_prices,
            'low': low_prices,
            'open': open_prices,
            'volume': volumes
        }, index=dates)

    def test_model_loading_failure(self):
        """Test handling of model loading failures."""
        # Create a predictor without models
        predictor = GAMONTrinityPredictor()
        
        # Mock the model loading to raise an exception
        with patch('gamon_trinity_predictor.PowerMethodBTCEigenwaves') as mock_eigenwave:
            mock_eigenwave.side_effect = Exception("Model loading failed")
            
            # This should not raise an exception
            predictor._load_models()
            
            # Verify that models are set to None
            self.assertIsNone(predictor.hmm_mapper)
            self.assertIsNone(predictor.eigenwave_detector)
            self.assertIsNone(predictor.cycle_approximator)

    def test_data_loading_failure(self):
        """Test handling of data loading failures."""
        # Mock yfinance.download to raise an exception
        with patch('yfinance.download', side_effect=Exception("Data download failed")):
            # This should not raise an exception
            try:
                from hmm_btc_state_mapper import load_btc_data
                load_btc_data(start_date="2020-01-01")
            except Exception as e:
                self.fail(f"Data loading should handle exceptions gracefully: {str(e)}")

    def test_prediction_with_missing_data(self):
        """Test prediction handling with missing or invalid data."""
        # Create data with missing values
        invalid_data = self.test_data.copy()
        invalid_data.loc[invalid_data.index[0], 'close'] = np.nan
        
        # This should not raise an exception
        try:
            predictions = self.predictor.predict_future_states(invalid_data)
            self.assertIsInstance(predictions, list)
        except Exception as e:
            self.fail(f"Prediction should handle missing data gracefully: {str(e)}")

    def test_visualization_with_invalid_data(self):
        """Test visualization handling with invalid prediction data."""
        # Create invalid predictions data
        invalid_predictions = [
            {
                'step': 1,
                'state': 'invalid',  # Invalid state type
                'confidence': 'invalid',  # Invalid confidence type
                'components': {
                    'hmm': {'state': 0, 'confidence': 0.7},
                    'eigenwave': {'state': 0, 'confidence': 0.8},
                    'cycle': {'state': 0, 'confidence': 0.9},
                    'volume': {'confidence': 0.6},
                    'volatility': {'confidence': 0.7}
                }
            }
        ]
        
        # Mock plotly.graph_objects.Figure.show
        with patch('plotly.graph_objects.Figure.show') as mock_show:
            # This should not raise an exception
            try:
                GAMONTrinityPredictor.plot_predictions(invalid_predictions)
            except Exception as e:
                self.fail(f"Visualization should handle invalid data gracefully: {str(e)}")

    def test_plot_predictions_static_method(self):
        """Test that plot_predictions works as a static method with correct input type."""
        # Create sample predictions list
        sample_predictions = [
            {
                'step': 1,
                'state': 0,
                'confidence': 0.8,
                'components': {
                    'hmm': {'state': 0, 'confidence': 0.7},
                    'eigenwave': {'state': 0, 'confidence': 0.8},
                    'cycle': {'state': 0, 'confidence': 0.9},
                    'volume': {'confidence': 0.6},
                    'volatility': {'confidence': 0.7}
                }
            }
        ]
        
        # Mock plotly.graph_objects.Figure.show
        with patch('plotly.graph_objects.Figure.show') as mock_show:
            # This should not raise a TypeError
            try:
                GAMONTrinityPredictor.plot_predictions(sample_predictions)
            except Exception as e:
                self.fail(f"plot_predictions raised {type(e).__name__} unexpectedly!")
            
            # Verify that show was called
            mock_show.assert_called_once()

    def test_predictions_dictionary_access(self):
        """Test that predictions can be accessed as a dictionary with string keys."""
        # Generate predictions
        predictions = self.predictor.predict_future_states(self.test_data)
        
        # Test that predictions is a list of dictionaries
        self.assertIsInstance(predictions, list)
        self.assertTrue(all(isinstance(pred, dict) for pred in predictions))
        
        # Test accessing dictionary keys that were causing linter errors
        for pred in predictions:
            # Test component access
            self.assertIn('components', pred)
            components = pred['components']
            
            # Test HMM component
            self.assertIn('hmm', components)
            hmm_pred = components['hmm']
            self.assertIn('state', hmm_pred)
            self.assertIn('confidence', hmm_pred)
            
            # Test cycle component
            self.assertIn('cycle', components)
            cycle_pred = components['cycle']
            self.assertIn('state', cycle_pred)
            self.assertIn('confidence', cycle_pred)

    def test_plot_predictions_class_method(self):
        """Test that plot_predictions works as a class method."""
        predictions = self.predictor.predict_future_states(self.test_data)
        
        # Mock plotly.graph_objects.Figure.show
        with patch('plotly.graph_objects.Figure.show') as mock_show:
            # This should not raise an AttributeError
            try:
                self.predictor.plot_predictions(predictions)
            except Exception as e:
                self.fail(f"plot_predictions raised {type(e).__name__} unexpectedly!")
            
            # Verify that show was called
            mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main() 