"""
OMEGA BTC AI - AI Self-Healing Test Suite
=======================================

Comprehensive test suite for the divine self-healing system.
Ensures flawless error recovery and golden ratio timing.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock
import logging
from omega_ai.trading.exchanges.ai_self_healing import AISelfHealing

# Configure divine logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Terminal colors for blessed output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

@pytest.fixture
def self_healing():
    """Create divine self-healing instance."""
    return AISelfHealing()

@pytest.mark.asyncio
async def test_golden_delay_calculation(self_healing):
    """Test divine golden ratio delay calculation."""
    logger.info(f"{GREEN}Testing golden ratio delay calculation{RESET}")
    
    # Test initial delay
    assert self_healing.calculate_golden_delay(0) == 1.0
    
    # Test increasing delays
    delays = [self_healing.calculate_golden_delay(i) for i in range(5)]
    assert all(delays[i] < delays[i+1] for i in range(len(delays)-1))
    assert all(delay <= 60.0 for delay in delays)

@pytest.mark.asyncio
async def test_error_handling(self_healing):
    """Test divine error handling."""
    logger.info(f"{GREEN}Testing error handling with divine energy{RESET}")
    
    # Mock error and context
    error = Exception("Test error")
    context = {"operation": "test"}
    
    # Handle error
    should_retry = await self_healing.handle_error("test_error", error, context)
    
    assert should_retry is True
    assert self_healing.error_counts["test_error"] == 1

@pytest.mark.asyncio
async def test_max_retries(self_healing):
    """Test divine maximum retry limit."""
    logger.info(f"{GREEN}Testing maximum retry limit{RESET}")
    
    error = Exception("Test error")
    context = {"operation": "test"}
    
    # Exceed max retries
    for _ in range(9):  # MAX_RETRIES + 1
        should_retry = await self_healing.handle_error("max_retries", error, context)
    
    assert should_retry is False
    assert self_healing.error_counts["max_retries"] == 8

@pytest.mark.asyncio
async def test_recovery_strategy(self_healing):
    """Test divine recovery strategy execution."""
    logger.info(f"{GREEN}Testing recovery strategy execution{RESET}")
    
    # Mock recovery strategy
    mock_strategy = AsyncMock()
    self_healing.register_recovery_strategy("test_strategy", mock_strategy)
    
    # Handle error with strategy
    await self_healing.handle_error("test_strategy", Exception(), {"test": "data"})
    
    mock_strategy.assert_called_once_with({"test": "data"})

@pytest.mark.asyncio
async def test_error_stats(self_healing):
    """Test divine error statistics collection."""
    logger.info(f"{GREEN}Testing error statistics collection{RESET}")
    
    # Generate some errors
    error = Exception("Test error")
    context = {"operation": "test"}
    
    await self_healing.handle_error("stats_test", error, context)
    await self_healing.handle_error("stats_test", error, context)
    
    stats = self_healing.get_error_stats()
    
    assert stats["error_counts"]["stats_test"] == 2
    assert "stats_test" in stats["last_retry_times"]

@pytest.mark.asyncio
async def test_error_count_reset(self_healing):
    """Test divine error count reset."""
    logger.info(f"{GREEN}Testing error count reset{RESET}")
    
    # Generate error
    await self_healing.handle_error("reset_test", Exception(), {})
    
    # Reset count
    self_healing.reset_error_count("reset_test")
    
    assert self_healing.error_counts["reset_test"] == 0

@pytest.mark.asyncio
async def test_concurrent_error_handling(self_self_healing):
    """Test divine concurrent error handling."""
    logger.info(f"{GREEN}Testing concurrent error handling{RESET}")
    
    # Create multiple concurrent error handlers
    async def handle_error(error_type: str):
        await self_healing.handle_error(error_type, Exception(), {})
    
    # Run concurrent error handlers
    tasks = [
        handle_error(f"concurrent_{i}")
        for i in range(3)
    ]
    
    await asyncio.gather(*tasks)
    
    # Verify all errors were handled
    for i in range(3):
        assert self_healing.error_counts[f"concurrent_{i}"] == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"]) 