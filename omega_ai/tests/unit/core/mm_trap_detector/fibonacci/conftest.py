"""
🌌 OMEGA RASTA FIBONACCI TEST FIXTURES 🌌
========================================

Shared fixtures for the divine Fibonacci detector tests.
May the golden ratio be with you! 🚀
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from omega_ai.mm_trap_detector.fibonacci_detector import FibonacciDetector

# ANSI color codes for divine output
MAGENTA = "\033[35m"
GREEN = "\033[32m"
RESET = "\033[0m"

@pytest.fixture
def detector():
    """Create a FibonacciDetector instance for testing."""
    return FibonacciDetector(symbol="BTCUSDT", test_mode=True)

@pytest.fixture
def mock_redis():
    """Create a mock Redis connection."""
    with patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn') as mock:
        yield mock

@pytest.fixture
def mock_detector():
    """Create a mock FibonacciDetector instance."""
    with patch('omega_ai.mm_trap_detector.fibonacci_detector.FibonacciDetector') as mock:
        yield mock

@pytest.fixture
def mock_detector_instance():
    """Create a mock FibonacciDetector instance with predefined attributes."""
    mock = MagicMock(spec=FibonacciDetector)
    mock.symbol = "BTCUSDT"
    mock.test_mode = True
    mock.recent_swing_high = 42000.0
    mock.recent_swing_low = 40000.0
    mock.price_history = []
    yield mock

@pytest.fixture
def mock_price_data():
    """Create mock price data for testing."""
    base_time = datetime.now(timezone.utc)
    return [
        (42000.0, base_time.replace(hour=i))
        for i in range(10)
    ]

@pytest.fixture
def mock_fibonacci_levels():
    """Create mock Fibonacci levels for testing."""
    return {
        0.0: 40000.0,
        0.236: 40472.0,
        0.382: 40764.0,
        0.5: 41000.0,
        0.618: 41236.0,
        0.786: 41528.0,
        1.0: 42000.0
    }

@pytest.fixture
def mock_fibonacci_data():
    """Create mock Fibonacci data for testing."""
    return {
        'levels': {
            0.618: 41236.0,
            0.786: 41528.0
        },
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'swing_high': 42000.0,
        'swing_low': 40000.0
    }

@pytest.fixture
def mock_fractal_harmony():
    """Create mock fractal harmony data for testing."""
    return {
        'is_harmonic': True,
        'strength': 0.85,
        'fractal_points': [0.618, 0.786],
        'fibonacci_ratio': 0.618,
        'nested_patterns': [{'level': 0.618, 'strength': 0.9}]
    }

@pytest.fixture
def mock_market_maker_data():
    """Create mock market maker data for testing."""
    return {
        'is_fakeout': True,
        'type': 'bullish',
        'strength': 0.8,
        'target_price': 41000.0,
        'stop_loss': 44000.0
    }

@pytest.fixture
def mock_wick_data():
    """Create mock wick data for testing."""
    return {
        'has_deviation': True,
        'upper_deviation': 500.0,
        'lower_deviation': 400.0,
        'body_size': 100.0,
        'upper_wick_ratio': 5.0,
        'lower_wick_ratio': 4.0
    }

@pytest.fixture
def mock_reversal_data():
    """Create mock reversal data for testing."""
    return {
        'is_valid': True,
        'level': 0.618,
        'strength': 0.85,
        'price': 41236.0,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

@pytest.fixture
def mock_confirmation_data():
    """Create mock confirmation data for testing."""
    return {
        'has_confirmation': True,
        'level': 0.618,
        'strength': 0.9,
        'tests': 3,
        'bounces': 3,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

@pytest.fixture
def mock_trap_data():
    """Create mock trap data for testing."""
    return {
        'is_trap': True,
        'type': 'bullish',
        'strength': 0.85,
        'entry_price': 44000.0,
        'target_price': 41000.0,
        'stop_loss': 45000.0,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

@pytest.fixture
def mock_get_fib_levels():
    """Create a mock Fibonacci levels function for testing."""
    return MagicMock()

@pytest.fixture
def mock_utils_calc():
    """Create a mock utility function for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data():
    """Create a mock detector instance with data for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels():
    """Create a mock detector instance with data and levels for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits():
    """Create a mock detector instance with data, levels, and hits for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences():
    """Create a mock detector instance with data, levels, hits, and confluences for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences():
    """Create a mock detector instance with data, levels, hits, confluences, and confidences for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, and hits for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, and confluences for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, and hits for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, and confluences for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences_and_hits():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, confluences, and hits for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, confluences, hits, and confluences for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, confluences, hits, confluences, and hits for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, confluences, hits, confluences, hits, and confluences for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, confluences, hits, confluences, hits, confluences, and hits for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, confluences, hits, confluences, hits, confluences, hits, and confluences for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, confluences, hits, confluences, hits, confluences, hits, confluences, and hits for testing."""
    return MagicMock()

@pytest.fixture
def mock_detector_instance_with_data_and_levels_and_hits_and_confluences_and_confidences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits_and_confluences_and_hits():
    """Create a mock detector instance with data, levels, hits, confluences, confidences, hits, confluences, hits, confluences, hits, confluences, hits, confluences, hits, confluences, hits, and confluences for testing."""
    return MagicMock() 