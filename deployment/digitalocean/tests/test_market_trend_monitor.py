"""
Test suite for the OMEGA Market Trend Monitor.
Tests the market analysis functionality and trend detection capabilities.
"""

import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Union, TypedDict, cast, TypeVar, Generic, Type, TypeGuard, Sequence, TypeAlias, Protocol, runtime_checkable, TypeVarTuple, Unpack
from deployment.digitalocean.monitor.omega_market_trend_monitor import OmegaMarketTrendMonitor
from deployment.digitalocean.logging.omega_logger import OmegaLogger
from deployment.digitalocean.utils.redis_manager import RedisManager
import numpy as np

T = TypeVar('T')
Ts = TypeVarTuple('Ts')

PriceHistory: TypeAlias = List[Dict[str, Any]]
PriceList: TypeAlias = List[float]

@runtime_checkable
class TrinityMatrixProtocol(Protocol):
    """Protocol for Trinity Matrix interface."""
    quantum_state: float
    energy_shift: float
    alignment_score: float
    temporal_data: List[Dict[str, Any]]
    
    def update_states(self, price_history: PriceList) -> None:
        """Update quantum states based on price history."""
        ...
    
    def calculate_alignment_score(self) -> float:
        """Calculate divine alignment score."""
        ...

class MarketAnalysis(TypedDict):
    """Type definition for market analysis results."""
    trend: str
    current_price: float
    fibonacci_levels: Dict[str, float]
    fibonacci_alignment: Optional[Dict[str, Any]]
    mm_trap: Optional[Dict[str, Any]]
    timestamp: str
    quantum_state: Optional[float]
    temporal_data: Optional[List[Dict[str, Any]]]
    energy_shift: Optional[float]
    trinity_states: Optional[Dict[str, Any]]

class SafeDict(Dict[str, Any]):
    """A dictionary that safely handles None values."""
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the dictionary, returning default if key doesn't exist or value is None."""
        value = super().get(key, default)
        return default if value is None else value

def is_not_none(value: Any) -> TypeGuard[Any]:
    """Type guard to check if a value is not None."""
    return value is not None

