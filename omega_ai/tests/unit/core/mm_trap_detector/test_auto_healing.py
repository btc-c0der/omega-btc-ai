"""
🔄 AUTO-HEALING TEST SUITE 🔄
============================

Testing the auto-healing capabilities of the MM Trap Detector.
May your system be resilient and self-healing! 🛡️

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.frames import Close
from omega_ai.mm_trap_detector.core.mm_trap_detector import MMTrapDetector
import redis

# ANSI color codes for h4x0r style output
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

class TestAutoHealing:
    """🛡️ Testing auto-healing capabilities."""
    
    @pytest.fixture
    def detector(self) -> MMTrapDetector:
        """Create a fresh detector instance for each test."""
        return MMTrapDetector()
    
    @pytest.mark.asyncio
    async def test_websocket_auto_healing(self, detector: MMTrapDetector) -> None:
        """Test WebSocket connection auto-healing."""
        print(f"\n{MAGENTA}Testing WEBSOCKET AUTO-HEALING...{RESET}")
        
        # Simulate connection failure
        with patch('websockets.client.connect') as mock_connect:
            # First attempt fails
            mock_connect.side_effect = [
                ConnectionClosedError(Close(1000, "Connection closed"), Close(1000, "Connection closed")),
                ConnectionClosedOK(Close(1000, "Connection closed"), Close(1000, "Connection closed")),
                None  # Third attempt succeeds
            ]
            
            # Attempt to connect
            await detector.connect_websocket()
            
            # Verify reconnection attempts
            assert mock_connect.call_count >= 2, "Should attempt reconnection"
            print(f"{GREEN}✓ WebSocket auto-healing verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_redis_connection_healing(self, detector: MMTrapDetector) -> None:
        """Test Redis connection auto-healing."""
        print(f"\n{MAGENTA}Testing REDIS AUTO-HEALING...{RESET}")
        
        # Simulate Redis connection failure
        with patch('redis.Redis.ping') as mock_ping:
            # First attempt fails
            mock_ping.side_effect = [
                redis.ConnectionError("Connection failed"),
                True  # Second attempt succeeds
            ]
            
            # Attempt to connect
            detector._initialize_redis()
            
            # Verify reconnection attempts
            assert mock_ping.call_count >= 2, "Should attempt reconnection"
            print(f"{GREEN}✓ Redis auto-healing verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_influxdb_connection_healing(self, detector: MMTrapDetector) -> None:
        """Test InfluxDB connection auto-healing."""
        print(f"\n{MAGENTA}Testing INFLUXDB AUTO-HEALING...{RESET}")
        
        # Simulate InfluxDB connection failure
        with patch('influxdb_client.InfluxDBClient.ping') as mock_ping:
            # First attempt fails
            mock_ping.side_effect = [
                Exception("Connection failed"),
                True  # Second attempt succeeds
            ]
            
            # Attempt to connect
            detector._initialize_influxdb()
            
            # Verify reconnection attempts
            assert mock_ping.call_count >= 2, "Should attempt reconnection"
            print(f"{GREEN}✓ InfluxDB auto-healing verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_data_consistency_recovery(self, detector: MMTrapDetector) -> None:
        """Test recovery from data inconsistency."""
        print(f"\n{MAGENTA}Testing DATA CONSISTENCY RECOVERY...{RESET}")
        
        # Simulate data corruption
        with patch('redis.Redis.get') as mock_get:
            # Return corrupted data
            mock_get.side_effect = [
                "invalid_data",
                "50000.0"  # Valid data on retry
            ]
            
            # Attempt to read data
            price = detector.last_price
            
            # Verify data recovery
            assert price == 50000.0, "Should recover valid data"
            print(f"{GREEN}✓ Data consistency recovery verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_threshold_recalculation_recovery(self, detector: MMTrapDetector) -> None:
        """Test recovery from threshold calculation errors."""
        print(f"\n{MAGENTA}Testing THRESHOLD RECALCULATION RECOVERY...{RESET}")
        
        # Simulate calculation error
        with patch('omega_ai.mm_trap_detector.core.mm_trap_detector.MMTrapDetector._detect_order_spoofing') as mock_detect:
            # First attempt fails
            mock_detect.side_effect = [
                ValueError("Invalid calculation"),
                False  # Valid result on retry
            ]
            
            # Attempt to analyze order book
            result = detector.analyze_order_book({"bids": [], "asks": []})
            
            # Verify recovery
            assert result is False, "Should recover valid result"
            print(f"{GREEN}✓ Threshold recalculation recovery verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_state_restoration_after_crash(self, detector: MMTrapDetector) -> None:
        """Test state restoration after system crash."""
        print(f"\n{MAGENTA}Testing STATE RESTORATION AFTER CRASH...{RESET}")
        
        # Simulate system crash
        with patch('redis.Redis.get') as mock_get, \
             patch('redis.Redis.set') as mock_set:
            # Simulate crash during state save
            mock_set.side_effect = [
                redis.ConnectionError("Connection lost"),
                True  # Success on retry
            ]
            
            # Attempt to save and restore state
            detector._initialize_components()
            
            # Verify state restoration
            assert mock_set.call_count >= 2, "Should attempt state restoration"
            print(f"{GREEN}✓ State restoration after crash verified!{RESET}")

if __name__ == "__main__":
    print("🚀 Running AUTO-HEALING Test Suite...")
    pytest.main([__file__, "-v"]) 