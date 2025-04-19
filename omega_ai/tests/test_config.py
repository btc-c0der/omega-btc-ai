# 🌌 AIXBT Divine Monitor Test Configuration
# ----------------------------------------

import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test Configuration
TEST_REDIS_HOST = os.getenv("TEST_REDIS_HOST", "localhost")
TEST_REDIS_PORT = int(os.getenv("TEST_REDIS_PORT", "6379"))
TEST_REDIS_PASSWORD = os.getenv("TEST_REDIS_PASSWORD", "test_password")

TEST_BITGET_API_URL = os.getenv("TEST_BITGET_API_URL", "https://api-testnet.bitget.com")
TEST_BITGET_API_KEY = os.getenv("TEST_BITGET_API_KEY", "test_api_key")
TEST_BITGET_API_SECRET = os.getenv("TEST_BITGET_API_SECRET", "test_api_secret")

TEST_DIVINE_INTERVAL = int(os.getenv("TEST_DIVINE_INTERVAL", "5"))
TEST_DIVINE_ALIGNMENT_THRESHOLD = float(os.getenv("TEST_DIVINE_ALIGNMENT_THRESHOLD", "0.7"))
TEST_DIVINE_TRAP_THRESHOLD = float(os.getenv("TEST_DIVINE_TRAP_THRESHOLD", "0.5"))

TEST_LOG_LEVEL = os.getenv("TEST_LOG_LEVEL", "DEBUG")
TEST_LOG_FILE = os.getenv("TEST_LOG_FILE", "/tmp/test_aixbt_monitor.log")

TEST_GBU2_ENABLED = os.getenv("TEST_GBU2_ENABLED", "true").lower() == "true"
TEST_GBU2_MATRIX_SIZE = int(os.getenv("TEST_GBU2_MATRIX_SIZE", "100"))
TEST_GBU2_HARMONY_THRESHOLD = float(os.getenv("TEST_GBU2_HARMONY_THRESHOLD", "0.8"))

# Test Fixtures
@pytest.fixture
def test_redis_config():
    return {
        "host": TEST_REDIS_HOST,
        "port": TEST_REDIS_PORT,
        "password": TEST_REDIS_PASSWORD,
    }

@pytest.fixture
def test_bitget_config():
    return {
        "api_url": TEST_BITGET_API_URL,
        "api_key": TEST_BITGET_API_KEY,
        "api_secret": TEST_BITGET_API_SECRET,
    }

@pytest.fixture
def test_divine_config():
    return {
        "interval": TEST_DIVINE_INTERVAL,
        "alignment_threshold": TEST_DIVINE_ALIGNMENT_THRESHOLD,
        "trap_threshold": TEST_DIVINE_TRAP_THRESHOLD,
    }

@pytest.fixture
def test_logging_config():
    return {
        "level": TEST_LOG_LEVEL,
        "file": TEST_LOG_FILE,
    }

@pytest.fixture
def test_gbu2_config():
    return {
        "enabled": TEST_GBU2_ENABLED,
        "matrix_size": TEST_GBU2_MATRIX_SIZE,
        "harmony_threshold": TEST_GBU2_HARMONY_THRESHOLD,
    }

# Test Data
TEST_PRICE_DATA = {
    "symbol": "AIXBTUSDT",
    "price": "100.50",
    "volume": "1000.00",
    "timestamp": 1640995200000,
}

TEST_VOLUME_DATA = {
    "symbol": "AIXBTUSDT",
    "volume": "1000.00",
    "timestamp": 1640995200000,
}

TEST_TRAP_DATA = {
    "symbol": "AIXBTUSDT",
    "trap_score": 0.75,
    "timestamp": 1640995200000,
}

# Test Metrics
TEST_DIVINE_METRICS = {
    "price_harmony": 0.85,
    "volume_harmony": 0.75,
    "trap_harmony": 0.65,
    "divine_alignment": 0.75,
}

# Test Redis Keys
TEST_REDIS_KEYS = {
    "price": "aixbt:price:latest",
    "volume": "aixbt:volume:latest",
    "trap": "aixbt:trap:latest",
    "metrics": "aixbt:metrics:latest",
} 