class TestMarketTrendMonitor(unittest.TestCase):
    """Test cases for the OMEGA Market Trend Monitor."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create sample history with clear trends
        self.bullish_history = [
            {"timestamp": "2024-03-27T00:00:00", "price": 50000.0},
            {"timestamp": "2024-03-27T01:00:00", "price": 51000.0},
            {"timestamp": "2024-03-27T02:00:00", "price": 52000.0},
            {"timestamp": "2024-03-27T03:00:00", "price": 53000.0},
            {"timestamp": "2024-03-27T04:00:00", "price": 54000.0}
        ]
        
        self.bearish_history = [
            {"timestamp": "2024-03-27T00:00:00", "price": 54000.0},
            {"timestamp": "2024-03-27T01:00:00", "price": 53000.0},
            {"timestamp": "2024-03-27T02:00:00", "price": 52000.0},
            {"timestamp": "2024-03-27T03:00:00", "price": 51000.0},
            {"timestamp": "2024-03-27T04:00:00", "price": 50000.0}
        ]
        
        self.neutral_history = [
            {"timestamp": "2024-03-27T00:00:00", "price": 50000.0},
            {"timestamp": "2024-03-27T01:00:00", "price": 50100.0},
            {"timestamp": "2024-03-27T02:00:00", "price": 49900.0},
            {"timestamp": "2024-03-27T03:00:00", "price": 50200.0},
            {"timestamp": "2024-03-27T04:00:00", "price": 50000.0}
        ]
        
        # Default to neutral history
        self.sample_history = self.neutral_history.copy()
        
        # Create mock objects
        self.redis_mock = Mock(spec=RedisManager)
        self.redis_mock.get_price_history.return_value = self.sample_history
        self.redis_mock.get_current_price.return_value = 50000.0
        
        self.logger_mock = Mock(spec=OmegaLogger)
        self.logger_mock.log_info.return_value = None
        self.logger_mock.log_error.return_value = None
        self.logger_mock.log_warning.return_value = None
        
        self.monitor = OmegaMarketTrendMonitor(
            redis_manager=self.redis_mock,
            logger=self.logger_mock,
            analysis_interval=3600,
            use_ai=True,
            quantum_mode=True
        )
        
        # Create AI model mock
        self.ai_mock = Mock()
        self.ai_mock.predict_trend.return_value = ("neutral", 0.7)
        self.ai_mock.predict_price.return_value = (50100.0, 0.8)
        self.ai_mock.predict_trap_probability.return_value = 0.5
        self.ai_mock.generate_market_insight.return_value = {
            "insight": "Market showing consolidation",
            "confidence": 0.7,
            "factors": ["Price stable", "No clear direction"]
        }
        
        # Assign AI mock
        self.monitor.ai_model = self.ai_mock
    
    def test_initialization(self):
        """Test monitor initialization with default parameters."""
        self.assertEqual(self.monitor.analysis_interval, 3600)
        self.assertTrue(self.monitor.use_ai)
        self.assertTrue(self.monitor.quantum_mode)
        self.assertEqual(self.monitor.consecutive_errors, 0)
        self.assertIsNotNone(self.monitor.redis_manager)
        self.assertIsNotNone(self.monitor.logger)
        self.assertIsNotNone(self.monitor.ai_model)
        self.assertIsNotNone(self.monitor.trinity_matrix)
    
    def test_analyze_price_trend_bullish(self):
        """Test price trend analysis for bullish market."""
        # Set bullish history
        self.redis_mock.get_price_history.return_value = self.bullish_history
        self.redis_mock.get_current_price.return_value = 54000.0
        self.ai_mock.predict_trend.return_value = ("bullish", 0.9)
        
        analysis = self.monitor.analyze_market()
        self.assertIsNotNone(analysis)
        analysis_dict = SafeDict(cast(MarketAnalysis, analysis))
        trend = analysis_dict.get("trend", "Unknown")
        self.assertEqual(trend, "Strongly Bullish")
    
    def test_analyze_price_trend_bearish(self):
        """Test price trend analysis for bearish market."""
        # Set bearish history
        self.redis_mock.get_price_history.return_value = self.bearish_history
        self.redis_mock.get_current_price.return_value = 50000.0
        self.ai_mock.predict_trend.return_value = ("bearish", 0.9)
        
        analysis = self.monitor.analyze_market()
        self.assertIsNotNone(analysis)
        analysis_dict = SafeDict(cast(MarketAnalysis, analysis))
        trend = analysis_dict.get("trend", "Unknown")
        self.assertEqual(trend, "Strongly Bearish")
    
    def test_analyze_price_trend_neutral(self):
        """Test price trend analysis for neutral market."""
        # Set neutral history
        self.redis_mock.get_price_history.return_value = self.neutral_history
        self.redis_mock.get_current_price.return_value = 50000.0
        self.ai_mock.predict_trend.return_value = ("neutral", 0.7)
        
        analysis = self.monitor.analyze_market()
        self.assertIsNotNone(analysis)
        analysis_dict = SafeDict(cast(MarketAnalysis, analysis))
        trend = analysis_dict.get("trend", "Unknown")
        self.assertEqual(trend, "Neutral")
    
    def test_insufficient_data(self):
        """Test behavior when insufficient data is available."""
        self.redis_mock.get_price_history.return_value = []
        analysis = self.monitor.analyze_market()
        
        self.assertIsNotNone(analysis)
        analysis_dict = SafeDict(cast(MarketAnalysis, analysis))
        self.assertEqual(analysis_dict.get("trend"), "Error")
        self.assertEqual(analysis_dict.get("error"), "No price data available")
    
    def test_fibonacci_levels_calculation(self):
        """Test Fibonacci retracement levels calculation."""
        prices = [float(p["price"]) for p in self.sample_history]
        levels = self.monitor.calculate_fibonacci_levels(prices)
        
        # Test key Fibonacci levels
        self.assertIn("two_three_six", levels)
        self.assertIn("three_eight_two", levels)
        self.assertIn("five_hundred", levels)
        self.assertIn("six_one_eight", levels)
        self.assertIn("seven_eight_six", levels)
        
        # Verify level calculations
        price_range = max(prices) - min(prices)
        self.assertAlmostEqual(levels["two_three_six"], min(prices) + price_range * 0.236)
        self.assertAlmostEqual(levels["six_one_eight"], min(prices) + price_range * 0.618)
    
    def test_fibonacci_alignment_detection(self):
        """Test detection of price alignment with Fibonacci levels."""
        prices = [float(p["price"]) for p in self.sample_history]
        levels = self.monitor.calculate_fibonacci_levels(prices)
        
        # Test price exactly at 0.618 level
        price_at_618 = levels.get("0.618")
        if price_at_618 is not None:
            alignment = self.monitor.detect_fibonacci_alignment(price_at_618, levels)
            
            self.assertIsNotNone(alignment)
            if is_not_none(alignment):
                self.assertEqual(alignment.get("type"), "Retracement")
                self.assertEqual(alignment.get("level"), "0.618")
                self.assertAlmostEqual(alignment.get("difference_pct", float('inf')), 0.0)
    
    def test_market_analysis(self):
        """Test comprehensive market analysis functionality."""
        analysis = self.monitor.analyze_market()
        
        self.assertIsNotNone(analysis)
        analysis_dict = SafeDict(cast(MarketAnalysis, analysis))
        # Verify basic analysis results
        self.assertIsNotNone(analysis_dict.get("trend"))
        self.assertIsNotNone(analysis_dict.get("current_price"))
        self.assertIsNotNone(analysis_dict.get("fibonacci_levels"))
        self.assertIsNotNone(analysis_dict.get("fibonacci_alignment"))
        self.assertIsNotNone(analysis_dict.get("mm_trap"))
        
        # Check timestamp
        self.assertIn("timestamp", analysis_dict)
        
        # Check quantum analysis if enabled
        if self.monitor.quantum_mode:
            self.assertIn("quantum_state", analysis_dict)
            self.assertIn("temporal_data", analysis_dict)
            self.assertIn("energy_shift", analysis_dict)
            self.assertIn("trinity_states", analysis_dict)
    
    def test_trend_output_formatting(self):
        """Test trend output formatting with colors and indicators."""
        # Test bullish trend
        bullish_output = self.monitor.format_trend_output("15min", "Strongly Bullish", 2.5)
        self.assertIn("Strongly Bullish", bullish_output)
        self.assertIn("+2.50%", bullish_output)
        self.assertIn("📈", bullish_output)
        
        # Test bearish trend
        bearish_output = self.monitor.format_trend_output("1h", "Strongly Bearish", -3.0)
        self.assertIn("Strongly Bearish", bearish_output)
        self.assertIn("-3.00%", bearish_output)
        self.assertIn("📉", bearish_output)
        
        # Test neutral trend
        neutral_output = self.monitor.format_trend_output("4h", "Neutral", 0.1)
        self.assertIn("Neutral", neutral_output)
        self.assertIn("+0.10%", neutral_output)
        self.assertIn("➡️", neutral_output)
    
    def test_error_handling(self):
        """Test error handling in market analysis."""
        # Simulate Redis error
        self.redis_mock.get_price_history.side_effect = Exception("Redis connection failed")
        
        # Test error handling in market analysis
        analysis = self.monitor.analyze_market()
        self.assertIsNotNone(analysis)
        analysis_dict = SafeDict(cast(MarketAnalysis, analysis))
        self.assertEqual(analysis_dict.get("trend"), "Error")
        self.assertEqual(analysis_dict.get("error"), "Redis connection failed")
        self.assertEqual(self.monitor.consecutive_errors, 1)
    
    def test_mm_trap_detection(self):
        """Test market maker trap detection."""
        # Test trap detection with high probability
        self.ai_mock.predict_trap_probability.return_value = 0.8
        trap = self.monitor.detect_mm_trap("1h", "bullish", 5.0)
        
        self.assertIsNotNone(trap)
        if is_not_none(trap):
            self.assertTrue(trap.get("detected"))
            self.assertEqual(trap.get("type"), "bull")
            self.assertEqual(trap.get("timeframe"), "1h")
            self.assertEqual(trap.get("trend"), "bullish")
            self.assertEqual(trap.get("change"), 5.0)
        
        # Test no trap detection
        self.ai_mock.predict_trap_probability.return_value = 0.5
        trap = self.monitor.detect_mm_trap("1h", "neutral", 0.1)
        self.assertIsNone(trap)

class TestOmegaMarketTrendMonitor(unittest.TestCase):
    """Test cases for the OMEGA Market Trend Monitor with Trinity Matrix."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create sample history with clear trends
        self.bullish_history = [
            {"timestamp": "2024-03-27T00:00:00", "price": 50000.0},
            {"timestamp": "2024-03-27T01:00:00", "price": 51000.0},
            {"timestamp": "2024-03-27T02:00:00", "price": 52000.0},
            {"timestamp": "2024-03-27T03:00:00", "price": 53000.0},
            {"timestamp": "2024-03-27T04:00:00", "price": 54000.0}
        ]
        
        # Create mock objects
        self.redis_mock = Mock(spec=RedisManager)
        self.redis_mock.get_price_history.return_value = self.bullish_history
        self.redis_mock.get_current_price.return_value = 50000.0
        
        self.logger_mock = Mock(spec=OmegaLogger)
        self.logger_mock.log_info.return_value = None
        self.logger_mock.log_error.return_value = None
        self.logger_mock.log_warning.return_value = None
        
        self.monitor = OmegaMarketTrendMonitor(
            redis_manager=self.redis_mock,
            logger=self.logger_mock,
            analysis_interval=1,
            use_ai=True,
            quantum_mode=True
        )
    
    def _create_sample_price_history(self) -> PriceHistory:
        """Create sample price history for testing."""
        return [
            {"timestamp": "2024-03-27T00:00:00", "price": 50000.0},
            {"timestamp": "2024-03-27T01:00:00", "price": 51000.0},
            {"timestamp": "2024-03-27T02:00:00", "price": 52000.0},
            {"timestamp": "2024-03-27T03:00:00", "price": 53000.0},
            {"timestamp": "2024-03-27T04:00:00", "price": 54000.0}
        ]
    
    def test_trinity_matrix_initialization(self):
        """Test initialization of Trinity Matrix components."""
        self.assertIsNotNone(self.monitor.trinity_matrix)
        if is_not_none(self.monitor.trinity_matrix):
            self.assertEqual(self.monitor.trinity_matrix.quantum_state, 0.0)
            self.assertEqual(self.monitor.trinity_matrix.energy_shift, 0.0)
            self.assertEqual(self.monitor.trinity_matrix.alignment_score, 0.0)
            self.assertEqual(len(self.monitor.trinity_matrix.temporal_data), 0)
    
    def test_quantum_state_calculation(self):
        """Test quantum state calculation in Trinity Matrix."""
        prices = [float(p["price"]) for p in self._create_sample_price_history()]
        trinity_matrix = cast(TrinityMatrixProtocol, self.monitor.trinity_matrix)
        if is_not_none(trinity_matrix):
            trinity_matrix.update_states(prices)
            
            self.assertNotEqual(trinity_matrix.quantum_state, 0.0)
            self.assertEqual(trinity_matrix.quantum_state, np.mean(np.diff(prices)))
    
    def test_temporal_data_calculation(self):
        """Test temporal analysis data calculation."""
        prices = [float(p["price"]) for p in self._create_sample_price_history()]
        trinity_matrix = cast(TrinityMatrixProtocol, self.monitor.trinity_matrix)
        if is_not_none(trinity_matrix):
            trinity_matrix.update_states(prices)
            
            temporal_data = trinity_matrix.temporal_data
            self.assertEqual(len(temporal_data), len(prices))
            
            for i, data in enumerate(temporal_data):
                self.assertEqual(data["price"], prices[i])
                self.assertEqual(data["timestamp"], i)
                if i > 0:
                    self.assertEqual(data["energy"], abs(prices[i] - prices[i-1]))
                else:
                    self.assertEqual(data["energy"], 0.0)
    
    def test_energy_shift_calculation(self):
        """Test energy shift detection in market."""
        # Set bullish history
        self.redis_mock.get_price_history.return_value = self.bullish_history
        prices = [float(p["price"]) for p in self.bullish_history]
        trinity_matrix = cast(TrinityMatrixProtocol, self.monitor.trinity_matrix)
        if is_not_none(trinity_matrix):
            trinity_matrix.update_states(prices)
            
            self.assertNotEqual(trinity_matrix.energy_shift, 0.0)
            self.assertEqual(trinity_matrix.energy_shift, float(np.mean(np.abs(np.diff(prices)))))
    
    def test_alignment_score_calculation(self):
        """Test divine alignment score calculation."""
        prices = [float(p["price"]) for p in self._create_sample_price_history()]
        trinity_matrix = cast(TrinityMatrixProtocol, self.monitor.trinity_matrix)
        if is_not_none(trinity_matrix):
            trinity_matrix.update_states(prices)
            
            score = trinity_matrix.calculate_alignment_score()
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
    
    def test_market_analysis_with_trinity(self):
        """Test comprehensive market analysis with Trinity Matrix integration."""
        analysis = self.monitor.analyze_market()
        
        self.assertIsNotNone(analysis)
        analysis_dict = SafeDict(cast(MarketAnalysis, analysis))
        # Check Trinity Matrix results
        self.assertIn("quantum_state", analysis_dict)
        self.assertIn("temporal_data", analysis_dict)
        self.assertIn("energy_shift", analysis_dict)
        self.assertIn("trinity_states", analysis_dict)
        
        trinity_states = analysis_dict.get("trinity_states", {})
        if is_not_none(trinity_states):
            self.assertIn("quantum_state", trinity_states)
            self.assertIn("temporal_data", trinity_states)
            self.assertIn("energy_shift", trinity_states)
            self.assertIn("alignment_score", trinity_states)
    
    def test_empty_price_history(self):
        """Test Trinity Matrix behavior with empty price history."""
        self.redis_mock.get_price_history.return_value = []
        trinity_matrix = cast(TrinityMatrixProtocol, self.monitor.trinity_matrix)
        if is_not_none(trinity_matrix):
            trinity_matrix.update_states([])
            
            self.assertEqual(trinity_matrix.quantum_state, 0.0)
            self.assertEqual(trinity_matrix.energy_shift, 0.0)
            self.assertEqual(trinity_matrix.alignment_score, 0.0)
            self.assertEqual(len(trinity_matrix.temporal_data), 0)
    
    def test_single_price_history(self):
        """Test Trinity Matrix behavior with single price point."""
        single_price = [50000.0]
        trinity_matrix = cast(TrinityMatrixProtocol, self.monitor.trinity_matrix)
        if is_not_none(trinity_matrix):
            trinity_matrix.update_states(single_price)
            
            self.assertEqual(trinity_matrix.quantum_state, 0.0)
            self.assertEqual(trinity_matrix.energy_shift, 0.0)
            self.assertEqual(trinity_matrix.alignment_score, 0.0)
            self.assertEqual(len(trinity_matrix.temporal_data), 1)
            self.assertEqual(trinity_matrix.temporal_data[0]["energy"], 0.0)

if __name__ == '__main__':
    unittest.main() 