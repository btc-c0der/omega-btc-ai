
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
OMEGA BTC AI - Position Scaling Test Suite
=========================================

This test suite validates the position scaling functionality added to the BitGetLiveTraders class.
It tests scaling for both long and short positions at Fibonacci levels, with checks for
market maker traps and volume confirmation.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import Mock, patch, AsyncMock, MagicMock
import logging
import json
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT

# Configure logging
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
def mock_mm_detector():
    """Create a mock MM Trap Detector."""
    with patch('omega_ai.mm_trap_detector.mm_trap_detector.MMTrapDetector') as mock:
        detector = mock.return_value
        detector.analyze_movement = AsyncMock(return_value="Organic Price Movement")
        yield detector

@pytest.fixture
def mock_ccxt():
    """Create a mock BitGetCCXT instance."""
    ccxt = Mock(spec=BitGetCCXT)
    ccxt.get_market_ticker = AsyncMock(return_value={"last": 50000.0})
    ccxt.get_positions = AsyncMock(return_value=[])
    ccxt.get_market_candles = AsyncMock(return_value=[
        # timestamp, open, high, low, close, volume
        [1626912000000, 49000.0, 51000.0, 48000.0, 50000.0, 100.0],
        [1626912060000, 50000.0, 52000.0, 49000.0, 51000.0, 120.0],
    ])
    ccxt.place_order = AsyncMock(return_value={"id": "12345"})
    ccxt.close_position = AsyncMock(return_value={"id": "12345"})
    ccxt.sub_account = ""
    return ccxt

@pytest.fixture
def live_traders(mock_ccxt, mock_mm_detector):
    """Initialize BitGetLiveTraders with mock components."""
    with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetCCXT', return_value=mock_ccxt), \
         patch('omega_ai.trading.exchanges.bitget_live_traders.send_telegram_alert', new_callable=AsyncMock):
        traders = BitGetLiveTraders(
            use_testnet=True,
            initial_capital=24.0,
            symbol="BTCUSDT",
            leverage=11
        )
        traders.traders = {"strategic": mock_ccxt}
        yield traders

