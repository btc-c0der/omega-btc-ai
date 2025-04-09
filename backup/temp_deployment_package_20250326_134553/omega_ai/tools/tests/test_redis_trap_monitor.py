"""
Tests for the Redis Trap Monitor module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import datetime
import json
import redis
from omega_ai.tools.redis_trap_monitor import RedisTrapMonitor

@pytest.fixture
def mock_redis():
    """Create a mock Redis instance."""
    mock = Mock()
    mock.scan.return_value = (0, [])  # Empty scan by default
    mock.hgetall.return_value = {}  # Empty hash by default
    return mock

@pytest.fixture
def monitor(mock_redis):
    """Create a RedisTrapMonitor instance with mocked Redis."""
    with patch('redis.Redis', return_value=mock_redis):
        monitor = RedisTrapMonitor(check_interval=1, backfill_minutes=1, verbose=True)
        return monitor

def test_init(monitor):
    """Test monitor initialization."""
    assert monitor.check_interval == 1
    assert monitor.backfill_minutes == 1
    assert monitor.verbose is True
    assert monitor.processed_traps == set()
    assert monitor.running is True
    assert monitor.trap_count == 0

def test_handle_signal(monitor):
    """Test signal handling."""
    monitor.handle_signal(None, None)
    assert monitor.running is False

def test_get_trap_timestamp(monitor):
    """Test timestamp extraction from trap keys."""
    # Valid timestamp
    key = "mm_trap:1647582489"
    timestamp = monitor.get_trap_timestamp(key)
    assert isinstance(timestamp, datetime.datetime)
    assert timestamp.timestamp() == 1647582489
    
    # Invalid timestamp
    key = "mm_trap:invalid"
    timestamp = monitor.get_trap_timestamp(key)
    assert timestamp is None

def test_is_recent_trap(monitor):
    """Test trap recency check."""
    # Recent trap
    key = f"mm_trap:{int(datetime.datetime.now().timestamp())}"
    cutoff = datetime.datetime.now() - datetime.timedelta(minutes=5)
    assert monitor.is_recent_trap(key, cutoff) is True
    
    # Old trap
    key = f"mm_trap:{int((datetime.datetime.now() - datetime.timedelta(hours=1)).timestamp())}"
    assert monitor.is_recent_trap(key, cutoff) is False

def test_find_new_traps(monitor, mock_redis):
    """Test finding new traps in Redis."""
    # Mock Redis scan results
    mock_redis.scan.return_value = (0, ["mm_trap:1", "mm_trap:2"])
    mock_redis.hgetall.side_effect = [
        {"type": "bullish", "confidence": "0.8"},
        {"type": "bearish", "confidence": "0.9"}
    ]
    
    new_traps = monitor.find_new_traps()
    
    assert len(new_traps) == 2
    assert len(monitor.processed_traps) == 2
    assert "mm_trap:1" in monitor.processed_traps
    assert "mm_trap:2" in monitor.processed_traps

def test_process_trap(monitor):
    """Test trap processing and alert sending."""
    with patch('omega_ai.tools.redis_trap_monitor.send_alert') as mock_send_alert:
        key = "mm_trap:1"
        trap_data = {
            "type": "bullish",
            "confidence": "0.8",
            "price": "50000",
            "change": "0.02",
            "timestamp": "2024-03-16T10:00:00Z"
        }
        
        success = monitor.process_trap(key, trap_data)
        
        assert success is True
        assert monitor.trap_count == 1
        mock_send_alert.assert_called_once()

def test_perform_backfill(monitor, mock_redis):
    """Test backfill of recent traps."""
    # Mock Redis scan results with recent and old traps
    current_time = datetime.datetime.now()
    recent_time = int(current_time.timestamp())
    old_time = int((current_time - datetime.timedelta(hours=1)).timestamp())
    
    mock_redis.scan.return_value = (0, [
        f"mm_trap:{recent_time}",
        f"mm_trap:{old_time}"
    ])
    
    mock_redis.hgetall.side_effect = [
        {"type": "recent", "timestamp": current_time.isoformat()},
        {"type": "old", "timestamp": (current_time - datetime.timedelta(hours=1)).isoformat()}
    ]
    
    monitor.perform_backfill()
    
    assert len(monitor.processed_traps) == 2
    assert f"mm_trap:{recent_time}" in monitor.processed_traps
    assert f"mm_trap:{old_time}" in monitor.processed_traps

def test_display_status(monitor, mock_redis, capsys):
    """Test status display."""
    # Mock Redis data
    mock_redis.hgetall.return_value = {
        "type": "bullish",
        "confidence": "0.8",
        "price": "50000"
    }
    
    monitor.display_status()
    
    captured = capsys.readouterr()
    # Strip ANSI color codes for comparison
    output = captured.out.replace('\x1b[', '\\x1b[')
    assert "OMEGA BTC AI TRAP MONITOR" in output
    assert "Monitoring status: ACTIVE" in output

def test_run(monitor, mock_redis):
    """Test main monitor loop."""
    with patch('time.sleep') as mock_sleep:
        # Set up monitor to run for one iteration
        monitor.running = True
        mock_sleep.side_effect = KeyboardInterrupt
        
        # Mock Redis scan results
        mock_redis.scan.return_value = (0, ["mm_trap:1"])
        mock_redis.hgetall.return_value = {
            "type": "bullish",
            "confidence": "0.8",
            "price": "50000"
        }
        
        monitor.run()
        
        assert monitor.running is False
        mock_sleep.assert_called_once()

def test_main():
    """Test main entry point."""
    with patch('omega_ai.tools.redis_trap_monitor.RedisTrapMonitor') as mock_monitor:
        mock_instance = MagicMock()
        mock_monitor.return_value = mock_instance
        
        # Test with default arguments
        with patch('sys.argv', ['redis_trap_monitor.py']):
            from omega_ai.tools.redis_trap_monitor import main
            main()
        
        mock_monitor.assert_called_once_with(
            check_interval=10,
            backfill_minutes=60,
            verbose=False
        )
        mock_instance.run.assert_called_once()

def test_redis_connection_error():
    """Test handling of Redis connection errors."""
    with patch('redis.Redis', side_effect=redis.ConnectionError):
        with pytest.raises(SystemExit):
            from omega_ai.tools.redis_trap_monitor import main
            main() 