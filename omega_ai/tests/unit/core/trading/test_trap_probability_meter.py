import pytest
import sys
import os
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the module to test
from omega_ai.tools.trap_probability_meter import TrapProbabilityMeter

class TestTrapProbabilityMeter:
    """Test suite for TrapProbabilityMeter class"""
    
    def test_initialization(self):
        """Test basic initialization of TrapProbabilityMeter"""
        # Create an instance with default values
        meter = TrapProbabilityMeter()
        
        # Check instance attributes set correctly
        assert meter.interval == 5
        assert meter.debug is False
        assert meter.use_color is True
        assert meter.verbose is False
        assert meter.backtest_date is None
        assert meter.backtest_mode is False
        assert meter.header_style == 1
        
        # Check component initialization
        assert len(meter.components) == 6  # Should have 6 components
        for name, comp in meter.components.items():
            assert "weight" in comp
            assert "description" in comp
            assert "value" in comp
            assert "trend" in comp
    
    def test_get_current_btc_price_with_mock_redis(self, mock_redis_with_data):
        """Test _get_current_btc_price method with mock Redis data"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis_with_data):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis_with_data
            
            # Call the method
            price = meter._get_current_btc_price()
            
            # Check correct price returned
            assert price == 85000.0
    
    def test_get_volume_data_with_mock_redis(self, mock_redis_with_data):
        """Test _get_volume_data method with mock Redis data"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis_with_data):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis_with_data
            
            # Call the method
            current_volume, avg_volume = meter._get_volume_data()
            
            # Check correct volume returned
            assert current_volume == 120.5
            assert avg_volume > 0  # Should be an average of the history
    
    def test_get_price_movement_with_mock_redis(self, mock_redis_with_data):
        """Test _get_price_movement method with mock Redis data"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis_with_data):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis_with_data
            
            # Call the method
            short_term, medium_term = meter._get_price_movement()
            
            # We can't assert exact values as they depend on random data,
            # but we can check they are within expected range
            assert isinstance(short_term, float)
            assert isinstance(medium_term, float)
            # Typical ranges would be between -0.1 and 0.1 for these values
            assert -0.5 <= short_term <= 0.5
            assert -0.5 <= medium_term <= 0.5

    def test_detect_volume_spike(self, mock_redis_with_data):
        """Test volume spike detection with mock Redis data"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis_with_data):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis_with_data
            
            # Inject a volume spike
            mock_redis_with_data.set("last_btc_volume", "500")  # Much higher than average
            
            # Call the method
            probability, description = meter._detect_volume_spike()
            
            # Check results
            assert 0.0 <= probability <= 1.0
            assert "above average" in description.lower() or "high" in description.lower()
    
    def test_analyze_price_pattern(self, mock_redis_with_data):
        """Test price pattern analysis with mock Redis data"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis_with_data):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis_with_data
            
            # Call the method
            probability, description = meter._analyze_price_pattern()
            
            # Check results
            assert 0.0 <= probability <= 1.0
            assert isinstance(description, str)
    
    def test_check_fibonacci_match(self, mock_redis_with_data):
        """Test Fibonacci level matching with mock Redis data"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis_with_data):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis_with_data
            
            # Call the method with current price
            price = float(mock_redis_with_data.get("last_btc_price"))
            probability, description = meter._check_fibonacci_match(price)
            
            # Check results
            assert 0.0 <= probability <= 1.0
            assert isinstance(description, str)
    
    def test_detect_likely_trap_type(self, mock_redis_with_data):
        """Test trap type detection with mock Redis data"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis_with_data):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis_with_data
            
            # Call the method
            trap_type, confidence = meter._detect_likely_trap_type()
            
            # Check results
            assert isinstance(trap_type, str) or trap_type is None
            assert 0.0 <= confidence <= 1.0
    
    def test_calculate_probability(self, mock_redis_with_data):
        """Test overall probability calculation with mock Redis data"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis_with_data):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis_with_data
            
            # Call the method
            probability = meter._calculate_probability()
            
            # Check result
            assert 0.0 <= probability <= 1.0
            
            # Check that components have been updated
            for comp_name, comp_data in meter.components.items():
                assert 0.0 <= comp_data["value"] <= 1.0
    
    def test_store_trap_prediction(self, mock_redis):
        """Test storing trap predictions to Redis"""
        # Create meter with mock Redis
        with patch('redis.Redis', return_value=mock_redis):
            meter = TrapProbabilityMeter()
            meter.redis_client = mock_redis
            
            # Set up a high probability and confidence
            meter.probability = 0.8
            trap_type = "Bull Trap"
            confidence = 0.75
            
            # Call the method
            meter._store_trap_prediction(trap_type, meter.probability, confidence)
            
            # Check Redis was updated
            assert mock_redis.exists("trap_predictions") == 1
            assert mock_redis.exists("latest_trap_prediction") == 1
            
            # Check data was stored correctly
            latest_prediction = json.loads(mock_redis.get("latest_trap_prediction"))
            assert latest_prediction["type"] == trap_type
            assert latest_prediction["probability"] == meter.probability
            assert latest_prediction["confidence"] == confidence
    
    def test_update_trend(self):
        """Test trend calculation based on probability history"""
        meter = TrapProbabilityMeter()
        
        # Test increasing trend
        meter.probability_history = []
        meter._update_trend(0.3)  # Add first data point
        meter._update_trend(0.4)  # Add second data point with increase
        assert "increasing" in meter.trend
        
        # Test decreasing trend
        meter.probability_history = []
        meter._update_trend(0.7)  # Add first data point
        meter._update_trend(0.6)  # Add second data point with decrease
        assert "decreasing" in meter.trend
        
        # Test stable trend
        meter.probability_history = []
        meter._update_trend(0.5)  # Add first data point
        meter._update_trend(0.5)  # Add second data point with no change
        assert meter.trend == "stable"
    
    def test_draw_progress_bar(self):
        """Test progress bar rendering"""
        meter = TrapProbabilityMeter()
        
        # Test 0% progress
        bar = meter._draw_progress_bar(0.0, width=10)
        assert bar == "░░░░░░░░░░"
        
        # Test 50% progress
        bar = meter._draw_progress_bar(0.5, width=10)
        assert bar == "█████░░░░░"
        
        # Test 100% progress
        bar = meter._draw_progress_bar(1.0, width=10)
        assert bar == "██████████"
    
    def test_color_methods(self):
        """Test color handling methods"""
        # Test with colors enabled
        meter = TrapProbabilityMeter(use_color=True)
        colored_text = meter._color("Test", "\033[31m")  # Red
        assert colored_text == "\033[31mTest\033[0m"
        
        # Test with colors disabled
        meter = TrapProbabilityMeter(use_color=False)
        plain_text = meter._color("Test", "\033[31m")  # Red
        assert plain_text == "Test" 