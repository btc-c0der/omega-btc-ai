
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
from unittest.mock import patch, MagicMock, call
import sys
import os
import json

# Add the project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

class TestMarketTrendsAIIntegration(unittest.TestCase):
    """Test the integration between the market trends monitor and AI predictions."""

    def test_ai_predictions_integration(self):
        """Test that AI predictions are properly integrated with market trends monitor."""
        # Create a direct test for the _generate_divine_wisdom method
        from omega_ai.ml.market_trends_model import MarketTrendsModel

        # Create the model with patched Redis
        with patch('omega_ai.ml.market_trends_model.redis.StrictRedis') as mock_redis:
            redis_instance = MagicMock()
            mock_redis.return_value = redis_instance
            
            model = MarketTrendsModel()
            
            # Create test predictions
            predictions = {
                "timestamp": "2023-03-24T12:00:00Z",
                "trend": {"trend": "Bullish", "confidence": 0.85},
                "price": {
                    "price": 55000.0,
                    "current_price": 50000.0,
                    "pct_change": 10.0,
                    "confidence": 0.75
                },
                "trap": {
                    "trap_detected": True,
                    "trap_type": "Bull Trap",
                    "confidence": 0.9
                }
            }
            
            # Make sure store combined predictions works
            model.redis_conn = redis_instance
            model.redis_conn.set("ai_predictions", json.dumps(predictions))
            
            # Test the divine wisdom generation
            wisdom = model._generate_divine_wisdom(predictions)
            
            # Validate trap_conf usage
            self.assertIn("trap", wisdom.lower())
            
            # Test with different trap confidence
            predictions["trap"]["confidence"] = 0.4
            wisdom = model._generate_divine_wisdom(predictions)
            
            # With lower confidence, the trap message should change
            self.assertNotIn("the market appears to be setting a", wisdom.lower())

    @patch('builtins.print')
    def test_market_trends_display_with_ai(self, mock_print):
        """Test that market trends display includes AI predictions with proper formatting."""
        # Import here to avoid circular imports during patching
        from omega_ai.ml.market_trends_model import MarketTrendsModel
        
        # Create model and mock its dependencies
        with patch('omega_ai.ml.market_trends_model.redis.StrictRedis'):
            model = MarketTrendsModel()
            
            # Mock prediction methods
            model.predict_trend = MagicMock(return_value={"trend": "Bearish", "confidence": 0.9})
            model.predict_price = MagicMock(return_value={
                "price": 45000.0,
                "current_price": 50000.0,
                "pct_change": -10.0,
                "confidence": 0.8
            })
            model.predict_mm_trap = MagicMock(return_value={
                "trap_detected": True,
                "trap_type": "Bear Trap",
                "confidence": 0.75
            })
            
            # Generate predictions
            predictions = model.generate_predictions()
            
            # Display predictions
            model.display_predictions(predictions)
            
            # Verify important display components were printed
            calls = [call for call in mock_print.call_args_list]
            printed_text = "".join(str(call) for call in calls)
            
            # Check that key elements are displayed
            self.assertIn("AI MODEL PREDICTIONS", printed_text)
            self.assertIn("TREND PREDICTION", printed_text) 
            self.assertIn("Bearish", printed_text)
            self.assertIn("PRICE PREDICTION", printed_text)
            self.assertIn("TRAP PREDICTION", printed_text)
            self.assertIn("TRAP DETECTED", printed_text)
            self.assertIn("Bear Trap", printed_text)
            self.assertIn("FIBONACCI HARMONY SCORE", printed_text)

    @patch('omega_ai.ml.market_trends_model.redis.StrictRedis')
    def test_trap_conf_variable_usage(self, mock_redis):
        """Test that trap_conf variable is properly used in divine wisdom generation."""
        # Import here to avoid circular imports during patching
        from omega_ai.ml.market_trends_model import MarketTrendsModel
        
        # Create model and mock Redis
        redis_instance = MagicMock()
        mock_redis.return_value = redis_instance
        model = MarketTrendsModel()
        
        # Test case with high confidence trap
        predictions = {
            "trend": {"trend": "Bullish", "confidence": 0.9},
            "price": {"price": 55000, "current_price": 50000, "pct_change": 10.0, "confidence": 0.8},
            "trap": {"trap_detected": True, "trap_type": "Bull Trap", "confidence": 0.85}
        }
        
        wisdom = model._generate_divine_wisdom(predictions)
        
        # With high confidence trap, should mention the trap
        self.assertIn("trap", wisdom.lower())
        
        # Test with low confidence trap - should not affect wisdom
        predictions["trap"]["confidence"] = 0.3
        wisdom = model._generate_divine_wisdom(predictions)
        
        # With low confidence trap, should not mention trap
        self.assertNotIn("the market appears to be setting a", wisdom.lower())

if __name__ == '__main__':
    unittest.main() 