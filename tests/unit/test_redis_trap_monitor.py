import pytest
import json
import os
import sys
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timedelta

# Import the module to test
from omega_ai.tools.redis_trap_monitor import RedisTrapMonitor

class TestRedisTrapMonitor:
    """Test suite for RedisTrapMonitor class"""
    
    def test_initialization(self, mock_redis):
        """Test basic initialization of RedisTrapMonitor"""
        # Mock Redis connection
        with patch('redis.Redis', return_value=mock_redis):
            # Create monitor instance
            monitor = RedisTrapMonitor(check_interval=5, backfill_minutes=30, verbose=True)
            
            # Check instance attributes
            assert monitor.check_interval == 5
            assert monitor.backfill_minutes == 30
            assert monitor.verbose is True
            assert monitor.processed_traps == set()
            assert monitor.running is True
            assert monitor.trap_count == 0
    
    def test_get_trap_timestamp(self):
        """Test extraction of timestamp from trap key"""
        monitor = RedisTrapMonitor()
        
        # Test with valid key
        valid_key = "mm_trap:1647582489"
        timestamp = monitor.get_trap_timestamp(valid_key)
        assert isinstance(timestamp, datetime)
        assert timestamp.year >= 2022  # Basic sanity check
        
        # Test with invalid key
        invalid_key = "invalid_key"
        assert monitor.get_trap_timestamp(invalid_key) is None
    
    def test_is_recent_trap(self):
        """Test identification of recent traps"""
        monitor = RedisTrapMonitor()
        
        # Create a cutoff time
        cutoff_time = datetime.now() - timedelta(minutes=30)
        
        # Test with recent trap (after cutoff)
        recent_timestamp = int(datetime.now().timestamp())
        recent_key = f"mm_trap:{recent_timestamp}"
        assert monitor.is_recent_trap(recent_key, cutoff_time) is True
        
        # Test with old trap (before cutoff)
        old_timestamp = int((datetime.now() - timedelta(hours=1)).timestamp())
        old_key = f"mm_trap:{old_timestamp}"
        assert monitor.is_recent_trap(old_key, cutoff_time) is False
    
    def test_find_new_traps(self, mock_redis):
        """Test finding new traps in Redis"""
        # Instead of mocking scan, directly seed the redis with the keys we want
        mock_redis.hset("mm_trap:1", mapping={"type": "Bull Trap", "confidence": "0.8"})
        mock_redis.hset("mm_trap:2", mapping={"type": "Bear Trap", "confidence": "0.7"})
        
        # Use patch to replace scan method to return our test keys
        with patch.object(mock_redis, 'scan', return_value=(0, ["mm_trap:1", "mm_trap:2"])):
            # Create monitor with our seeded redis
            with patch('redis.Redis', return_value=mock_redis):
                monitor = RedisTrapMonitor()
                monitor.redis = mock_redis
                
                # First call should find both traps
                traps = monitor.find_new_traps()
                assert len(traps) == 2
                assert traps[0][0] == "mm_trap:1"
                assert traps[1][0] == "mm_trap:2"
                
                # Second call should find no new traps (they're now in processed_traps)
                traps = monitor.find_new_traps()
                assert len(traps) == 0
    
    @patch('omega_ai.tools.redis_trap_monitor.send_alert')
    def test_process_trap(self, mock_send_alert, mock_redis):
        """Test processing a trap and sending an alert"""
        # Create sample trap data
        trap_key = "mm_trap:1647582489"
        trap_data = {
            "type": "Liquidity Grab",
            "confidence": "0.85",
            "price": "85000",
            "change": "0.02",
            "timestamp": datetime.now().isoformat()
        }
        
        # Create monitor with mock dependencies
        with patch('redis.Redis', return_value=mock_redis):
            monitor = RedisTrapMonitor()
            monitor.redis = mock_redis
            
            # Process the trap
            result = monitor.process_trap(trap_key, trap_data)
            
            # Check alert was sent with correct data
            assert result is True
            mock_send_alert.assert_called_once()
            
            # Check trap count was incremented
            assert monitor.trap_count == 1
    
    def test_perform_backfill(self, mock_redis):
        """Test backfilling of recent traps at startup"""
        # Setup test data
        recent_timestamp = int(datetime.now().timestamp())
        old_timestamp = int((datetime.now() - timedelta(hours=2)).timestamp())
        
        # Seed the redis with our test data
        mock_redis.hset(f"mm_trap:{recent_timestamp}", mapping={"type": "Bull Trap", "confidence": "0.8"})
        mock_redis.hset(f"mm_trap:{old_timestamp}", mapping={"type": "Bear Trap", "confidence": "0.7"})
        
        scan_result = (0, [f"mm_trap:{recent_timestamp}", f"mm_trap:{old_timestamp}"])
        
        # Create monitor with mock redis and patch process_trap and scan
        with patch.object(mock_redis, 'scan', return_value=scan_result):
            with patch('redis.Redis', return_value=mock_redis):
                with patch.object(RedisTrapMonitor, 'process_trap', return_value=True) as mock_process:
                    monitor = RedisTrapMonitor(backfill_minutes=60, verbose=True)
                    monitor.redis = mock_redis
                    
                    # Perform backfill
                    monitor.perform_backfill()
                    
                    # Only the recent trap should be processed
                    assert len(monitor.processed_traps) == 2  # Both should be marked as processed
                    assert mock_process.call_count == 1  # But only one processed due to backfill time
    
    @patch('os.system')
    def test_display_status(self, mock_system, mock_redis):
        """Test status display functionality"""
        # Setup test data directly in the redis
        mock_redis.hset("mm_trap:1", mapping={"type": "Bull Trap", "confidence": "0.8", "price": "85000"})
        
        # Use a real redis operation instead of mocking hgetall
        with patch('redis.Redis', return_value=mock_redis):
            # Create monitor with processed traps
            monitor = RedisTrapMonitor(verbose=True)
            monitor.redis = mock_redis
            monitor.processed_traps = ["mm_trap:1"]
            monitor.trap_count = 1
            
            # Call method to test
            monitor.display_status()
            
            # Verify system clear and print calls
            mock_system.assert_called_once_with('clear')
    
    def test_handle_signal(self):
        """Test signal handling for graceful termination"""
        monitor = RedisTrapMonitor()
        assert monitor.running is True
        
        # Simulate SIGINT
        monitor.handle_signal(None, None)
        
        # Check monitor is no longer running
        assert monitor.running is False 