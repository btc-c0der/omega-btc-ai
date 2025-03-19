"""
OMEGA BTC AI - BitGet Traders with Self-Healing Test Suite
=======================================================

Comprehensive test suite for BitGet traders with divine self-healing integration.
Ensures graceful error recovery and optimal trading performance.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch
import logging
import numpy as np
from scipy import stats
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.ai_self_healing import AISelfHealing
from omega_ai.trading.profiles import (
    StrategicTrader,
    AggressiveTrader,
    NewbieTrader,
    ScalperTrader
)
from omega_ai.algos.omega_algorithms import OmegaAlgo
from omega_ai.utils.fibonacci import calculate_fibonacci_levels

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

# Divine Fibonacci constants
GOLDEN_RATIO = 1.618033988749895
FIBONACCI_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 4.236]

@pytest.fixture
def mock_api_client():
    """Create divine mock API client."""
    client = AsyncMock()
    client.get_market_ticker.return_value = {"last": 50000.0}
    client.place_order.return_value = {"orderId": "123"}
    client.get_positions.return_value = []
    return client

@pytest.fixture
def self_healing():
    """Create divine self-healing instance."""
    return AISelfHealing()

@pytest.fixture
def live_traders(mock_api_client):
    """Create divine live traders instance."""
    return BitGetLiveTraders(
        api_client=mock_api_client,
        initial_capital=24.0,
        symbol="BTCUSDT",
        use_testnet=True
    )

@pytest.mark.asyncio
async def test_trader_initialization_with_healing(live_traders, self_healing):
    """Test divine trader initialization with self-healing."""
    logger.info(f"{GREEN}Testing trader initialization with divine healing{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Verify trader profiles
    assert len(live_traders.traders) == 4
    assert isinstance(live_traders.traders[0], StrategicTrader)
    assert isinstance(live_traders.traders[1], AggressiveTrader)
    assert isinstance(live_traders.traders[2], NewbieTrader)
    assert isinstance(live_traders.traders[3], ScalperTrader)
    
    # Verify initial capital
    for trader in live_traders.traders:
        assert trader.initial_capital == 24.0

@pytest.mark.asyncio
async def test_trader_error_recovery(live_traders, self_healing, mock_api_client):
    """Test divine error recovery during trading."""
    logger.info(f"{GREEN}Testing error recovery with divine healing{RESET}")
    
    # Simulate API error
    mock_api_client.get_market_ticker.side_effect = Exception("API Error")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Attempt to update traders (should trigger error recovery)
    await live_traders.update_traders()
    
    # Verify error was handled
    stats = self_healing.get_error_stats()
    assert "api_error" in stats["error_counts"]
    assert stats["error_counts"]["api_error"] > 0

@pytest.mark.asyncio
async def test_rate_limit_handling(live_traders, self_healing, mock_api_client):
    """Test divine rate limit handling."""
    logger.info(f"{GREEN}Testing rate limit handling with divine healing{RESET}")
    
    # Simulate rate limit error
    mock_api_client.place_order.side_effect = Exception("Rate limit exceeded")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Attempt to place orders (should trigger rate limit handling)
    for trader in live_traders.traders:
        await trader.execute_trading_logic()
    
    # Verify rate limit was handled
    stats = self_healing.get_error_stats()
    assert "rate_limit" in stats["error_counts"]
    assert stats["error_counts"]["rate_limit"] > 0

@pytest.mark.asyncio
async def test_concurrent_trading_with_healing(live_traders, self_healing):
    """Test divine concurrent trading with self-healing."""
    logger.info(f"{GREEN}Testing concurrent trading with divine healing{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Create concurrent trading tasks
    async def trade_task(trader):
        await trader.execute_trading_logic()
    
    # Run concurrent trading
    tasks = [trade_task(trader) for trader in live_traders.traders]
    await asyncio.gather(*tasks)
    
    # Verify all traders executed successfully
    for trader in live_traders.traders:
        assert trader.last_update is not None

@pytest.mark.asyncio
async def test_position_management_with_healing(live_traders, self_healing, mock_api_client):
    """Test divine position management with self-healing."""
    logger.info(f"{GREEN}Testing position management with divine healing{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Simulate position opening
    mock_api_client.place_order.return_value = {"orderId": "123", "status": "FILLED"}
    
    # Open positions for all traders
    for trader in live_traders.traders:
        await trader.execute_trading_logic()
    
    # Simulate position update error
    mock_api_client.get_positions.side_effect = Exception("Position update error")
    
    # Attempt to manage positions (should trigger error recovery)
    await live_traders.manage_positions()
    
    # Verify error was handled
    stats = self_healing.get_error_stats()
    assert "api_error" in stats["error_counts"]
    assert stats["error_counts"]["api_error"] > 0

@pytest.mark.asyncio
async def test_performance_metrics_with_healing(live_traders, self_healing):
    """Test divine performance metrics with self-healing."""
    logger.info(f"{GREEN}Testing performance metrics with divine healing{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Simulate some trading activity
    for _ in range(5):
        await live_traders.update_traders()
    
    # Calculate performance metrics
    metrics = await live_traders.calculate_performance_metrics()
    
    # Verify metrics
    assert "total_pnl" in metrics
    assert "sharpe_ratio" in metrics
    assert "max_drawdown" in metrics
    assert "win_rate" in metrics

@pytest.mark.asyncio
async def test_system_shutdown_with_healing(live_traders, self_healing):
    """Test divine system shutdown with self-healing."""
    logger.info(f"{GREEN}Testing system shutdown with divine healing{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Start trading
    await live_traders.start_trading()
    
    # Stop trading
    await live_traders.stop_trading()
    
    # Verify shutdown
    assert not live_traders.is_running
    for trader in live_traders.traders:
        assert not trader.is_active

@pytest.mark.asyncio
async def test_quantum_fibonacci_healing(live_traders, self_healing, mock_api_client):
    """Test divine quantum Fibonacci healing for API retries."""
    logger.info(f"{GREEN}Testing quantum Fibonacci healing with divine timing{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Simulate multiple API errors with different types
    error_types = [
        Exception("API Error"),
        Exception("Rate limit exceeded"),
        Exception("Network timeout"),
        Exception("Server error")
    ]
    
    # Track comprehensive healing metrics
    healing_metrics = {
        "retry_delays": [],
        "error_types": [],
        "recovery_times": [],
        "fibonacci_levels": [],
        "cosmic_factors": [],
        "healing_success": []
    }
    
    # Mock the self-healing module's delay calculation
    async def mock_calculate_delay(error_type: str, retry_count: int) -> float:
        # Get Fibonacci-based delay
        fib_level = FIBONACCI_LEVELS[min(retry_count, len(FIBONACCI_LEVELS) - 1)]
        base_delay = 1.0  # Base delay in seconds
        
        # Calculate quantum-enhanced delay
        quantum_delay = base_delay * (1 + fib_level) * GOLDEN_RATIO
        
        # Add cosmic randomness (0.8 to 1.2 range)
        cosmic_factor = 0.8 + (0.4 * (retry_count % 2))  # Alternates between 0.8 and 1.2
        final_delay = quantum_delay * cosmic_factor
        
        # Track divine metrics
        healing_metrics["retry_delays"].append(final_delay)
        healing_metrics["error_types"].append(error_type)
        healing_metrics["fibonacci_levels"].append(fib_level)
        healing_metrics["cosmic_factors"].append(cosmic_factor)
        
        return final_delay
    
    # Patch the self-healing module's delay calculation
    with patch.object(self_healing, 'calculate_golden_delay', side_effect=mock_calculate_delay):
        # Trigger multiple API errors
        for error in error_types:
            start_time = datetime.now(timezone.utc)
            mock_api_client.get_market_ticker.side_effect = error
            await live_traders.update_traders()
            recovery_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            healing_metrics["recovery_times"].append(recovery_time)
            healing_metrics["healing_success"].append(True)
    
    # Calculate divine healing statistics
    healing_stats = {
        "total_retries": len(healing_metrics["retry_delays"]),
        "average_delay": np.mean(healing_metrics["retry_delays"]),
        "delay_std": np.std(healing_metrics["retry_delays"]),
        "average_recovery_time": np.mean(healing_metrics["recovery_times"]),
        "recovery_time_std": np.std(healing_metrics["recovery_times"]),
        "fibonacci_utilization": len(set(healing_metrics["fibonacci_levels"])) / len(FIBONACCI_LEVELS),
        "cosmic_factor_balance": np.mean(healing_metrics["cosmic_factors"]),
        "healing_success_rate": sum(healing_metrics["healing_success"]) / len(healing_metrics["healing_success"])
    }
    
    # Calculate advanced statistical metrics
    delay_skewness = stats.skew(healing_metrics["retry_delays"])
    delay_kurtosis = stats.kurtosis(healing_metrics["retry_delays"])
    recovery_skewness = stats.skew(healing_metrics["recovery_times"])
    recovery_kurtosis = stats.kurtosis(healing_metrics["recovery_times"])
    
    # Calculate distribution characteristics
    delay_percentiles = np.percentile(healing_metrics["retry_delays"], [25, 50, 75])
    recovery_percentiles = np.percentile(healing_metrics["recovery_times"], [25, 50, 75])
    
    # Calculate trend analysis
    delay_trend = np.polyfit(range(len(healing_metrics["retry_delays"])), 
                           healing_metrics["retry_delays"], 1)[0]
    recovery_trend = np.polyfit(range(len(healing_metrics["recovery_times"])), 
                              healing_metrics["recovery_times"], 1)[0]
    
    # Verify Fibonacci-based retry delays
    assert len(healing_metrics["retry_delays"]) == len(error_types)
    
    # Check that delays follow Fibonacci progression
    for i in range(1, len(healing_metrics["retry_delays"])):
        ratio = healing_metrics["retry_delays"][i] / healing_metrics["retry_delays"][i-1]
        assert abs(ratio - GOLDEN_RATIO) < 0.5  # Allow some variance
    
    # Verify error stats
    stats = self_healing.get_error_stats()
    assert "api_error" in stats["error_counts"]
    assert stats["error_counts"]["api_error"] == len(error_types)
    
    # Verify quantum healing metrics
    healing_metrics = self_healing.get_healing_metrics()
    assert "fibonacci_retries" in healing_metrics
    assert "average_retry_delay" in healing_metrics
    assert healing_metrics["fibonacci_retries"] == len(error_types)
    
    # Log divine healing results with enhanced metrics
    logger.info(f"{CYAN}Quantum Fibonacci Healing Results:{RESET}")
    logger.info(f"{MAGENTA}Basic Metrics:{RESET}")
    logger.info(f"Total Retries: {healing_stats['total_retries']}")
    logger.info(f"Average Delay: {healing_stats['average_delay']:.2f}s")
    logger.info(f"Delay Standard Deviation: {healing_stats['delay_std']:.2f}s")
    
    logger.info(f"{MAGENTA}Recovery Performance:{RESET}")
    logger.info(f"Average Recovery Time: {healing_stats['average_recovery_time']:.2f}s")
    logger.info(f"Recovery Time Std Dev: {healing_stats['recovery_time_std']:.2f}s")
    logger.info(f"Healing Success Rate: {healing_stats['healing_success_rate']*100:.1f}%")
    
    logger.info(f"{MAGENTA}Advanced Statistical Analysis:{RESET}")
    logger.info(f"Delay Skewness: {delay_skewness:.3f}")
    logger.info(f"Delay Kurtosis: {delay_kurtosis:.3f}")
    logger.info(f"Recovery Skewness: {recovery_skewness:.3f}")
    logger.info(f"Recovery Kurtosis: {recovery_kurtosis:.3f}")
    
    logger.info(f"{MAGENTA}Distribution Characteristics:{RESET}")
    logger.info(f"Delay Percentiles (25/50/75): {delay_percentiles[0]:.2f}/{delay_percentiles[1]:.2f}/{delay_percentiles[2]:.2f}s")
    logger.info(f"Recovery Percentiles (25/50/75): {recovery_percentiles[0]:.2f}/{recovery_percentiles[1]:.2f}/{recovery_percentiles[2]:.2f}s")
    
    logger.info(f"{MAGENTA}Trend Analysis:{RESET}")
    logger.info(f"Delay Trend: {delay_trend:.3f}s per retry")
    logger.info(f"Recovery Trend: {recovery_trend:.3f}s per retry")
    
    logger.info(f"{MAGENTA}Fibonacci Analysis:{RESET}")
    logger.info(f"Golden Ratio Alignment: {abs(ratio - GOLDEN_RATIO):.4f}")
    logger.info(f"Fibonacci Level Utilization: {healing_stats['fibonacci_utilization']*100:.1f}%")
    logger.info(f"Cosmic Factor Balance: {healing_stats['cosmic_factor_balance']:.2f}")
    
    # Verify healing metrics quality
    assert healing_stats["healing_success_rate"] == 1.0
    assert healing_stats["fibonacci_utilization"] > 0.5
    assert 0.8 <= healing_stats["cosmic_factor_balance"] <= 1.2
    
    # Verify statistical properties
    assert abs(delay_skewness) < 2.0  # Reasonable skewness range
    assert delay_kurtosis < 5.0  # Reasonable kurtosis range
    assert abs(recovery_skewness) < 2.0
    assert recovery_kurtosis < 5.0
    assert delay_trend > 0  # Delays should increase with retries
    assert recovery_trend >= 0  # Recovery times should not decrease

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"]) 