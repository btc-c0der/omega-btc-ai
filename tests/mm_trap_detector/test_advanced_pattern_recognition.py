import pytest
import numpy as np
import json
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

# Direct import to avoid issues with module attributes
from omega_ai.mm_trap_detector.advanced_pattern_recognition import (
    AdvancedPatternRecognition,
    TrapPattern,
    PatternConfidence
)


# ---- Test Data Generators ----

def generate_price_series(base_price=80000, length=100, noise_level=200, trend=0):
    """Generate a realistic price series with noise for testing patterns."""
    # Create base time series with trend
    x = np.linspace(0, 1, length)
    trend_component = trend * x * base_price / 100  # Percentage trend
    
    # Add noise
    noise = np.random.normal(0, noise_level, length)
    
    # Combine components
    prices = base_price + trend_component + noise
    
    return prices


def generate_pattern_data(pattern_type="double_bottom", base_price=80000):
    """Generate specific pattern data for testing pattern recognition."""
    if pattern_type == "double_bottom":
        # Generate a double bottom pattern (W shape)
        prices = []
        prices.extend(generate_price_series(base_price, 20, 100, -5))  # Initial downtrend
        prices.extend(generate_price_series(base_price * 0.97, 15, 80, 3))  # First bottom and bounce
        prices.extend(generate_price_series(base_price * 0.99, 15, 80, -3))  # Second decline
        prices.extend(generate_price_series(base_price * 0.97, 15, 80, 6))  # Second bottom and stronger bounce
        return np.array(prices)
        
    elif pattern_type == "head_and_shoulders":
        # Generate a head and shoulders pattern (M shape with middle peak higher)
        prices = []
        prices.extend(generate_price_series(base_price, 15, 100, 3))  # Initial uptrend
        prices.extend(generate_price_series(base_price * 1.03, 10, 80, -2))  # First shoulder and decline
        prices.extend(generate_price_series(base_price * 1.02, 15, 100, 5))  # Head formation (higher peak)
        prices.extend(generate_price_series(base_price * 1.05, 10, 80, -4))  # Decline from head
        prices.extend(generate_price_series(base_price * 1.02, 15, 100, 2))  # Second shoulder formation
        prices.extend(generate_price_series(base_price * 1.03, 10, 80, -3))  # Final decline (breakdown)
        return np.array(prices)
        
    elif pattern_type == "bull_flag":
        # Generate a bull flag pattern (uptrend, then small consolidation)
        prices = []
        prices.extend(generate_price_series(base_price, 20, 100, 8))  # Strong uptrend (flag pole)
        # Consolidation period (flag) with slight downward drift
        flag_base = base_price * 1.08
        prices.extend(generate_price_series(flag_base, 5, 50, -0.5))
        prices.extend(generate_price_series(flag_base * 0.99, 5, 50, -0.3))
        prices.extend(generate_price_series(flag_base * 0.98, 5, 50, -0.2))
        prices.extend(generate_price_series(flag_base * 0.97, 5, 50, 0.1))
        return np.array(prices)
        
    else:
        # Default to random noise around base price
        return generate_price_series(base_price, 50, 200, 0)


# ---- Fixtures ----

@pytest.fixture
def mock_redis():
    """Mock Redis connection with appropriate methods."""
    mock = MagicMock()
    mock.get.return_value = "80000"
    mock.lrange.return_value = ["79800,120", "80100,130", "80050,115", "79950,140"]
    return mock


@pytest.fixture
def pattern_recognizer(mock_redis):
    """Create a pattern recognizer with mocked dependencies."""
    with patch('redis.Redis', return_value=mock_redis):
        # Create analyzer with test settings
        recognizer = AdvancedPatternRecognition(
            base_confidence_threshold=0.6,
            debug_mode=True
        )
        
        # Use our mock Redis connection
        recognizer.redis = mock_redis
        
        return recognizer


# ---- Test Class ----

