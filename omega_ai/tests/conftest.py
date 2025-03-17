"""
DIVINE RASTA TEST CONFIGURATION 🌿🔥
Provides blessed configuration for all tests with JAH guidance.
"""

import pytest
import os
import sys

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

def pytest_addoption(parser):
    """Add divine command line options with JAH BLESSING"""
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="run slow tests with divine patience"
    )
    parser.addoption(
        "--run-integration", action="store_true", default=False, help="run integration tests with divine synergy"
    )

def pytest_configure(config):
    """Configure the divine test environment"""
    # Register divine markers
    config.addinivalue_line("markers", "slow: mark test as slow running (needs divine patience)")
    config.addinivalue_line("markers", "integration: mark test as integration test (needs divine synergy)")
    config.addinivalue_line("markers", "fibonacci: mark test as testing fibonacci divine patterns")
    config.addinivalue_line("markers", "schumann: mark test as testing schumann divine resonance")

def pytest_collection_modifyitems(config, items):
    """Divinely modify test collection based on command line options"""
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="need --run-slow option to run with divine patience")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
                
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="need --run-integration option to run with divine synergy")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)

class TestConfig:
    """Divine test configuration with blessed mock data."""
    
    # Mock price data for Fibonacci tests
    MOCK_PRICE_HISTORY = [50000, 51000, 50500, 52000, 53000, 51500, 52500]
    
    # Predefined Fibonacci levels
    FIBONACCI_LEVELS = {
        "0.236": 50710,
        "0.382": 51080,
        "0.500": 51500,
        "0.618": 51920,
        "0.786": 52500
    }

@pytest.fixture
def mock_redis():
    """Provide a mock Redis client for divine test isolation."""
    from unittest.mock import MagicMock
    mock = MagicMock()
    # Add any needed mock behaviors here
    return mock

@pytest.fixture
def setup_mock_redis_data(mock_redis):
    """Setup mock data in Redis for blessed testing."""
    # Mock data setup logic here
    pass