
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

import os
import pytest
import requests
from datetime import datetime
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader

# Test configuration
API_KEY = os.getenv("BITGET_MAINNET_API_KEY", "")
SECRET_KEY = os.getenv("BITGET_MAINNET_SECRET_KEY", "")
PASSPHRASE = os.getenv("BITGET_MAINNET_PASSPHRASE", "")

# Initialize the BitGetTrader for MAINNET
trader = BitGetTrader(
    profile_type="strategic",
    api_key=API_KEY,
    secret_key=SECRET_KEY,
    passphrase=PASSPHRASE,
    use_testnet=False,
    initial_capital=10000.0
)

@pytest.fixture
def setup_trader():
    """Fixture to set up the trader for testing."""
    return trader


def test_public_interface(setup_trader):
    """Test the public interface for market data."""
    response = requests.get("https://api.bitget.com/api/mix/v1/market/ticker?symbol=BTCUSDT")
    assert response.status_code == 200
    assert "data" in response.json()


def test_private_interface_authentication(setup_trader):
    """Test the private interface authentication."""
    timestamp = str(int(datetime.now().timestamp() * 1000))
    headers = setup_trader._get_auth_headers(timestamp, "GET", "/api/mix/v1/account/account")
    response = requests.get(
        "https://api.bitget.com/api/mix/v1/account/account",
        headers=headers
    )
    assert response.status_code == 200
    assert "data" in response.json()


def test_signature_error_handling(setup_trader):
    """Test handling of signature errors."""
    # Intentionally use wrong secret key to simulate signature error
    wrong_trader = BitGetTrader(
        profile_type="strategic",
        api_key=API_KEY,
        secret_key="wrong_secret",
        passphrase=PASSPHRASE,
        use_testnet=False,
        initial_capital=10000.0
    )
    timestamp = str(int(datetime.now().timestamp() * 1000))
    headers = wrong_trader._get_auth_headers(timestamp, "GET", "/api/mix/v1/account/account")
    response = requests.get(
        "https://api.bitget.com/api/mix/v1/account/account",
        headers=headers
    )
    assert response.status_code == 400
    assert response.json().get("msg") == "sign signature error"


def test_rate_limiting(setup_trader):
    """Test rate limiting by making rapid requests."""
    response = None  # Initialize response before the loop
    for _ in range(15):  # Exceed the rate limit
        response = requests.get("https://api.bitget.com/api/mix/v1/market/ticker?symbol=BTCUSDT")
        if response.status_code == 429:
            break
    assert response is not None, "Response is None, rate limiting test did not execute as expected"
    assert response.status_code == 429
    assert "too frequent" in response.json().get("msg", "") 