class TestAdvancedPatternRecognition:
    """Tests for the Advanced Pattern Recognition module."""
    
    def test_initialization(self, pattern_recognizer):
        """Test recognizer initializes with proper settings."""
        assert pattern_recognizer.base_confidence_threshold == 0.6
        assert pattern_recognizer.debug_mode is True
        assert pattern_recognizer.min_pattern_window == 5
        assert pattern_recognizer.max_pattern_window == 100
    
    @patch('redis.Redis')
    def test_redis_connection_error(self, mock_redis_cls):
        """Test handling Redis connection errors."""
        # Arrange - simulate Redis connection failure
        mock_redis_cls.side_effect = Exception("Connection failed")
        
        # Act & Assert - initialization should still succeed, with warnings
        with pytest.warns(UserWarning, match="Redis connection failed"):
            recognizer = AdvancedPatternRecognition()
            
        # Should have a flag indicating Redis is unavailable
        assert recognizer.redis_available is False
    
    def test_get_price_data_success(self, pattern_recognizer, mock_redis):
        """Test successfully retrieving price data."""
        # Arrange
        mock_redis.lrange.return_value = [
            "80100,150", "80200,160", "80150,155", "80300,170", "80250,165"
        ]
        
        # Act
        prices, volumes = pattern_recognizer.get_price_data(timeframe="5min", limit=5)
        
        # Assert
        assert len(prices) == 5
        assert len(volumes) == 5
        assert prices[0] == 80100
        assert volumes[0] == 150
        mock_redis.lrange.assert_called_once()
    
    def test_get_price_data_with_redis_error(self, pattern_recognizer, mock_redis):
        """Test error handling when Redis fails during price retrieval."""
        # Arrange
        mock_redis.lrange.side_effect = Exception("Redis error")
        
        # Act
        prices, volumes = pattern_recognizer.get_price_data(timeframe="5min", limit=5)
        
        # Assert - should return empty arrays on error
        assert len(prices) == 0
        assert len(volumes) == 0
    
    def test_detect_double_bottom_pattern(self, pattern_recognizer):
        """Test detection of double bottom pattern."""
        # Arrange
        prices = generate_pattern_data("double_bottom")
        pattern_recognizer.get_price_data = MagicMock(return_value=(prices, []))
        
        # Act
        patterns = pattern_recognizer.detect_patterns(timeframe="15min")
        
        # Assert
        # At least one pattern should be detected
        assert len(patterns) > 0
        # Find double bottom in detected patterns
        double_bottom_patterns = [p for p in patterns if p.pattern_type == "double_bottom"]
        assert len(double_bottom_patterns) > 0
        # The confidence should be reasonably high
        assert double_bottom_patterns[0].confidence > 0.6
    
    def test_detect_head_and_shoulders_pattern(self, pattern_recognizer):
        """Test detection of head and shoulders pattern."""
        # Arrange
        prices = generate_pattern_data("head_and_shoulders")
        pattern_recognizer.get_price_data = MagicMock(return_value=(prices, []))
        
        # Act
        patterns = pattern_recognizer.detect_patterns(timeframe="15min")
        
        # Assert
        # Find head and shoulders in detected patterns
        hs_patterns = [p for p in patterns if p.pattern_type == "head_and_shoulders"]
        assert len(hs_patterns) > 0
        # The confidence should be reasonably high
        assert hs_patterns[0].confidence > 0.6
    
    def test_detect_bull_flag_pattern(self, pattern_recognizer):
        """Test detection of bull flag pattern."""
        # Arrange
        prices = generate_pattern_data("bull_flag")
        pattern_recognizer.get_price_data = MagicMock(return_value=(prices, []))
        
        # Act
        patterns = pattern_recognizer.detect_patterns(timeframe="15min")
        
        # Assert
        # Find bull flag in detected patterns
        bull_flag_patterns = [p for p in patterns if p.pattern_type == "bull_flag"]
        assert len(bull_flag_patterns) > 0
        # The confidence should be reasonably high
        assert bull_flag_patterns[0].confidence > 0.6
    
    def test_detect_patterns_with_empty_data(self, pattern_recognizer):
        """Test pattern detection with empty price data."""
        # Arrange
        pattern_recognizer.get_price_data = MagicMock(return_value=([], []))
        
        # Act
        patterns = pattern_recognizer.detect_patterns(timeframe="15min")
        
        # Assert
        assert len(patterns) == 0  # No patterns should be detected
    
    def test_detect_patterns_with_insufficient_data(self, pattern_recognizer):
        """Test pattern detection with insufficient data points."""
        # Arrange - only 3 data points, below minimum
        prices = [80000, 80100, 80050]
        pattern_recognizer.get_price_data = MagicMock(return_value=(prices, []))
        
        # Act
        patterns = pattern_recognizer.detect_patterns(timeframe="15min")
        
        # Assert
        assert len(patterns) == 0  # No patterns should be detected
    
    def test_calculate_pattern_probability(self, pattern_recognizer):
        """Test calculation of pattern probability."""
        # Arrange
        # Create a strong double bottom pattern
        prices = generate_pattern_data("double_bottom")
        
        # Act - set window size to match the pattern
        probability = pattern_recognizer.calculate_pattern_probability(
            prices, "double_bottom", window_size=len(prices)
        )
        
        # Assert
        assert probability > 0.6  # Should have high probability for clean pattern
    
    def test_get_pattern_description(self, pattern_recognizer):
        """Test getting human-readable pattern descriptions."""
        # Act
        description1 = pattern_recognizer.get_pattern_description("double_bottom")
        description2 = pattern_recognizer.get_pattern_description("head_and_shoulders")
        description3 = pattern_recognizer.get_pattern_description("unknown_pattern")
        
        # Assert
        assert "bottom" in description1.lower()
        assert "reversal" in description1.lower()
        
        assert "shoulders" in description2.lower()
        assert "reversal" in description2.lower()
        
        assert "unknown" in description3.lower()
    
    def test_calculate_confidence_threshold(self, pattern_recognizer):
        """Test dynamic confidence threshold calculation."""
        # Arrange
        # Mock volatility data
        mock_redis = pattern_recognizer.redis
        mock_redis.get.side_effect = lambda key: {
            "volatility_1h": "1.2",  # High volatility 
            "last_btc_price": "82000"
        }.get(key, None)
        
        # Act
        threshold = pattern_recognizer.calculate_confidence_threshold()
        
        # Assert
        # Higher volatility should increase the threshold
        assert threshold > pattern_recognizer.base_confidence_threshold
        
        # Change to low volatility
        mock_redis.get.side_effect = lambda key: {
            "volatility_1h": "0.3",  # Low volatility
            "last_btc_price": "82000"
        }.get(key, None)
        
        # Act again
        low_vol_threshold = pattern_recognizer.calculate_confidence_threshold()
        
        # Assert
        # Lower volatility should decrease the threshold
        assert low_vol_threshold < threshold
    
    def test_filter_low_confidence_patterns(self, pattern_recognizer):
        """Test filtering low confidence patterns."""
        # Arrange
        patterns = [
            TrapPattern("double_bottom", 0.8, "15min", "strong reversal"),
            TrapPattern("bull_flag", 0.5, "15min", "weak continuation"),
            TrapPattern("head_and_shoulders", 0.7, "15min", "moderate reversal"),
            TrapPattern("triangle", 0.4, "15min", "very weak continuation")
        ]
        
        # Set threshold to 0.6
        pattern_recognizer.base_confidence_threshold = 0.6
        
        # Act
        filtered_patterns = pattern_recognizer.filter_low_confidence_patterns(patterns)
        
        # Assert
        assert len(filtered_patterns) == 2  # Only patterns above 0.6 threshold
        assert filtered_patterns[0].pattern_type == "double_bottom"
        assert filtered_patterns[1].pattern_type == "head_and_shoulders"
    
    def test_analyze_market_conditions(self, pattern_recognizer, mock_redis):
        """Test market condition analysis."""
        # Arrange
        # Set up mock data for multiple timeframes
        mock_redis.lrange.side_effect = lambda key, start, end: {
            "btc_movements_5min": ["80000,100", "80100,110", "80300,120", "80400,130"],
            "btc_movements_15min": ["79800,100", "80000,110", "80200,120", "80400,130"],
            "btc_movements_1h": ["79000,100", "79500,110", "80000,120", "80500,130"]
        }.get(key, [])
        
        # Act
        conditions = pattern_recognizer.analyze_market_conditions()
        
        # Assert
        assert "trend" in conditions
        assert "volatility" in conditions
        assert "volume_profile" in conditions
        assert isinstance(conditions["trend"], dict)
        assert isinstance(conditions["volatility"], dict)
    
    def test_match_mm_trap_patterns(self, pattern_recognizer):
        """Test matching pattern types to potential MM trap types."""
        # Arrange
        patterns = [
            TrapPattern("double_bottom", 0.8, "15min", "strong reversal"),
            TrapPattern("head_and_shoulders", 0.7, "15min", "moderate reversal"),
            TrapPattern("bull_flag", 0.9, "15min", "strong continuation")
        ]
        
        # Act
        trap_candidates = pattern_recognizer.match_mm_trap_patterns(patterns)
        
        # Assert
        assert len(trap_candidates) >= 1
        # Head and shoulders is a classic trap pattern
        hs_traps = [t for t in trap_candidates if "head_and_shoulders" in t["pattern_type"]]
        assert len(hs_traps) > 0
        # The confidence should be transferred
        assert hs_traps[0]["confidence"] == 0.7
    
    @patch('omega_ai.mm_trap_detector.advanced_pattern_recognition.insert_possible_mm_trap')
    def test_report_potential_traps(self, mock_insert, pattern_recognizer):
        """Test reporting potential traps to the database."""
        # Arrange
        trap_candidates = [
            {
                "pattern_type": "head_and_shoulders",
                "trap_type": "Bearish Reversal Trap",
                "confidence": 0.85,
                "timeframe": "1h",
                "description": "Strong H&S pattern indicating potential reversal"
            },
            {
                "pattern_type": "double_top",
                "trap_type": "Double Top Trap",
                "confidence": 0.75,
                "timeframe": "15min",
                "description": "Clear double top formation"
            }
        ]
        
        # Act
        pattern_recognizer.report_potential_traps(trap_candidates)
        
        # Assert
        assert mock_insert.call_count == 2
        # Verify the trap data is correctly formatted
        call_args = mock_insert.call_args_list
        assert call_args[0][0][0]["type"] == "Bearish Reversal Trap"
        assert call_args[0][0][0]["confidence"] == 0.85
        assert call_args[1][0][0]["type"] == "Double Top Trap"
    
    @patch('omega_ai.mm_trap_detector.advanced_pattern_recognition.insert_possible_mm_trap')
    def test_scan_for_patterns(self, mock_insert, pattern_recognizer):
        """Test the main pattern scanning workflow."""
        # Arrange
        # Double bottom pattern
        prices = generate_pattern_data("double_bottom")
        pattern_recognizer.get_price_data = MagicMock(return_value=(prices, []))
        
        # Act
        result = pattern_recognizer.scan_for_patterns(timeframes=["15min"])
        
        # Assert
        assert result is True
        assert mock_insert.called
        
        # Test error handling
        pattern_recognizer.get_price_data.side_effect = Exception("Test error")
        result = pattern_recognizer.scan_for_patterns(timeframes=["15min"])
        
        # Should handle errors gracefully
        assert result is False 