#!/usr/bin/env python3

"""
Pytest fixtures for CCXT integration tests.

This module provides common fixtures for testing the CCXT integration
in the Omega Bot Farm.
"""

import os
import pytest
import unittest.mock as mock

# Import the class to test
from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t

# Setup testing environment
@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up environment variables for testing."""
    # Store original env vars
    original_env = {}
    for key in ['SYMBOL', 'BITGET_API_KEY', 'BITGET_SECRET_KEY', 'BITGET_PASSPHRASE', 'USE_TESTNET']:
        original_env[key] = os.environ.get(key)
    
    # Set testing env vars
    os.environ['SYMBOL'] = 'BTCUSDT'
    os.environ['BITGET_API_KEY'] = 'test_api_key'
    os.environ['BITGET_SECRET_KEY'] = 'test_secret_key'
    os.environ['BITGET_PASSPHRASE'] = 'test_passphrase'
    os.environ['USE_TESTNET'] = 'true'
    
    yield
    
    # Restore original env vars
    for key, value in original_env.items():
        if value is None:
            if key in os.environ:
                del os.environ[key]
        else:
            os.environ[key] = value

# Mock CCXT libraries
@pytest.fixture
def ccxt_mocks():
    """Create mock objects for CCXT libraries."""
    ccxt_mock = mock.MagicMock()
    ccxt_async_mock = mock.MagicMock()
    
    # Create a mock exchange instance
    mock_exchange = mock.MagicMock()
    
    # Configure the async exchange constructor
    ccxt_async_mock.exchanges = {
        'bitget': mock.MagicMock(return_value=mock_exchange),
        'binance': mock.MagicMock(return_value=mock_exchange),
    }
    
    return {
        'ccxt': ccxt_mock,
        'ccxt_async': ccxt_async_mock,
        'exchange': mock_exchange
    }

@pytest.fixture
def ccxt_client(ccxt_mocks):
    """Create a mock CCXT client for testing."""
    with mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt', ccxt_mocks['ccxt']), \
         mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt_async', ccxt_mocks['ccxt_async']), \
         mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.HAVE_CCXT', True):
        
        # Return client
        client = ExchangeClientB0t(exchange_id='bitget')
        # Replace exchange with our mock
        client.exchange = ccxt_mocks['exchange']
        return client

@pytest.fixture
def binance_client(ccxt_mocks):
    """Create a mock Binance client for testing different exchanges."""
    with mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt', ccxt_mocks['ccxt']), \
         mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt_async', ccxt_mocks['ccxt_async']), \
         mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.HAVE_CCXT', True):
        
        # Return client
        client = ExchangeClientB0t(exchange_id='binance')
        # Replace exchange with our mock
        client.exchange = ccxt_mocks['exchange']
        # Set a different symbol format for Binance
        client.symbol_format = "{0}/USDT"
        client.symbol_suffix = ""
        return client

@pytest.fixture
def no_ccxt_client():
    """Create a client when CCXT is not available."""
    with mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.HAVE_CCXT', False):
        client = ExchangeClientB0t(exchange_id='bitget')
        return client 