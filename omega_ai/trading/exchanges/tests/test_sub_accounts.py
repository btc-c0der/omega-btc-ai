#!/usr/bin/env python3

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


"""
Test suite for BitGet sub-account functionality.
"""

import os
import pytest
from typing import Dict, Any
from ..bitget_trader import BitGetTrader

# Test configuration
TEST_SUB_ACCOUNT_NAME = "test_trader_1"
TEST_SUB_ACCOUNT_PASSWORD = "Test123!@#"

@pytest.fixture
def bitget_trader():
    """Create a BitGet trader instance for testing."""
    trader = BitGetTrader(
        profile_type="strategic",
        use_testnet=True,
        api_version="v2"
    )
    return trader

def test_create_sub_account(bitget_trader):
    """Test creating a new sub-account."""
    result = bitget_trader.create_sub_account(TEST_SUB_ACCOUNT_NAME, TEST_SUB_ACCOUNT_PASSWORD)
    assert result is not None
    assert "code" in result
    assert result["code"] == "00000"  # Success code

def test_get_sub_accounts(bitget_trader):
    """Test getting list of sub-accounts."""
    result = bitget_trader.get_sub_accounts()
    assert result is not None
    assert isinstance(result, list)
    
    # Verify our test account exists
    test_account = next((acc for acc in result if acc["subAccountName"] == TEST_SUB_ACCOUNT_NAME), None)
    assert test_account is not None

def test_get_sub_account_balance(bitget_trader):
    """Test getting balance for a sub-account."""
    result = bitget_trader.get_sub_account_balance(TEST_SUB_ACCOUNT_NAME)
    assert result is not None
    assert "totalAsset" in result
    assert "available" in result

def test_transfer_to_sub_account(bitget_trader):
    """Test transferring funds to a sub-account."""
    # Transfer a small amount (0.1 USDT) to test
    result = bitget_trader.transfer_to_sub_account(TEST_SUB_ACCOUNT_NAME, 0.1)
    assert result is not None
    assert "code" in result
    assert result["code"] == "00000"  # Success code

def test_transfer_from_sub_account(bitget_trader):
    """Test transferring funds from a sub-account."""
    # Transfer a small amount (0.1 USDT) back from test
    result = bitget_trader.transfer_from_sub_account(TEST_SUB_ACCOUNT_NAME, 0.1)
    assert result is not None
    assert "code" in result
    assert result["code"] == "00000"  # Success code

def test_trading_with_sub_account():
    """Test trading operations with a sub-account."""
    # Create a trader instance with sub-account
    trader = BitGetTrader(
        profile_type="strategic",
        use_testnet=True,
        api_version="v2",
        sub_account_name=TEST_SUB_ACCOUNT_NAME
    )
    
    # Test getting balance
    balance = trader.get_account_balance()
    assert balance is not None
    
    # Test getting positions
    positions = trader.get_positions()
    assert positions is not None
    
    # Test getting market data
    ticker = trader.get_market_ticker("BTCUSDT")
    assert ticker is not None

def test_sub_account_authentication():
    """Test that sub-account authentication is properly included in requests."""
    trader = BitGetTrader(
        profile_type="strategic",
        use_testnet=True,
        api_version="v2",
        sub_account_name=TEST_SUB_ACCOUNT_NAME
    )
    
    # Get balance which should include sub-account parameter
    balance = trader.get_account_balance()
    assert balance is not None
    
    # Get positions which should include sub-account parameter
    positions = trader.get_positions()
    assert positions is not None 