"""
Test suite for TrapQueueManager
==============================

Tests the market maker trap queue management functionality with Redis integration.
"""

import pytest
from unittest.mock import Mock, patch
import time
from datetime import datetime
import json
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.mm_trap_detector.queue_manager import TrapQueueManager

@pytest.fixture
def redis_manager():
    """Create a mock RedisManager."""
    mock_redis = Mock(spec=RedisManager)
    # Set up default return values for methods
    mock_redis.zcard.return_value = 0
    mock_redis.zadd.return_value = 1  # Return 1 for successful add
    mock_redis.zrange.return_value = []
    mock_redis.zremrangebyrank.return_value = True
    mock_redis.delete.return_value = True
    return mock_redis

@pytest.fixture
def queue_manager(redis_manager):
    """Create a TrapQueueManager instance with mocked Redis."""
    # Patch the RedisManager class to return our mock
    with patch('omega_ai.mm_trap_detector.queue_manager.RedisManager', return_value=redis_manager):
        manager = TrapQueueManager(redis_manager=redis_manager)
        yield manager

def test_init(queue_manager, redis_manager):
    """Test TrapQueueManager initialization."""
    assert queue_manager.queue_name == "mm_trap_queue:zset"
    assert queue_manager.max_queue_size == 50000
    assert queue_manager.cleanup_threshold == 60000
    assert queue_manager.sampling_rate == 1.0
    assert queue_manager.min_interval == 0.01

def test_add_trap(queue_manager, redis_manager):
    """Test adding a trap to the queue."""
    trap_data = {
        "type": "bullish",
        "timestamp": datetime.now().isoformat(),
        "price": 50000.0,
        "volume": 1.5,
        "confidence": 0.85
    }
    
    # Mock successful Redis operation
    redis_manager.zadd.return_value = 1  # Return 1 for successful add
    
    # Set initial last_add_time to allow the first add
    queue_manager.last_add_time = time.time() - queue_manager.min_interval - 1
    
    # Add trap
    result = queue_manager.add_trap(trap_data)
    assert result is True
    
    # Verify Redis call
    redis_manager.zadd.assert_called_once()
    args = redis_manager.zadd.call_args[0]
    assert args[0] == "mm_trap_queue:zset"
    assert isinstance(args[1], dict)
    assert json.loads(list(args[1].keys())[0])["type"] == "bullish"

def test_add_trap_rate_limiting(queue_manager, redis_manager):
    """Test rate limiting when adding traps."""
    trap_data = {
        "type": "bearish",
        "timestamp": datetime.now().isoformat(),
        "price": 49000.0,
        "volume": 2.0,
        "confidence": 0.75
    }
    
    # Set initial last_add_time to allow the first add
    queue_manager.last_add_time = time.time() - queue_manager.min_interval - 1
    
    # First add should succeed
    redis_manager.zadd.return_value = 1  # Return 1 for successful add
    assert queue_manager.add_trap(trap_data) is True
    
    # Immediate second add should be rate limited
    assert queue_manager.add_trap(trap_data) is False
    
    # Wait for rate limit to expire
    time.sleep(queue_manager.min_interval)
    assert queue_manager.add_trap(trap_data) is True

def test_get_recent_traps(queue_manager, redis_manager):
    """Test retrieving recent traps."""
    # Mock Redis response
    mock_traps = [
        json.dumps({
            "type": "bullish",
            "timestamp": datetime.now().isoformat(),
            "price": 50000.0,
            "confidence": 0.85
        }),
        json.dumps({
            "type": "bearish",
            "timestamp": datetime.now().isoformat(),
            "price": 49000.0,
            "confidence": 0.75
        })
    ]
    redis_manager.zrange.return_value = mock_traps
    
    # Get recent traps
    traps = queue_manager.get_recent_traps(limit=2)
    assert len(traps) == 2
    assert traps[0]["type"] == "bullish"
    assert traps[1]["type"] == "bearish"
    
    # Verify Redis call
    redis_manager.zrange.assert_called_once_with(
        "mm_trap_queue:zset",
        0,
        1,
        desc=True
    )

def test_cleanup_queue(queue_manager, redis_manager):
    """Test queue cleanup functionality."""
    # Mock queue size check
    redis_manager.zcard.return_value = 70000  # Above cleanup threshold
    
    # Mock successful cleanup
    redis_manager.zremrangebyrank.return_value = True
    
    # Perform cleanup
    result = queue_manager.cleanup_queue()
    assert result is True
    
    # Verify Redis calls
    redis_manager.zcard.assert_called_once_with("mm_trap_queue:zset")
    redis_manager.zremrangebyrank.assert_called_once_with(
        "mm_trap_queue:zset",
        0,
        -queue_manager.max_queue_size
    )

def test_get_queue_size(queue_manager, redis_manager):
    """Test getting queue size."""
    # Mock Redis response
    redis_manager.zcard.return_value = 1000
    
    # Get queue size
    size = queue_manager.get_queue_size()
    assert size == 1000
    
    # Verify Redis call
    redis_manager.zcard.assert_called_once_with("mm_trap_queue:zset")

def test_clear_queue(queue_manager, redis_manager):
    """Test clearing the entire queue."""
    # Mock successful clear
    redis_manager.delete.return_value = True
    
    # Clear queue
    result = queue_manager.clear_queue()
    assert result is True
    
    # Verify Redis call
    redis_manager.delete.assert_called_once_with("mm_trap_queue:zset")

def test_get_trap_distribution(queue_manager, redis_manager):
    """Test getting trap type distribution."""
    # Mock Redis response with mixed trap types
    mock_traps = [
        json.dumps({"type": "bullish", "confidence": 0.8}),
        json.dumps({"type": "bullish", "confidence": 0.9}),
        json.dumps({"type": "bearish", "confidence": 0.75}),
        json.dumps({"type": "accumulation", "confidence": 0.85})
    ]
    redis_manager.zrange.return_value = mock_traps
    
    # Get distribution
    distribution = queue_manager.get_trap_distribution()
    
    # Verify results
    assert distribution["bullish"] == 2
    assert distribution["bearish"] == 1
    assert distribution["accumulation"] == 1
    
    # Verify Redis call
    redis_manager.zrange.assert_called_once_with(
        "mm_trap_queue:zset",
        0,
        -1,
        desc=True
    ) 