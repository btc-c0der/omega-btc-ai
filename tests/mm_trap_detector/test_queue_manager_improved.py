import pytest
import json
import random
from unittest.mock import MagicMock, patch, call
from datetime import datetime, timezone, timedelta

# Use direct imports rather than trying to access attributes to avoid linter issues
from omega_ai.mm_trap_detector.queue_manager import TrapQueueManager


# ---- Fixtures ----

@pytest.fixture
def mock_redis():
    """Mock Redis connection with all required methods."""
    mock = MagicMock()
    
    # Set up default behavior for all Redis commands used
    mock.zadd.return_value = 1
    mock.zrange.return_value = []
    mock.zcard.return_value = 0
    mock.zremrangebyrank.return_value = 0
    mock.zrem.return_value = 0 
    mock.ping.return_value = True  # Healthy connection
    
    return mock


@pytest.fixture
def queue_manager(mock_redis):
    """Create a trap queue manager with mocked Redis."""
    # Patch the Redis client creation
    with patch('redis.Redis', return_value=mock_redis):
        # Create manager with test settings - don't specify params that will cause linter errors
        manager = TrapQueueManager()
        
        # Explicitly override the attributes we want to test with
        manager.queue_name = "test_mm_trap_queue"
        manager.max_queue_size = 1000
        manager.cleanup_threshold = 1200
        manager.sampling_rate = 1.0  # Full sampling by default
        
        # Use our mock Redis connection
        manager.redis = mock_redis
        
        return manager


# ---- Test Class ----

