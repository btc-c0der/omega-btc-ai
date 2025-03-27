import pytest
import json
from unittest.mock import MagicMock, patch
from omega_ai.mm_trap_detector.queue_manager import TrapQueueManager

@pytest.fixture
def queue_manager():
    """Create a trap queue manager with mocked dependencies."""
    with patch('redis.Redis', MagicMock()):
        manager = TrapQueueManager(
            queue_name="mm_trap_queue:zset",
            redis_host="localhost",
            redis_port=6379
        )
        manager.redis = MagicMock()
        return manager

class TestTrapQueueManager:
    """Tests for the Trap Queue Manager component."""
    
    def test_init(self, queue_manager):
        """Test initialization of the queue manager."""
        assert queue_manager.queue_name == "mm_trap_queue:zset"
        assert queue_manager.max_queue_size == 50000
        assert queue_manager.cleanup_threshold == 60000
        assert queue_manager.sampling_rate == 1.0
    
    def test_add_trap(self, queue_manager):
        """Test adding a trap to the queue."""
        # Arrange
        trap_data = {
            "type": "Fake Pump",
            "confidence": 0.85,
            "price": 81000,
            "timestamp": "2023-06-15T10:30:00Z"
        }
        
        # Act
        result = queue_manager.add_trap(trap_data)
        
        # Assert
        assert result is True
        queue_manager.redis.zadd.assert_called_once()
        args, kwargs = queue_manager.redis.zadd.call_args
        assert args[0] == "mm_trap_queue:zset"
        assert isinstance(args[1], dict)
        assert len(args[1]) == 1
        # The value should be a JSON string of our trap data
        key = list(args[1].keys())[0]
        assert json.loads(key)["type"] == "Fake Pump"
    
    def test_get_traps(self, queue_manager):
        """Test retrieving traps from the queue."""
        # Arrange
        mock_traps = [
            json.dumps({"type": "Fake Pump", "confidence": 0.85}),
            json.dumps({"type": "Liquidity Grab", "confidence": 0.9})
        ]
        queue_manager.redis.zrange.return_value = mock_traps
        
        # Act
        traps = queue_manager.get_traps(limit=10)
        
        # Assert
        assert len(traps) == 2
        assert traps[0]["type"] == "Fake Pump"
        assert traps[1]["type"] == "Liquidity Grab"
        queue_manager.redis.zrange.assert_called_once_with(
            "mm_trap_queue:zset", 0, 9, desc=True
        )
    
    def test_cleanup_queue(self, queue_manager):
        """Test queue cleanup functionality."""
        # Arrange
        queue_manager.redis.zcard.return_value = 70000  # Over threshold
        
        # Act
        result = queue_manager.cleanup_queue()
        
        # Assert
        assert result is True
        queue_manager.redis.zremrangebyrank.assert_called_once_with(
            "mm_trap_queue:zset", 0, 19999  # Remove oldest 20k items
        )
    
    def test_sample_traps(self, queue_manager):
        """Test trap sampling functionality."""
        # Arrange
        mock_traps = [
            json.dumps({"type": "Fake Pump", "confidence": 0.85, "timestamp": "2023-06-15T10:30:00Z"}),
            json.dumps({"type": "Liquidity Grab", "confidence": 0.9, "timestamp": "2023-06-15T10:35:00Z"}),
            json.dumps({"type": "Stop Hunt", "confidence": 0.75, "timestamp": "2023-06-15T10:40:00Z"})
        ]
        queue_manager.redis.zrange.return_value = mock_traps
        queue_manager.sampling_rate = 0.66  # Sample 2/3 of traps
        
        # Act
        sampled_traps = queue_manager.sample_traps(limit=3)
        
        # Assert
        assert len(sampled_traps) == 2  # 3 * 0.66 = ~2
        for trap in sampled_traps:
            assert isinstance(trap, dict)
            assert "type" in trap
            assert "confidence" in trap
    
    def test_get_trap_stats(self, queue_manager):
        """Test getting trap statistics."""
        # Arrange
        mock_traps = [
            json.dumps({"type": "Fake Pump", "confidence": 0.85}),
            json.dumps({"type": "Fake Pump", "confidence": 0.9}),
            json.dumps({"type": "Liquidity Grab", "confidence": 0.75})
        ]
        queue_manager.redis.zrange.return_value = mock_traps
        
        # Act
        stats = queue_manager.get_trap_stats()
        
        # Assert
        assert stats["total_traps"] == 3
        assert stats["average_confidence"] == (0.85 + 0.9 + 0.75) / 3
        assert stats["trap_distribution"]["Fake Pump"] == 2
        assert stats["trap_distribution"]["Liquidity Grab"] == 1
        
    def test_queue_empty(self, queue_manager):
        """Test behavior when queue is empty."""
        # Arrange
        queue_manager.redis.zrange.return_value = []
        queue_manager.redis.zcard.return_value = 0
        
        # Act
        traps = queue_manager.get_traps()
        stats = queue_manager.get_trap_stats()
        
        # Assert
        assert traps == []
        assert stats["total_traps"] == 0
        assert stats["average_confidence"] == 0 