class TestPositionScaling:
    """Test position scaling functionality."""
    
    @pytest.mark.asyncio
    async def test_long_position_scaling(self, live_traders, mock_ccxt):
        """Test scaling of a long position at Fibonacci levels."""
        logger.info(f"{GREEN}Testing long position scaling at Fibonacci levels{RESET}")
        
        # Set up a long position
        mock_ccxt.get_positions.return_value = [{
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000.0,
            "contracts": 0.01,
            "unrealizedPnl": 0.0
        }]
        
        # Current price at a Fibonacci scaling level: 50000 * (1 - 1/1.618) = 50000 * 0.382 = 19100
        # (approximately 19000)
        mock_ccxt.get_market_ticker.return_value = {"last": 19100.0}
        
        # Reset position additions count
        setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": 0})
        
        # Call _update_trader
        await live_traders._update_trader(mock_ccxt, "strategic")
        
        # Verify position was scaled (order was placed)
        mock_ccxt.place_order.assert_called_once()
        args, kwargs = mock_ccxt.place_order.call_args
        assert kwargs["side"] == "buy"  # Long position scale should be a buy
        assert kwargs["symbol"] == "BTC/USDT:USDT"
        assert kwargs["order_type"] == "market"
        
        # Verify position additions count was incremented
        assert live_traders._strategic_position_additions_count["BTC/USDT:USDT"] == 1
    
    @pytest.mark.asyncio
    async def test_short_position_scaling(self, live_traders, mock_ccxt):
        """Test scaling of a short position at Fibonacci levels."""
        logger.info(f"{GREEN}Testing short position scaling at Fibonacci levels{RESET}")
        
        # Set up a short position
        mock_ccxt.get_positions.return_value = [{
            "symbol": "BTC/USDT:USDT",
            "side": "short",
            "entryPrice": 50000.0,
            "contracts": 0.01,
            "unrealizedPnl": 0.0
        }]
        
        # Current price at a Fibonacci scaling level: 50000 * (1 + 1/1.618) = 50000 * 1.618 = 80900
        # (approximately 81000)
        mock_ccxt.get_market_ticker.return_value = {"last": 80900.0}
        
        # Reset position additions count
        setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": 0})
        
        # Call _update_trader
        await live_traders._update_trader(mock_ccxt, "strategic")
        
        # Verify position was scaled (order was placed)
        mock_ccxt.place_order.assert_called_once()
        args, kwargs = mock_ccxt.place_order.call_args
        assert kwargs["side"] == "sell"  # Short position scale should be a sell
        assert kwargs["symbol"] == "BTC/USDT:USDT"
        assert kwargs["order_type"] == "market"
        
        # Verify position additions count was incremented
        assert live_traders._strategic_position_additions_count["BTC/USDT:USDT"] == 1
    
    @pytest.mark.asyncio
    async def test_max_position_additions(self, live_traders, mock_ccxt):
        """Test that scaling stops after max additions."""
        logger.info(f"{GREEN}Testing maximum position additions limit{RESET}")
        
        # Set up a long position
        mock_ccxt.get_positions.return_value = [{
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000.0,
            "contracts": 0.01,
            "unrealizedPnl": 0.0
        }]
        
        # Current price at a Fibonacci scaling level
        mock_ccxt.get_market_ticker.return_value = {"last": 19100.0}
        
        # Set position additions count to max (3)
        setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": 3})
        
        # Call _update_trader
        await live_traders._update_trader(mock_ccxt, "strategic")
        
        # Verify position was NOT scaled (no order placed)
        mock_ccxt.place_order.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_position_reset_on_close(self, live_traders, mock_ccxt):
        """Test that position additions count resets when position is closed."""
        logger.info(f"{GREEN}Testing position additions count reset on position close{RESET}")
        
        # Set up a long position
        mock_ccxt.get_positions.return_value = [{
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000.0,
            "contracts": 0.01,
            "unrealizedPnl": 1000.0  # High PnL to trigger close
        }]
        
        # Current price with large gain to trigger close
        mock_ccxt.get_market_ticker.return_value = {"last": 55000.0}
        
        # Set position additions count to 2
        setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": 2})
        
        # Patch _check_position_close to return True (close position)
        with patch.object(live_traders, '_check_position_close', AsyncMock(return_value=True)):
            # Call _update_trader
            await live_traders._update_trader(mock_ccxt, "strategic")
            
            # Verify position was closed
            mock_ccxt.close_position.assert_called_once()
            
            # Verify position additions count was reset
            assert live_traders._strategic_position_additions_count["BTC/USDT:USDT"] == 0
    
    @pytest.mark.asyncio
    async def test_volume_confirmation(self, live_traders, mock_ccxt):
        """Test volume confirmation requirement for scaling."""
        logger.info(f"{GREEN}Testing volume confirmation for position scaling{RESET}")
        
        # Set up a long position
        mock_ccxt.get_positions.return_value = [{
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000.0,
            "contracts": 0.01,
            "unrealizedPnl": 0.0
        }]
        
        # Current price at a Fibonacci scaling level
        mock_ccxt.get_market_ticker.return_value = {"last": 19100.0}
        
        # Set volume data with insufficient increase (only 10% instead of required 20%)
        mock_ccxt.get_market_candles.return_value = [
            [1626912000000, 49000.0, 51000.0, 48000.0, 50000.0, 100.0],
            [1626912060000, 50000.0, 52000.0, 49000.0, 51000.0, 110.0],  # Only 10% increase
        ]
        
        # Reset position additions count
        setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": 0})
        
        # Call _update_trader
        await live_traders._update_trader(mock_ccxt, "strategic")
        
        # Verify position was NOT scaled (no order placed) due to insufficient volume
        mock_ccxt.place_order.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_market_maker_trap_detection(self, live_traders, mock_ccxt, mock_mm_detector):
        """Test market maker trap detection prevents scaling."""
        logger.info(f"{GREEN}Testing market maker trap detection in position scaling{RESET}")
        
        # Set up a long position
        mock_ccxt.get_positions.return_value = [{
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": 50000.0,
            "contracts": 0.01,
            "unrealizedPnl": 0.0
        }]
        
        # Current price at a Fibonacci scaling level
        mock_ccxt.get_market_ticker.return_value = {"last": 19100.0}
        
        # Set volume data with sufficient increase
        mock_ccxt.get_market_candles.return_value = [
            [1626912000000, 49000.0, 51000.0, 48000.0, 50000.0, 100.0],
            [1626912060000, 50000.0, 52000.0, 49000.0, 51000.0, 150.0],  # 50% increase
        ]
        
        # Make MM detector report trap
        mock_mm_detector.analyze_movement.return_value = "Potential market maker trap detected"
        
        # Reset position additions count
        setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": 0})
        
        # Call _update_trader
        with patch('omega_ai.mm_trap_detector.mm_trap_detector.MMTrapDetector', return_value=mock_mm_detector):
            await live_traders._update_trader(mock_ccxt, "strategic")
            
            # Verify position was NOT scaled (no order placed) due to trap detection
            mock_ccxt.place_order.assert_not_called()

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"]) 