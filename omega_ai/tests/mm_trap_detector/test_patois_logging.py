
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
🎵 PATOIS-INFUSED LOGGING TEST SUITE 🎵
=====================================

Test the Rasta-inspired logging features of the MM Trap Detector.
May your tests reveal the truth of market manipulation! 🌿

JAH BLESS THE TRUTHFUL TESTING! 🙏
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, List
from omega_ai.mm_trap_detector.core.mm_trap_detector import MMTrapDetector, TrapDetection, TrapType
from omega_ai.mm_trap_detector.core.trap_reporter import TrapReporter
from omega_ai.mm_trap_detector.core.patois_logger import PatoisLogger
from omega_ai.mm_trap_detector.core.cosmic_prophecy import CosmicProphecyAnalyzer

# ANSI color codes for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

class TestPatoisLogging:
    """Test suite for Patois-infused logging features."""
    
    @pytest.fixture
    def trap_detector(self) -> MMTrapDetector:
        """Create a trap detector instance."""
        return MMTrapDetector()
    
    @pytest.fixture
    def trap_reporter(self) -> TrapReporter:
        """Create a trap reporter instance."""
        return TrapReporter()
    
    @pytest.fixture
    def patois_logger(self) -> PatoisLogger:
        """Create a Patois logger instance."""
        return PatoisLogger()
    
    @pytest.fixture
    def cosmic_analyzer(self) -> CosmicProphecyAnalyzer:
        """Create a cosmic prophecy analyzer instance."""
        return CosmicProphecyAnalyzer()
    
    @pytest.fixture
    def sample_trap(self) -> TrapDetection:
        """Create a sample trap for testing."""
        return TrapDetection(
            type=TrapType.LIQUIDITY_GRAB,
            price=50000.0,
            volume=100.0,
            confidence=0.85,
            timestamp=datetime.now(),
            metadata={
                "exchange": "binance",
                "symbol": "BTC/USDT",
                "test_data": True
            }
        )
    
    @pytest.mark.asyncio
    async def test_rasta_alert_generation(self, patois_logger: PatoisLogger, sample_trap: TrapDetection) -> None:
        """Test generation of Rasta-style alerts."""
        # Enable Rasta mode
        patois_logger.set_rasta_mode(True)
        
        # Generate alert
        alert = patois_logger.generate_rasta_alert(sample_trap)
        
        # Verify alert format
        assert "🌿" in alert  # Check for Rasta emoji
        assert "JAH" in alert  # Check for spiritual reference
        assert "Babylon" in alert  # Check for market manipulation reference
        assert str(sample_trap.price) in alert  # Check for price inclusion
        assert str(sample_trap.confidence) in alert  # Check for confidence inclusion
    
    @pytest.mark.asyncio
    async def test_weekly_report_generation(self, trap_reporter: TrapReporter, sample_trap: TrapDetection) -> None:
        """Test generation of weekly trap reports."""
        # Create multiple traps over a week
        traps = []
        for i in range(5):
            trap = TrapDetection(
                type=TrapType.LIQUIDITY_GRAB,
                price=50000.0 + i * 1000,
                volume=100.0 + i * 10,
                confidence=0.85 + i * 0.02,
                timestamp=datetime.now() - timedelta(days=i),
                metadata={
                    "exchange": "binance",
                    "symbol": "BTC/USDT",
                    "test_data": True,
                    "sequence": i
                }
            )
            traps.append(trap)
        
        # Generate report
        report = await trap_reporter.generate_weekly_report(traps)
        
        # Verify report content
        assert "Weekly Trap Analysis" in report
        assert "Pattern Evolution" in report
        assert "Market Conditions" in report
        assert "Confidence Trends" in report
        assert "Trap Types" in report
    
    @pytest.mark.asyncio
    async def test_cosmic_prophecy_analysis(self, cosmic_analyzer: CosmicProphecyAnalyzer, sample_trap: TrapDetection) -> None:
        """Test bio-energy based trap analysis."""
        # Analyze trap
        analysis: Dict[str, Any] = await cosmic_analyzer.analyze_trap(sample_trap)
        
        # Verify analysis components
        assert "fibonacci_alignment" in analysis
        assert "babylon_deception" in analysis
        assert "cosmic_prophecy" in analysis
        assert "timestamp" in analysis
        assert "trap_type" in analysis
        
        # Verify score ranges
        assert 0 <= analysis["fibonacci_alignment"] <= 100
        assert 0 <= analysis["babylon_deception"] <= 100
    
    @pytest.mark.asyncio
    async def test_alert_history_management(self, patois_logger: PatoisLogger, sample_trap: TrapDetection) -> None:
        """Test alert history management."""
        # Generate multiple alerts
        alerts = []
        for i in range(3):
            trap = TrapDetection(
                type=TrapType.LIQUIDITY_GRAB,
                price=50000.0 + i * 1000,
                volume=100.0 + i * 10,
                confidence=0.85 + i * 0.02,
                timestamp=datetime.now() - timedelta(hours=i),
                metadata={
                    "exchange": "binance",
                    "symbol": "BTC/USDT",
                    "test_data": True,
                    "sequence": i
                }
            )
            alert = patois_logger.generate_rasta_alert(trap)
            alerts.append(alert)
        
        # Verify history
        history = patois_logger.get_alert_history()
        assert len(history) == 3
        
        # Clear history
        patois_logger.clear_history()
        history = patois_logger.get_alert_history()
        assert len(history) == 0
    
    @pytest.mark.asyncio
    async def test_rasta_mode_toggle(self, patois_logger: PatoisLogger, sample_trap: TrapDetection) -> None:
        """Test Rasta mode toggle functionality."""
        # Initially disabled
        alert = patois_logger.generate_rasta_alert(sample_trap)
        assert "🌿" not in alert
        
        # Enable Rasta mode
        patois_logger.set_rasta_mode(True)
        alert = patois_logger.generate_rasta_alert(sample_trap)
        assert "🌿" in alert
        
        # Disable Rasta mode
        patois_logger.set_rasta_mode(False)
        alert = patois_logger.generate_rasta_alert(sample_trap)
        assert "🌿" not in alert

if __name__ == "__main__":
    print("🚀 Running PATOIS LOGGING Test Suite...")
    pytest.main([__file__, "-v"]) 