class TestTrapQueueManager:
    """Tests for the Trap Queue Manager with improved error handling."""
    
    def test_initialization(self, queue_manager, mock_redis):
        """Test queue manager initialization with proper settings."""
        assert queue_manager.queue_name == "test_mm_trap_queue"
        assert queue_manager.max_queue_size == 1000
        assert queue_manager.cleanup_threshold == 1200
        assert queue_manager.sampling_rate == 1.0
        assert queue_manager.redis == mock_redis
    
    def test_add_trap_success(self, queue_manager, mock_redis):
        """Test adding a trap successfully."""
        # Arrange
        trap_data = {
            "type": "Fake Pump",
            "confidence": 0.85,
            "price": 81000,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Act
        result = queue_manager.add_trap(trap_data)
        
        # Assert
        assert result is True
        mock_redis.zadd.assert_called_once()
        # Verify the added data
        zadd_args = mock_redis.zadd.call_args
        assert zadd_args[0][0] == "test_mm_trap_queue"  # Queue name
        # The value should be a dict with JSON string and score
        added_dict = zadd_args[0][1]
        assert len(added_dict) == 1
        
        # The key should be the trap data as JSON
        json_key = list(added_dict.keys())[0]
        parsed_trap = json.loads(json_key)
        assert parsed_trap["type"] == "Fake Pump"
        assert parsed_trap["confidence"] == 0.85
    
    def test_add_trap_with_redis_error(self, queue_manager, mock_redis):
        """Test error handling when Redis fails during trap addition."""
        # Arrange
        trap_data = {
            "type": "Fake Pump",
            "confidence": 0.85,
            "price": 81000
        }
        mock_redis.zadd.side_effect = Exception("Redis connection error")
        
        # Act
        result = queue_manager.add_trap(trap_data)
        
        # Assert
        assert result is False  # Should return False on error
    
    def test_get_traps_success(self, queue_manager, mock_redis):
        """Test successfully retrieving traps from the queue."""
        # Arrange
        mock_traps = [
            json.dumps({"type": "Fake Pump", "confidence": 0.85, "price": 81000}),
            json.dumps({"type": "Liquidity Grab", "confidence": 0.9, "price": 80500})
        ]
        mock_redis.zrange.return_value = mock_traps
        
        # Act
        traps = queue_manager.get_traps(limit=10)
        
        # Assert
        assert len(traps) == 2
        assert isinstance(traps, list)
        assert all(isinstance(trap, dict) for trap in traps)
        assert traps[0]["type"] == "Fake Pump"
        assert traps[1]["type"] == "Liquidity Grab"
        mock_redis.zrange.assert_called_once_with(
            "test_mm_trap_queue", 0, 9, desc=True
        )
    
    def test_get_traps_with_invalid_json(self, queue_manager, mock_redis):
        """Test error handling when traps contain invalid JSON."""
        # Arrange
        mock_traps = [
            json.dumps({"type": "Valid Trap", "confidence": 0.8}),
            "{invalid json",  # Invalid JSON
            json.dumps({"type": "Also Valid", "confidence": 0.7})
        ]
        mock_redis.zrange.return_value = mock_traps
        
        # Act
        traps = queue_manager.get_traps(limit=10)
        
        # Assert - should skip invalid JSON but return valid ones
        assert len(traps) == 2  # Only valid entries
        assert traps[0]["type"] == "Valid Trap"
        assert traps[1]["type"] == "Also Valid"
    
    def test_get_traps_with_redis_error(self, queue_manager, mock_redis):
        """Test error handling when Redis fails during trap retrieval."""
        # Arrange
        mock_redis.zrange.side_effect = Exception("Redis connection error")
        
        # Act
        traps = queue_manager.get_traps(limit=10)
        
        # Assert
        assert traps == []  # Should return empty list on error
    
    def test_cleanup_queue_when_needed(self, queue_manager, mock_redis):
        """Test queue cleanup when size exceeds threshold."""
        # Arrange
        mock_redis.zcard.return_value = 1500  # Over threshold of 1200
        
        # Act
        result = queue_manager.cleanup_queue()
        
        # Assert
        assert result is True
        mock_redis.zremrangebyrank.assert_called_once()
        # Verify we're removing the right number of items (oldest first)
        zrem_args = mock_redis.zremrangebyrank.call_args
        assert zrem_args[0][0] == "test_mm_trap_queue"
        assert zrem_args[0][1] == 0  # Start from 0 (oldest)
        # Should remove items to bring queue back to max_queue_size
        assert zrem_args[0][2] == 499  # Remove 500 items (1500-1000)
    
    def test_cleanup_queue_not_needed(self, queue_manager, mock_redis):
        """Test queue cleanup behavior when size is below threshold."""
        # Arrange
        mock_redis.zcard.return_value = 1000  # At max but below threshold
        
        # Act
        result = queue_manager.cleanup_queue()
        
        # Assert
        assert result is True
        mock_redis.zremrangebyrank.assert_not_called()  # No cleanup needed
    
    def test_cleanup_queue_with_redis_error(self, queue_manager, mock_redis):
        """Test error handling when Redis fails during cleanup."""
        # Arrange
        mock_redis.zcard.return_value = 1500
        mock_redis.zremrangebyrank.side_effect = Exception("Redis error")
        
        # Act
        result = queue_manager.cleanup_queue()
        
        # Assert
        assert result is False  # Should return False on error
    
    def test_sample_traps_full_sampling(self, queue_manager, mock_redis):
        """Test trap sampling with 100% sampling rate."""
        # Arrange
        mock_traps = [
            json.dumps({"type": "Trap 1", "confidence": 0.8}),
            json.dumps({"type": "Trap 2", "confidence": 0.9}),
            json.dumps({"type": "Trap 3", "confidence": 0.7})
        ]
        mock_redis.zrange.return_value = mock_traps
        queue_manager.sampling_rate = 1.0  # 100% sampling
        
        # Act
        sampled_traps = queue_manager.sample_traps(limit=3)
        
        # Assert
        assert len(sampled_traps) == 3  # All traps returned
        assert [trap["type"] for trap in sampled_traps] == ["Trap 1", "Trap 2", "Trap 3"]
    
    def test_sample_traps_partial_sampling(self, queue_manager, mock_redis):
        """Test trap sampling with partial sampling rate."""
        # Arrange
        mock_traps = [
            json.dumps({"type": "Trap 1", "confidence": 0.8}),
            json.dumps({"type": "Trap 2", "confidence": 0.9}),
            json.dumps({"type": "Trap 3", "confidence": 0.7}),
            json.dumps({"type": "Trap 4", "confidence": 0.6})
        ]
        mock_redis.zrange.return_value = mock_traps
        queue_manager.sampling_rate = 0.5  # 50% sampling
        
        # Use a fixed seed for reproducible sampling
        with patch('random.sample') as mock_sample:
            # Simulate sampling behavior
            mock_sample.side_effect = lambda population, k: population[:k]
            
            # Act
            sampled_traps = queue_manager.sample_traps(limit=4)
            
            # Assert - should take 50% of 4 = 2 traps
            assert len(sampled_traps) == 2
            mock_sample.assert_called_once_with(mock_traps, 2)
    
    def test_get_trap_stats_success(self, queue_manager, mock_redis):
        """Test getting accurate trap statistics."""
        # Arrange
        mock_traps = [
            json.dumps({"type": "Fake Pump", "confidence": 0.8}),
            json.dumps({"type": "Fake Pump", "confidence": 0.9}),
            json.dumps({"type": "Liquidity Grab", "confidence": 0.7}),
            json.dumps({"type": "Stop Hunt", "confidence": 0.85})
        ]
        mock_redis.zrange.return_value = mock_traps
        mock_redis.zcard.return_value = 4
        
        # Act
        stats = queue_manager.get_trap_stats()
        
        # Assert
        assert stats["total_traps"] == 4
        assert stats["trap_distribution"]["Fake Pump"] == 2
        assert stats["trap_distribution"]["Liquidity Grab"] == 1
        assert stats["trap_distribution"]["Stop Hunt"] == 1
        assert abs(stats["average_confidence"] - ((0.8 + 0.9 + 0.7 + 0.85) / 4)) < 0.001
    
    def test_get_trap_stats_empty_queue(self, queue_manager, mock_redis):
        """Test getting trap statistics with empty queue."""
        # Arrange
        mock_redis.zrange.return_value = []
        mock_redis.zcard.return_value = 0
        
        # Act
        stats = queue_manager.get_trap_stats()
        
        # Assert
        assert stats["total_traps"] == 0
        assert stats["trap_distribution"] == {}
        assert stats["average_confidence"] == 0
    
    def test_get_trap_stats_with_redis_error(self, queue_manager, mock_redis):
        """Test error handling when Redis fails during stats retrieval."""
        # Arrange
        mock_redis.zrange.side_effect = Exception("Redis connection error")
        
        # Act
        stats = queue_manager.get_trap_stats()
        
        # Assert - should return empty stats
        assert stats["total_traps"] == 0
        assert stats["trap_distribution"] == {}
        assert stats["average_confidence"] == 0
    
    def test_get_recent_traps(self, queue_manager, mock_redis):
        """Test retrieving the most recent traps by timestamp."""
        # Arrange - create traps with different timestamps
        now = datetime.now(timezone.utc)
        old_traps = [
            json.dumps({
                "type": "Old Trap", 
                "confidence": 0.8, 
                "timestamp": (now - timedelta(hours=3)).isoformat()
            })
        ]
        recent_traps = [
            json.dumps({
                "type": "Recent Trap 1", 
                "confidence": 0.85,
                "timestamp": (now - timedelta(minutes=30)).isoformat()
            }),
            json.dumps({
                "type": "Recent Trap 2", 
                "confidence": 0.75,
                "timestamp": (now - timedelta(minutes=15)).isoformat()
            })
        ]
        mock_redis.zrange.return_value = old_traps + recent_traps
        
        # Act - get traps from the last hour
        traps = queue_manager.get_recent_traps(hours=1)
        
        # Assert
        assert len(traps) == 2  # Only the recent ones
        assert traps[0]["type"] == "Recent Trap 1"
        assert traps[1]["type"] == "Recent Trap 2"
    
    def test_health_check_success(self, queue_manager, mock_redis):
        """Test successful health check."""
        # Arrange
        mock_redis.ping.return_value = True
        
        # Act
        is_healthy = queue_manager.health_check()
        
        # Assert
        assert is_healthy is True
        mock_redis.ping.assert_called_once()
    
    def test_health_check_failure(self, queue_manager, mock_redis):
        """Test health check failure."""
        # Arrange
        mock_redis.ping.side_effect = Exception("Redis connection error")
        
        # Act
        is_healthy = queue_manager.health_check()
        
        # Assert
        assert is_healthy is False
        mock_redis.ping.assert_called_once() 