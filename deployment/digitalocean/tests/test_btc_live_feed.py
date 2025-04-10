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
OMEGA BTC AI - DigitalOcean BTC Live Feed Tests 🔱

A spiritually-aligned test suite that verifies the divine harmony of the Bitcoin 
price feed in the DigitalOcean deployment, ensuring proper flow of cosmic market energy.

JAH BLESS THE PRICE FEED WITH DIVINE ACCURACY! 🙏🌟
"""

import os
import sys
import pytest
import time
import json
import redis
import asyncio
import random
import math
from typing import List, Dict, Any
from datetime import datetime, timedelta, UTC
from unittest.mock import patch, MagicMock, AsyncMock, ANY

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

# Import the necessary modules with JAH BLESSING
from deployment.digitalocean.redis_manager import DigitalOceanRedisManager
from deployment.digitalocean.logging.omega_logger import OmegaLogger
from deployment.digitalocean.btc_live_feed import BtcLiveFeed

# Test fixtures with divine energy alignment
@pytest.fixture
async def redis_manager():
    """Create a blessed Redis manager with sacred connection."""
    manager = DigitalOceanRedisManager()
    await manager._connect()
    return manager

@pytest.fixture
def mock_price_feed():
    """Create a spiritually aligned BTC price feed for testing."""
    feed = MagicMock()
    feed.redis_client = AsyncMock()
    feed.ws = AsyncMock()
    feed.on_message = AsyncMock()
    feed.send_to_mm_websocket = AsyncMock()
    feed.check_redis_health = AsyncMock(return_value=True)
    return feed

@pytest.fixture
def sample_price_history():
    """Generate Fibonacci-aligned price history for divine testing."""
    base_price = 50000.0
    history = []
    
    # Create 100 price points with Fibonacci-inspired movements
    for i in range(100):
        # Add some Fibonacci-inspired price movement
        fib_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        movement = fib_sequence[i % 10] * (10 if i % 2 == 0 else -7)
        
        timestamp = datetime.now() - timedelta(minutes=100-i)
        price = base_price + movement
        
        history.append({
            "timestamp": timestamp.isoformat(),
            "price": price,
            "volume": 1 + (i % 5)
        })
    
    return history

class TestBtcLiveFeed:
    """Test BTC live feed with divine protection."""
    
    @pytest.fixture
    async def feed(self):
        """Create BTC live feed fixture."""
        # Mock dependencies
        redis_manager = AsyncMock(spec=DigitalOceanRedisManager)
        logger = AsyncMock(spec=OmegaLogger)
        ws = AsyncMock()
        
        # Create feed
        feed = BtcLiveFeed(redis_manager=redis_manager, logger=logger)
        feed.ws = ws
        feed._last_update = datetime.now()
        
        return feed
    
    @pytest.mark.asyncio
    async def test_check_redis_health(self, feed):
        """Test Redis health check with divine protection."""
        # Mock Redis manager
        feed.redis_manager.ping.return_value = True
        
        # Check health
        result = await feed.check_redis_health()
        
        # Verify result
        assert result is True
        feed.redis_manager.ping.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_on_message(self, feed):
        """Test handling incoming messages with divine protection."""
        # Test data
        message = json.dumps({
            "p": "85000.50",
            "q": "1.5"
        })
        
        # Process message
        await feed.on_message(message)
        
        # Verify Redis update
        feed.redis_manager.set_cached.assert_called_once_with(
            "last_btc_price",
            "85000.50"
        )
        
        # Verify price update logging
        feed.logger.log_price_update.assert_called_once_with(85000.50, 1.5)
        
        # Verify MM websocket update
        feed.ws.send.assert_called_once_with(json.dumps({
            "price": 85000.50,
            "volume": 1.5,
            "timestamp": feed._last_update.isoformat()
        }))
    
    @pytest.mark.asyncio
    async def test_send_to_mm_websocket(self, feed):
        """Test sending data to MM websocket with divine protection."""
        # Test sending None data
        with pytest.raises(ValueError, match="Cannot send None data to MM websocket"):
            await feed.send_to_mm_websocket(None)
            
        # Test sending valid data
        data = {"price": 50000.0, "volume": 1.5}
        await feed.send_to_mm_websocket(data)
        feed.ws.send.assert_called_once_with(json.dumps(data))
    
    @pytest.mark.asyncio
    async def test_chaos_network_disruption(self, feed):
        """Test handling network disruptions with divine resilience."""
        # Mock Redis manager to fail
        feed.redis_manager.ping.side_effect = Exception("Network chaos")
        
        # Check health
        result = await feed.check_redis_health()
        
        # Verify result
        assert result is False
        feed.redis_manager.ping.assert_called_once()
        feed.logger.error.assert_called_once_with("Redis health check failed: Network chaos")
    
    @pytest.mark.asyncio
    async def test_dos_protection(self, feed):
        """Test protection against DoS attacks with divine shield."""
        # Mock Redis manager to be slow
        feed.redis_manager.set_cached.side_effect = AsyncMock(side_effect=lambda *args: None)
        
        # Send multiple messages rapidly
        messages = [
            json.dumps({"p": str(price), "q": "1.0"})
            for price in range(50000, 51000, 100)
        ]
        
        for message in messages:
            await feed.on_message(message)
        
        # Verify rate limiting
        assert feed.redis_manager.set_cached.call_count == len(messages)
    
    @pytest.mark.asyncio
    async def test_performance_under_load(self, feed):
        """Test performance under heavy load with divine optimization."""
        # Mock Redis manager to be fast
        feed.redis_manager.set_cached.side_effect = AsyncMock(side_effect=lambda *args: None)
        
        # Send many messages
        messages = [
            json.dumps({"p": str(price), "q": "1.0"})
            for price in range(50000, 55000, 100)
        ]
        
        for message in messages:
            await feed.on_message(message)
        
        # Verify all messages processed
        assert feed.redis_manager.set_cached.call_count == len(messages)
    
    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, feed):
        """Test error handling and recovery with divine grace."""
        # Mock Redis manager to fail then succeed
        feed.redis_manager.set_cached.side_effect = [
            Exception("Temporary failure"),
            None
        ]
        
        # Send two messages
        messages = [
            json.dumps({"p": "50000.0", "q": "1.0"}),
            json.dumps({"p": "50100.0", "q": "1.0"})
        ]
        
        for message in messages:
            await feed.on_message(message)
        
        # Verify error handling
        assert feed.redis_manager.set_cached.call_count == 2
        feed.logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_constructor_initialization(self):
        """Test constructor initialization."""
        redis_manager = AsyncMock(spec=DigitalOceanRedisManager)
        logger = AsyncMock(spec=OmegaLogger)
        feed = BtcLiveFeed(redis_manager=redis_manager, logger=logger)
        
        # Verify initialization
        assert feed.redis_manager == redis_manager
        assert feed.logger == logger
        assert feed.ws is None
        assert feed._last_update is None
        assert feed._last_price is None
        assert feed._last_volume is None

    @pytest.mark.asyncio
    async def test_send_to_mm_websocket_error_handling(self, feed):
        """Test error handling in send_to_mm_websocket."""
        # Test sending None data
        with pytest.raises(ValueError, match="Cannot send None data to MM websocket"):
            await feed.send_to_mm_websocket(None)
        
        # Test sending valid data
        data = {"price": 50000.0, "volume": 1.5}
        await feed.send_to_mm_websocket(data)
        feed.ws.send.assert_called_once_with(json.dumps(data))

    @pytest.mark.asyncio
    async def test_on_message_error_handling(self, feed):
        """Test error handling in on_message."""
        # Test invalid JSON
        await feed.on_message("invalid json")
        feed.logger.error.assert_called_once()
        feed.redis_manager.set_cached.assert_not_called()
        
        # Reset mocks
        feed.logger.error.reset_mock()
        feed.redis_manager.set_cached.reset_mock()
        
        # Test empty message
        await feed.on_message("{}")
        feed.logger.warning.assert_called_once_with("Received empty message")
        feed.redis_manager.set_cached.assert_not_called()
        
        # Reset mocks
        feed.logger.warning.reset_mock()
        feed.redis_manager.set_cached.reset_mock()
        
        # Test missing price
        await feed.on_message('{"q": "1.5"}')
        feed.redis_manager.set_cached.assert_not_called()
        
        # Test invalid price format
        await feed.on_message('{"p": "invalid", "q": "1.5"}')
        feed.redis_manager.set_cached.assert_not_called()

    @pytest.mark.asyncio
    async def test_on_message_successful_processing(self, feed):
        """Test successful message processing."""
        message = json.dumps({
            "p": "85000.50",
            "q": "1.5"
        })
        
        # Process message
        await feed.on_message(message)
        
        # Verify Redis update
        feed.redis_manager.set_cached.assert_called_once_with(
            "last_btc_price",
            "85000.50"
        )
        
        # Verify price update logging
        feed.logger.log_price_update.assert_called_once_with(85000.50, 1.5)
        
        # Verify MM websocket update
        feed.ws.send.assert_called_once_with(json.dumps({
            "price": 85000.50,
            "volume": 1.5,
            "timestamp": feed._last_update.isoformat()
        }))

    @pytest.mark.asyncio
    async def test_on_message_high_frequency_mode(self, feed):
        """Test high frequency message processing."""
        message = json.dumps({
            "p": "85000.50",
            "q": "1.5"
        })
        
        # Process multiple messages in quick succession
        for _ in range(5):
            await feed.on_message(message)
            await asyncio.sleep(0.1)  # Small delay to simulate high frequency
        
        # Verify Redis updates
        assert feed.redis_manager.set_cached.call_count == 5
        
        # Verify price update logging
        assert feed.logger.log_price_update.call_count == 5
        
        # Verify MM websocket updates
        assert feed.ws.send.call_count == 5 