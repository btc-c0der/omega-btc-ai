"""
🎯 OMEGA RASTA TEST CONFIGURATION 🎯
===================================

Shared test configuration and fixtures for the Fibonacci detector.
May the golden ratio be with you! 🚀
"""

import pytest
from omega_ai.mm_trap_detector.fibonacci_detector import FibonacciDetector

@pytest.fixture(scope="session")
def test_config():
    """Shared test configuration."""
    return {
        "min_swing_diff": 0.005,  # 0.5% minimum difference for swing points
        "fibonacci_tolerance": 0.005,  # 0.5% tolerance for Fibonacci levels
        "confirmation_threshold": 3,  # Number of confirmations needed for swing points
        "price_history_size": 100,  # Size of price history to maintain
        "timeframes": ["5m", "15m", "1h", "4h", "1d"],  # Supported timeframes
        "schumann_frequencies": [7.83, 14.3, 20.8, 27.3, 33.8],  # Schumann resonance frequencies
        "golden_ratio": 0.618,  # Golden ratio constant
        "fibonacci_levels": {
            "0%": 0.0,
            "23.6%": 0.236,
            "38.2%": 0.382,
            "50%": 0.5,
            "61.8%": 0.618,
            "78.6%": 0.786,
            "100%": 1.0,
            "127.2%": 1.272,
            "161.8%": 1.618,
            "261.8%": 2.618
        }
    }

@pytest.fixture(scope="function")
def fib_detector(test_config):
    """Create a fresh detector instance for each test."""
    detector = FibonacciDetector()
    # Apply test configuration
    detector.min_swing_diff = test_config["min_swing_diff"]
    detector.confirmation_threshold = test_config["confirmation_threshold"]
    return detector

@pytest.fixture(scope="function")
def mock_redis():
    """Create a mock Redis connection."""
    from unittest.mock import MagicMock
    mock = MagicMock()
    mock.get.return_value = None
    mock.set.return_value = True
    mock.zadd.return_value = True
    return mock

@pytest.fixture(scope="function")
def sample_price_data():
    """Create sample price data for testing."""
    import datetime
    base_time = datetime.datetime.now(datetime.timezone.utc)
    prices = []
    for i in range(20):
        timestamp = base_time + datetime.timedelta(minutes=i*5)
        price = 42000.0 + (i * 100) * (1 + 0.618 * (i % 2))  # Golden ratio modulation
        prices.append((timestamp, price))
    return prices

@pytest.fixture(scope="function")
def sample_fibonacci_levels():
    """Create sample Fibonacci levels for testing."""
    return {
        "0% (Base)": 40000.0,
        "23.6%": 41180.0,
        "38.2%": 41910.0,
        "50%": 42500.0,
        "61.8%": 43090.0,  # Golden ratio level
        "78.6%": 43930.0,
        "100%": 45000.0,
        "127.2%": 46360.0,
        "161.8%": 48090.0
    } 