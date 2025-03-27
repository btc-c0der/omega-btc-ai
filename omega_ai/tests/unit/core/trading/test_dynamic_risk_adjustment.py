"""
OMEGA BTC AI - Dynamic Risk Adjustment Test Suite
==============================================

Test suite for dynamic risk adjustment in volatile market conditions.
Ensures AI adapts leverage and position sizing based on market volatility.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, AsyncMock, patch
import logging
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.profiles import (
    StrategicTrader,
    AggressiveTrader,
    NewbieTrader,
    ScalperTrader
)

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
def mock_volatile_market_data():
    """Create divine mock volatile market data."""
    return {
        "BTCUSDT": {
            "last": 50000.0,
            "bid": 49999.0,
            "ask": 50001.0,
            "volume": 100.0,
            "volatility": 0.05,  # 5% volatility
            "market_regime": "volatile",
            "price_history": [
                {"timestamp": datetime.now(timezone.utc) - timedelta(minutes=i), 
                 "price": 50000.0 * (1 + (0.05 * (i % 2 - 0.5)))}
                for i in range(60)
            ]
        }
    }

@pytest.fixture
def mock_stable_market_data():
    """Create divine mock stable market data."""
    return {
        "BTCUSDT": {
            "last": 50000.0,
            "bid": 49999.0,
            "ask": 50001.0,
            "volume": 100.0,
            "volatility": 0.01,  # 1% volatility
            "market_regime": "stable",
            "price_history": [
                {"timestamp": datetime.now(timezone.utc) - timedelta(minutes=i), 
                 "price": 50000.0 * (1 + (0.01 * (i % 2 - 0.5)))}
                for i in range(60)
            ]
        }
    }

@pytest.mark.asyncio
async def test_volatile_market_leverage_adjustment(live_traders, mock_volatile_market_data):
    """Test divine leverage adjustment in volatile market conditions."""
    logger.info(f"{GREEN}Testing leverage adjustment in volatile market{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Update market data with volatile conditions
    live_traders.market_data = mock_volatile_market_data
    
    # Get initial leverage settings
    initial_leverage = {
        trader.profile_type: trader.leverage 
        for trader in live_traders.traders
    }
    
    # Simulate volatile market conditions
    for _ in range(5):
        await live_traders.update_traders()
    
    # Verify leverage adjustments
    for trader in live_traders.traders:
        # Leverage should be reduced in volatile conditions
        assert trader.leverage <= initial_leverage[trader.profile_type]
        
        # Log the adjustment
        logger.info(f"{CYAN}Profile: {trader.profile_type} | Initial: {initial_leverage[trader.profile_type]}x | Current: {trader.leverage}x{RESET}")

@pytest.mark.asyncio
async def test_stable_market_leverage_restoration(live_traders, mock_volatile_market_data, mock_stable_market_data):
    """Test divine leverage restoration when market stabilizes."""
    logger.info(f"{GREEN}Testing leverage restoration in stable market{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Start with volatile market
    live_traders.market_data = mock_volatile_market_data
    await live_traders.update_traders()
    
    # Record leverage after volatility
    volatile_leverage = {
        trader.profile_type: trader.leverage 
        for trader in live_traders.traders
    }
    
    # Switch to stable market
    live_traders.market_data = mock_stable_market_data
    await live_traders.update_traders()
    
    # Verify leverage restoration
    for trader in live_traders.traders:
        # Leverage should increase in stable conditions
        assert trader.leverage >= volatile_leverage[trader.profile_type]
        
        # Log the restoration
        logger.info(f"{CYAN}Profile: {trader.profile_type} | Volatile: {volatile_leverage[trader.profile_type]}x | Stable: {trader.leverage}x{RESET}")

@pytest.mark.asyncio
async def test_position_size_adjustment(live_traders, mock_volatile_market_data):
    """Test divine position size adjustment in volatile conditions."""
    logger.info(f"{GREEN}Testing position size adjustment in volatile market{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Update market data with volatile conditions
    live_traders.market_data = mock_volatile_market_data
    
    # Get initial position sizes
    initial_sizes = {
        trader.profile_type: trader.position_size 
        for trader in live_traders.traders
    }
    
    # Simulate volatile market conditions
    for _ in range(5):
        await live_traders.update_traders()
    
    # Verify position size adjustments
    for trader in live_traders.traders:
        # Position size should be reduced in volatile conditions
        assert trader.position_size <= initial_sizes[trader.profile_type]
        
        # Log the adjustment
        logger.info(f"{CYAN}Profile: {trader.profile_type} | Initial Size: {initial_sizes[trader.profile_type]} | Current: {trader.position_size}{RESET}")

@pytest.mark.asyncio
async def test_risk_metrics_tracking(live_traders, mock_volatile_market_data):
    """Test divine risk metrics tracking during volatility."""
    logger.info(f"{GREEN}Testing risk metrics tracking in volatile market{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Update market data with volatile conditions
    live_traders.market_data = mock_volatile_market_data
    
    # Simulate volatile market conditions
    for _ in range(5):
        await live_traders.update_traders()
    
    # Verify risk metrics
    for trader in live_traders.traders:
        metrics = trader.calculate_risk_metrics()
        
        # Check essential risk metrics
        assert "volatility" in metrics
        assert "market_regime" in metrics
        assert "risk_score" in metrics
        
        # Log the metrics
        logger.info(f"{CYAN}Profile: {trader.profile_type} | Risk Score: {metrics['risk_score']:.2f} | Market Regime: {metrics['market_regime']}{RESET}")

@pytest.mark.asyncio
async def test_profile_specific_risk_adjustment(live_traders, mock_volatile_market_data):
    """Test divine profile-specific risk adjustments."""
    logger.info(f"{GREEN}Testing profile-specific risk adjustments{RESET}")
    
    # Initialize traders
    await live_traders.initialize_traders()
    
    # Update market data with volatile conditions
    live_traders.market_data = mock_volatile_market_data
    
    # Simulate volatile market conditions
    await live_traders.update_traders()
    
    # Verify profile-specific adjustments
    adjustments = {}
    for trader in live_traders.traders:
        adjustments[trader.profile_type] = {
            "leverage": trader.leverage,
            "position_size": trader.position_size,
            "risk_score": trader.calculate_risk_metrics()["risk_score"]
        }
    
    # Verify different profiles have different risk levels
    assert adjustments["aggressive"]["leverage"] >= adjustments["strategic"]["leverage"]
    assert adjustments["newbie"]["leverage"] <= adjustments["scalper"]["leverage"]
    
    # Log the adjustments
    for profile, metrics in adjustments.items():
        logger.info(f"{CYAN}{profile.title()} | Leverage: {metrics['leverage']}x | Risk Score: {metrics['risk_score']:.2f}{RESET}")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"]) 