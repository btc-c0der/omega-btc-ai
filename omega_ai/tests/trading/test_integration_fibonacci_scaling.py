"""
OMEGA BTC AI - Fibonacci Scaling Integration Test
===============================================

This integration test verifies the Fibonacci-based position scaling works accurately
with real-world price calculations and checks for proper placement of orders at
precise Fibonacci levels.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import pytest
import asyncio
import logging
from unittest.mock import patch, AsyncMock, MagicMock
import numpy as np
import json
from datetime import datetime, timezone, timedelta

from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fibonacci constants
GOLDEN_RATIO = 1.618033988749895
FIBONACCI_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618, 4.236]

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class TestFibonacciScalingIntegration:
    """Test Fibonacci-based position scaling with accurate price calculations."""
    
    @pytest.mark.asyncio
    async def test_fibonacci_long_scaling_accuracy(self):
        """Test that long position scaling occurs at precise Fibonacci levels."""
        # Entry price for BTC long position
        entry_price = 42000.0
        
        # Calculate the expected Fibonacci scaling levels for longs
        scaling_levels = []
        for fib_level in [1.618, 2.618, 4.236]:
            # For longs, we scale on dips: entry_price * (1 - 1/fib_level)
            scaling_levels.append(entry_price * (1 - 1/fib_level))
        
        # Print the expected scaling levels
        logger.info(f"{CYAN}BTC Long Position Entry: ${entry_price:.2f}{RESET}")
        logger.info(f"{GREEN}Expected Fibonacci Scaling Levels for Long Position:{RESET}")
        for i, level in enumerate(scaling_levels):
            logger.info(f"  Level {i+1} (1/{[1.618, 2.618, 4.236][i]}): ${level:.2f}")
        
        # Create mocks
        mock_ccxt = AsyncMock(spec=BitGetCCXT)
        mock_mm_detector = AsyncMock()
        mock_mm_detector.analyze_movement = AsyncMock(return_value="Organic Price Movement")
        
        # Set up long position
        mock_ccxt.get_positions = AsyncMock(return_value=[{
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": entry_price,
            "contracts": 0.01,
            "unrealizedPnl": 0.0
        }])
        
        # Set up candles with sufficient volume
        mock_ccxt.get_market_candles = AsyncMock(return_value=[
            [int(datetime.now(timezone.utc).timestamp() * 1000) - 60000, 
             entry_price-100, entry_price+100, entry_price-200, entry_price, 100.0],
            [int(datetime.now(timezone.utc).timestamp() * 1000), 
             entry_price, entry_price+50, entry_price-50, entry_price, 150.0],
        ])
        
        mock_ccxt.place_order = AsyncMock(return_value={"id": "test-order-id"})
        mock_ccxt.sub_account = ""
        
        # Create BitGetLiveTraders instance with mocks
        with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetCCXT', return_value=mock_ccxt), \
             patch('omega_ai.mm_trap_detector.mm_trap_detector.MMTrapDetector', return_value=mock_mm_detector), \
             patch('omega_ai.trading.exchanges.bitget_live_traders.send_telegram_alert', new_callable=AsyncMock):
            
            live_traders = BitGetLiveTraders(
                use_testnet=True,
                initial_capital=24.0,
                symbol="BTCUSDT",
                leverage=11
            )
            live_traders.traders = {"strategic": mock_ccxt}
            
            # Test each Fibonacci level
            for i, level in enumerate(scaling_levels):
                # Reset position additions count
                setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": i})
                
                # Set current price to the Fibonacci level
                mock_ccxt.get_market_ticker = AsyncMock(return_value={"last": level})
                
                # Call _update_trader
                await live_traders._update_trader(mock_ccxt, "strategic")
                
                # Verify order was placed at the correct level
                mock_ccxt.place_order.assert_called_once()
                args, kwargs = mock_ccxt.place_order.call_args_list[-1]
                
                # Check order details
                assert kwargs["side"] == "buy"
                assert kwargs["symbol"] == "BTC/USDT:USDT"
                assert kwargs["order_type"] == "market"
                
                # Reset mock for next iteration
                mock_ccxt.place_order.reset_mock()
    
    @pytest.mark.asyncio
    async def test_fibonacci_short_scaling_accuracy(self):
        """Test that short position scaling occurs at precise Fibonacci levels."""
        # Entry price for BTC short position
        entry_price = 42000.0
        
        # Calculate the expected Fibonacci scaling levels for shorts
        scaling_levels = []
        for fib_level in [1.618, 2.618, 4.236]:
            # For shorts, we scale on pumps: entry_price * (1 + 1/fib_level)
            scaling_levels.append(entry_price * (1 + 1/fib_level))
        
        # Print the expected scaling levels
        logger.info(f"{CYAN}BTC Short Position Entry: ${entry_price:.2f}{RESET}")
        logger.info(f"{GREEN}Expected Fibonacci Scaling Levels for Short Position:{RESET}")
        for i, level in enumerate(scaling_levels):
            logger.info(f"  Level {i+1} ({[1.618, 2.618, 4.236][i]}): ${level:.2f}")
        
        # Create mocks
        mock_ccxt = AsyncMock(spec=BitGetCCXT)
        mock_mm_detector = AsyncMock()
        mock_mm_detector.analyze_movement = AsyncMock(return_value="Organic Price Movement")
        
        # Set up short position
        mock_ccxt.get_positions = AsyncMock(return_value=[{
            "symbol": "BTC/USDT:USDT",
            "side": "short",
            "entryPrice": entry_price,
            "contracts": 0.01,
            "unrealizedPnl": 0.0
        }])
        
        # Set up candles with sufficient volume
        mock_ccxt.get_market_candles = AsyncMock(return_value=[
            [int(datetime.now(timezone.utc).timestamp() * 1000) - 60000, 
             entry_price-100, entry_price+100, entry_price-200, entry_price, 100.0],
            [int(datetime.now(timezone.utc).timestamp() * 1000), 
             entry_price, entry_price+50, entry_price-50, entry_price, 150.0],
        ])
        
        mock_ccxt.place_order = AsyncMock(return_value={"id": "test-order-id"})
        mock_ccxt.sub_account = ""
        
        # Create BitGetLiveTraders instance with mocks
        with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetCCXT', return_value=mock_ccxt), \
             patch('omega_ai.mm_trap_detector.mm_trap_detector.MMTrapDetector', return_value=mock_mm_detector), \
             patch('omega_ai.trading.exchanges.bitget_live_traders.send_telegram_alert', new_callable=AsyncMock):
            
            live_traders = BitGetLiveTraders(
                use_testnet=True,
                initial_capital=24.0,
                symbol="BTCUSDT",
                leverage=11
            )
            live_traders.traders = {"strategic": mock_ccxt}
            
            # Test each Fibonacci level
            for i, level in enumerate(scaling_levels):
                # Reset position additions count
                setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": i})
                
                # Set current price to the Fibonacci level
                mock_ccxt.get_market_ticker = AsyncMock(return_value={"last": level})
                
                # Call _update_trader
                await live_traders._update_trader(mock_ccxt, "strategic")
                
                # Verify order was placed at the correct level
                mock_ccxt.place_order.assert_called_once()
                args, kwargs = mock_ccxt.place_order.call_args_list[-1]
                
                # Check order details
                assert kwargs["side"] == "sell"
                assert kwargs["symbol"] == "BTC/USDT:USDT"
                assert kwargs["order_type"] == "market"
                
                # Reset mock for next iteration
                mock_ccxt.place_order.reset_mock()
    
    @pytest.mark.asyncio
    async def test_dynamic_position_sizing(self):
        """Test that position sizing scales correctly with each addition."""
        # Entry price for BTC position
        entry_price = 42000.0
        
        # Set up initial position size
        initial_position_size = 0.02  # BTC
        
        # Create mocks
        mock_ccxt = AsyncMock(spec=BitGetCCXT)
        mock_mm_detector = AsyncMock()
        mock_mm_detector.analyze_movement = AsyncMock(return_value="Organic Price Movement")
        
        # Set up long position
        mock_ccxt.get_positions = AsyncMock(return_value=[{
            "symbol": "BTC/USDT:USDT",
            "side": "long",
            "entryPrice": entry_price,
            "contracts": initial_position_size,
            "unrealizedPnl": 0.0
        }])
        
        # Set up candles with sufficient volume
        mock_ccxt.get_market_candles = AsyncMock(return_value=[
            [int(datetime.now(timezone.utc).timestamp() * 1000) - 60000, 
             entry_price-100, entry_price+100, entry_price-200, entry_price, 100.0],
            [int(datetime.now(timezone.utc).timestamp() * 1000), 
             entry_price, entry_price+50, entry_price-50, entry_price, 150.0],
        ])
        
        # Calculate first Fibonacci level for long
        fib_level = 1.618
        scale_level = entry_price * (1 - 1/fib_level)
        
        mock_ccxt.get_market_ticker = AsyncMock(return_value={"last": scale_level})
        mock_ccxt.place_order = AsyncMock(return_value={"id": "test-order-id"})
        mock_ccxt.sub_account = ""
        
        # Create BitGetLiveTraders instance with mocks
        with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetCCXT', return_value=mock_ccxt), \
             patch('omega_ai.mm_trap_detector.mm_trap_detector.MMTrapDetector', return_value=mock_mm_detector), \
             patch('omega_ai.trading.exchanges.bitget_live_traders.send_telegram_alert', new_callable=AsyncMock):
            
            live_traders = BitGetLiveTraders(
                use_testnet=True,
                initial_capital=24.0,
                symbol="BTCUSDT",
                leverage=11
            )
            live_traders.traders = {"strategic": mock_ccxt}
            
            # Reset position additions count
            setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": 0})
            
            # Call _update_trader
            await live_traders._update_trader(mock_ccxt, "strategic")
            
            # Verify order was placed with correct size
            mock_ccxt.place_order.assert_called_once()
            args, kwargs = mock_ccxt.place_order.call_args
            
            # Expected size is half of the original position
            expected_size = initial_position_size * 0.5
            assert abs(kwargs["amount"] - expected_size) < 0.0001
            
    @pytest.mark.asyncio
    async def test_scaling_proximity_threshold(self):
        """Test that scaling only happens when price is within proximity threshold."""
        # Entry price for BTC position
        entry_price = 42000.0
        
        # Calculate first Fibonacci level for long
        fib_level = 1.618
        exact_level = entry_price * (1 - 1/fib_level)
        
        # Define test cases with different proximity percentages
        test_cases = [
            {"description": "Exactly at level", "price": exact_level, "expected_order": True},
            {"description": "Within 1% above", "price": exact_level * 1.009, "expected_order": True},
            {"description": "Within 1% below", "price": exact_level * 0.991, "expected_order": True},
            {"description": "Outside threshold above", "price": exact_level * 1.011, "expected_order": False},
            {"description": "Outside threshold below", "price": exact_level * 0.989, "expected_order": False}
        ]
        
        for tc in test_cases:
            logger.info(f"{YELLOW}Testing case: {tc['description']}{RESET}")
            logger.info(f"  Exact level: ${exact_level:.2f}")
            logger.info(f"  Test price: ${tc['price']:.2f}")
            
            # Create mocks
            mock_ccxt = AsyncMock(spec=BitGetCCXT)
            mock_mm_detector = AsyncMock()
            mock_mm_detector.analyze_movement = AsyncMock(return_value="Organic Price Movement")
            
            # Set up long position
            mock_ccxt.get_positions = AsyncMock(return_value=[{
                "symbol": "BTC/USDT:USDT",
                "side": "long",
                "entryPrice": entry_price,
                "contracts": 0.01,
                "unrealizedPnl": 0.0
            }])
            
            # Set up candles with sufficient volume
            mock_ccxt.get_market_candles = AsyncMock(return_value=[
                [int(datetime.now(timezone.utc).timestamp() * 1000) - 60000, 
                 entry_price-100, entry_price+100, entry_price-200, entry_price, 100.0],
                [int(datetime.now(timezone.utc).timestamp() * 1000), 
                 entry_price, entry_price+50, entry_price-50, entry_price, 150.0],
            ])
            
            mock_ccxt.get_market_ticker = AsyncMock(return_value={"last": tc['price']})
            mock_ccxt.place_order = AsyncMock(return_value={"id": "test-order-id"})
            mock_ccxt.sub_account = ""
            
            # Create BitGetLiveTraders instance with mocks
            with patch('omega_ai.trading.exchanges.bitget_live_traders.BitGetCCXT', return_value=mock_ccxt), \
                 patch('omega_ai.mm_trap_detector.mm_trap_detector.MMTrapDetector', return_value=mock_mm_detector), \
                 patch('omega_ai.trading.exchanges.bitget_live_traders.send_telegram_alert', new_callable=AsyncMock):
                
                live_traders = BitGetLiveTraders(
                    use_testnet=True,
                    initial_capital=24.0,
                    symbol="BTCUSDT",
                    leverage=11
                )
                live_traders.traders = {"strategic": mock_ccxt}
                
                # Reset position additions count
                setattr(live_traders, "_strategic_position_additions_count", {"BTC/USDT:USDT": 0})
                
                # Call _update_trader
                await live_traders._update_trader(mock_ccxt, "strategic")
                
                # Verify order placement based on expectation
                if tc['expected_order']:
                    mock_ccxt.place_order.assert_called_once()
                    logger.info(f"{GREEN}✓ Order placed as expected{RESET}")
                else:
                    mock_ccxt.place_order.assert_not_called()
                    logger.info(f"{GREEN}✓ No order placed as expected{RESET}")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"]) 