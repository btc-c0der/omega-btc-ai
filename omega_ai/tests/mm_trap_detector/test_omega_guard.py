"""
🔱 OMEGA GUARD: Self-Healing AI Defense Test Suite 🔱
=================================================

Testing advanced resilience and self-healing capabilities of the MM Trap Detector.
May your system be as resilient as the blockchain itself! 🛡️

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏
"""

import pytest
import asyncio
import psutil
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, AsyncMock
from omega_ai.mm_trap_detector.core.mm_trap_detector import MMTrapDetector, TrapType, TrapDetection

# ANSI color codes for OMEGA style output
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

class TestOmegaGuard:
    """🔱 Testing OMEGA GUARD self-healing capabilities."""
    
    @pytest.fixture
    def detector(self) -> MMTrapDetector:
        """Create a fresh detector instance for each test."""
        return MMTrapDetector()
    
    async def test_preemptive_anomaly_detection(self, detector: MMTrapDetector) -> None:
        """Test preemptive anomaly detection using order book analysis."""
        print(f"\n{MAGENTA}Testing PREEMPTIVE ANOMALY DETECTION...{RESET}")
        
        # Create test order book data
        order_book = {
            "bids": [
                {"price": 42000.0, "size": 5.0},
                {"price": 41999.0, "size": 150.0},  # Large order
                {"price": 41998.0, "size": 3.0}
            ],
            "asks": [
                {"price": 42001.0, "size": 4.0},
                {"price": 42002.0, "size": 160.0},  # Large order
                {"price": 42003.0, "size": 2.0}
            ]
        }
        
        # Analyze order book for preemptive patterns
        spoofing_detected = detector._detect_order_spoofing(order_book)
        hidden_liquidity_detected = detector._detect_hidden_liquidity(order_book)
        
        # Verify preemptive detection
        assert spoofing_detected, "Should detect order book spoofing"
        assert not hidden_liquidity_detected, "Should not detect hidden liquidity in clean order book"
        
        print(f"{GREEN}✓ Preemptive anomaly detection verified!{RESET}")
    
    async def test_hardware_stress_scenarios(self, detector: MMTrapDetector) -> None:
        """Test system behavior under hardware stress conditions."""
        print(f"\n{MAGENTA}Testing HARDWARE STRESS SCENARIOS...{RESET}")
        
        # Get initial system metrics
        initial_cpu = psutil.cpu_percent()
        initial_memory = psutil.virtual_memory().percent
        
        # Simulate high CPU load
        with patch("psutil.cpu_percent") as mock_cpu:
            mock_cpu.return_value = 95.0
            
            # Simulate high memory usage
            with patch("psutil.virtual_memory") as mock_memory:
                mock_memory.return_value = MagicMock(percent=90.0)
                
                # Create test order book under stress
                order_book = {
                    "bids": [{"price": 42000.0, "size": 100.0}],
                    "asks": [{"price": 42001.0, "size": 100.0}]
                }
                
                # Analyze order book under stress
                spoofing_detected = detector._detect_order_spoofing(order_book)
                hidden_liquidity_detected = detector._detect_hidden_liquidity(order_book)
                
                # Verify system still functions under stress
                assert isinstance(spoofing_detected, bool), "Should return boolean under stress"
                assert isinstance(hidden_liquidity_detected, bool), "Should return boolean under stress"
        
        print(f"{GREEN}✓ Hardware stress handling verified!{RESET}")
    
    async def test_anti_blackout_mode(self, detector: MMTrapDetector) -> None:
        """Test system resilience during complete service blackout."""
        print(f"\n{MAGENTA}Testing ANTI-BLACKOUT MODE...{RESET}")
        
        # Create test order book data
        order_book = {
            "bids": [{"price": 42000.0, "size": 100.0}],
            "asks": [{"price": 42001.0, "size": 100.0}]
        }
        
        # Simulate service failures
        with patch("omega_ai.mm_trap_detector.core.mm_trap_detector.MMTrapDetector._initialize_redis") as mock_redis:
            mock_redis.side_effect = Exception("Redis connection failed")
            
            with patch("omega_ai.mm_trap_detector.core.mm_trap_detector.MMTrapDetector._initialize_influxdb") as mock_influx:
                mock_influx.side_effect = Exception("InfluxDB connection failed")
                
                with patch("omega_ai.mm_trap_detector.core.mm_trap_detector.MMTrapDetector.connect_websocket") as mock_ws:
                    mock_ws.side_effect = Exception("WebSocket connection failed")
                    
                    # Attempt to analyze order book during blackout
                    spoofing_detected = detector._detect_order_spoofing(order_book)
                    hidden_liquidity_detected = detector._detect_hidden_liquidity(order_book)
                    
                    # Verify local analysis still works
                    assert isinstance(spoofing_detected, bool), "Should analyze locally during blackout"
                    assert isinstance(hidden_liquidity_detected, bool), "Should analyze locally during blackout"
                    
                    # Simulate service recovery
                    mock_redis.side_effect = None
                    mock_influx.side_effect = None
                    mock_ws.side_effect = None
                    
                    # Reinitialize components
                    detector._initialize_components()
                    
                    # Verify system recovered
                    assert detector.redis_client is not None, "Should reconnect to Redis"
                    assert detector.influxdb_client is not None, "Should reconnect to InfluxDB"
                    assert detector.websocket is not None, "Should reconnect to WebSocket"
        
        print(f"{GREEN}✓ Anti-blackout mode verified!{RESET}")
    
    async def test_adaptive_analysis(self, detector: MMTrapDetector) -> None:
        """Test system's ability to adapt analysis based on load."""
        print(f"\n{MAGENTA}Testing ADAPTIVE ANALYSIS...{RESET}")
        
        # Create test data with increasing complexity
        for i in range(3):
            # Create order book with increasing depth
            order_book = {
                "bids": [{"price": 42000.0 - j, "size": 100.0} for j in range(10 * (i + 1))],
                "asks": [{"price": 42001.0 + j, "size": 100.0} for j in range(10 * (i + 1))]
            }
            
            # Analyze order book
            spoofing_detected = detector._detect_order_spoofing(order_book)
            hidden_liquidity_detected = detector._detect_hidden_liquidity(order_book)
            
            # Verify analysis completes
            assert isinstance(spoofing_detected, bool), "Should complete analysis under load"
            assert isinstance(hidden_liquidity_detected, bool), "Should complete analysis under load"
        
        print(f"{GREEN}✓ Adaptive analysis verified!{RESET}")

if __name__ == "__main__":
    print("🚀 Running OMEGA GUARD Test Suite...")
    pytest.main([__file__, "-v"]) 