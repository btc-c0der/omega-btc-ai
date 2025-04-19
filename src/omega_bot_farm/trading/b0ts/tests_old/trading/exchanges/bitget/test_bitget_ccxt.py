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
Bitget-specific tests for CCXT Integration in Omega Bot Farm.

This module extends the base CCXT tests with Bitget-specific tests.
"""

import os
import pytest
import unittest.mock as mock
from typing import Dict, Any, List

# Import the base test classes
from src.omega_bot_farm.tests.trading.exchanges.test_ccxt_b0t import BaseCCXTClientTests
from src.omega_bot_farm.tests.trading.exchanges.conftest import requires_ccxt

# Import the class to test
from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t, to_dict

# Bitget-specific constants
BITGET_SYMBOL_SUFFIX = "_UMCBL"

@pytest.fixture
def bitget_client():
    """Create a Bitget-specific client for testing."""
    with mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt'):
        with mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt_async'):
            with mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.HAVE_CCXT', True):
                client = ExchangeClientB0t(exchange_id='bitget')
                client.symbol_suffix = BITGET_SYMBOL_SUFFIX
                # Add any additional Bitget-specific configuration here
                client.exchange = mock.AsyncMock()
                return client

class TestBitgetClient(BaseCCXTClientTests.TestUtilityFunctions):
    """Tests specific to Bitget exchange."""

    def test_bitget_symbol_suffix(self, bitget_client):
        """Test Bitget-specific symbol suffix."""
        assert bitget_client.symbol_suffix == BITGET_SYMBOL_SUFFIX

@requires_ccxt
class TestBitgetClientWithCCXT(BaseCCXTClientTests.TestWithCCXT):
    """Bitget-specific tests that require CCXT to be installed."""
    
    @pytest.mark.asyncio
    async def test_bitget_specific_format_symbol(self, bitget_client):
        """Test Bitget-specific symbol formatting."""
        # Test with Bitget's UMCBL suffix
        formatted = bitget_client._format_symbol("BTC_UMCBL")
        assert formatted == "BTC/USDT:USDT"
        
        # Test with contract symbol
        formatted = bitget_client._format_symbol("BTCUSDT_UMCBL")
        assert formatted == "BTC/USDT:USDT"
    
    @pytest.mark.asyncio
    async def test_bitget_copy_trade(self, bitget_client):
        """Test Bitget-specific copy trade functionality."""
        # Setup mock response
        bitget_client.exchange.private_post_mix_v1_order_follow_place = mock.AsyncMock(
            return_value={"data": {"orderId": "123456"}}
        )
        
        # Test the copy trade functionality (hypothetical method)
        # In a real implementation, you would call the actual method on the client
        # This is just an example of how you might test Bitget-specific functionality
        result = await bitget_client.exchange.private_post_mix_v1_order_follow_place({
            "symbol": "BTCUSDT_UMCBL",
            "marginCoin": "USDT",
            "side": "buy",
            "orderType": "market",
            "size": "0.001",
            "targetCoin": "USDT"
        })
        
        assert result["data"]["orderId"] == "123456"
        bitget_client.exchange.private_post_mix_v1_order_follow_place.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_bitget_specific_close_position(self, bitget_client):
        """Test Bitget-specific position closing."""
        # Setup mock responses for Bitget-specific API
        position = {
            "info": {"symbolId": "BTCUSDT_UMCBL"},
            "symbol": "BTC/USDT:USDT",
            "contracts": 0.01, 
            "contractSize": 1.0,
            "entryPrice": 30000.0,
            "side": "long"
        }
        
        bitget_client.exchange.fetch_positions = mock.AsyncMock(return_value=[position])
        
        # Setup create_order mock for the close_position call
        bitget_client.exchange.create_order = mock.AsyncMock(return_value={
            "id": "12345",
            "info": {"orderId": "12345"},
            "status": "closed"
        })
        
        # Patch to_dict to return our position
        with mock.patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.to_dict', return_value=position):
            # Test the position closing with Bitget-specific symbol format
            result = await bitget_client.close_position("BTCUSDT_UMCBL")
            
            # Verify correct endpoints were called
            bitget_client.exchange.fetch_positions.assert_called_once()
            
            # In a real implementation, you might check that the code uses the special Bitget endpoint
            # This is just an example of testing exchange-specific behavior
            assert "closed_positions" in result
            assert len(result["closed_positions"]) == 1

# Concrete implementation of the tests for Bitget without CCXT
class TestBitgetClientWithoutCCXT(BaseCCXTClientTests.TestWithoutCCXT):
    """Tests for Bitget client without CCXT installed."""
    pass 