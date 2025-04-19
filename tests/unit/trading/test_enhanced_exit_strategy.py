#!/usr/bin/env python3

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
Test suite for the Enhanced Exit Strategy.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json
from datetime import datetime

from omega_ai.trading.strategies.enhanced_exit_strategy import EnhancedExitStrategy

@pytest.fixture
def exit_strategy():
    """Create an EnhancedExitStrategy instance with mocked Redis."""
    with patch('redis.Redis') as mock_redis:
        # Setup mock Redis instance
        mock_redis_instance = MagicMock()
        mock_redis_instance.get = MagicMock(return_value=None)
        mock_redis.return_value = mock_redis_instance
        
        strategy = EnhancedExitStrategy(
            base_risk_percent=1.0,
            enable_scalping=True,
            scalping_coefficient=0.3,
            strategic_coefficient=0.6,
            aggressive_coefficient=0.1
        )
        
        yield strategy, mock_redis_instance

def test_initialization(exit_strategy):
    """Test that EnhancedExitStrategy initializes correctly."""
    strategy, _ = exit_strategy
    
    assert strategy.base_risk_percent == 1.0
    assert strategy.enable_scalping is True
    assert strategy.scalping_coefficient == 0.3
    assert strategy.strategic_coefficient == 0.6
    assert strategy.aggressive_coefficient == 0.1
    assert len(strategy.fib_levels) > 0
    assert strategy.active_positions == {}
    assert strategy.trailing_stops == {}

def test_calculate_fib_take_profits(exit_strategy):
    """Test Fibonacci take profit calculation."""
    strategy, _ = exit_strategy
    
    # Test long position
    take_profits = strategy._calculate_fib_take_profits(
        entry_price=50000.0,
        stop_loss=49000.0,
        direction='long',
        leverage=5.0
    )
    
    assert len(take_profits) > 0
    assert all('price' in tp for tp in take_profits)
    assert all('percentage' in tp for tp in take_profits)
    assert all('fib_level' in tp for tp in take_profits)
    assert all(tp['price'] > 50000.0 for tp in take_profits)  # All TPs above entry for long
    
    # Test short position
    take_profits = strategy._calculate_fib_take_profits(
        entry_price=50000.0,
        stop_loss=51000.0,
        direction='short',
        leverage=5.0
    )
    
    assert len(take_profits) > 0
    assert all('price' in tp for tp in take_profits)
    assert all('percentage' in tp for tp in take_profits)
    assert all('fib_level' in tp for tp in take_profits)
    assert all(tp['price'] < 50000.0 for tp in take_profits)  # All TPs below entry for short

def test_apply_scalping_influence(exit_strategy):
    """Test scalping influence on take profits."""
    strategy, _ = exit_strategy
    
    original_take_profits = [
        {"price": 51000.0, "percentage": 40, "fib_level": 0.618},
        {"price": 52000.0, "percentage": 30, "fib_level": 1.0},
        {"price": 53000.0, "percentage": 30, "fib_level": 1.618}
    ]
    
    modified_tps = strategy._apply_scalping_influence(
        original_take_profits,
        'long',
        50000.0
    )
    
    assert len(modified_tps) == len(original_take_profits)
    assert modified_tps[0]["percentage"] > original_take_profits[0]["percentage"]
    assert modified_tps[0]["price"] < original_take_profits[0]["price"]  # Moved closer
    assert sum(tp["percentage"] for tp in modified_tps) <= 100  # Total <= 100%

@pytest.mark.asyncio
async def test_update_trailing_stop(exit_strategy):
    """Test trailing stop updates."""
    strategy, _ = exit_strategy
    
    # Setup test position
    position_id = "test_position"
    strategy.active_positions[position_id] = {
        'entry_price': 50000.0,
        'direction': 'long',
        'size': 0.1,
        'leverage': 5.0,
        'stop_loss': 49000.0,
        'take_profits': [],
        'initial_stop': 49000.0,
        'trailing_activated': False,
        'partial_exits': []
    }
    
    # Test activation threshold
    new_stop = await strategy.update_trailing_stop(position_id, 50500.0)  # 1% profit
    assert new_stop == 49000.0  # Not activated yet
    
    # Test trailing activation
    new_stop = await strategy.update_trailing_stop(position_id, 51000.0)  # 2% profit
    assert strategy.active_positions[position_id]['trailing_activated']
    assert new_stop > 49000.0  # Stop moved up
    
    # Test trailing continues
    previous_stop = new_stop
    new_stop = await strategy.update_trailing_stop(position_id, 51500.0)
    assert new_stop > previous_stop  # Stop continues moving up

@pytest.mark.asyncio
async def test_check_exit_conditions(exit_strategy):
    """Test exit condition checking."""
    strategy, mock_redis = exit_strategy
    
    # Setup test position
    position_id = "test_position"
    strategy.active_positions[position_id] = {
        'entry_price': 50000.0,
        'direction': 'long',
        'size': 0.1,
        'leverage': 5.0,
        'stop_loss': 49000.0,
        'take_profits': [
            {"price": 51000.0, "percentage": 50, "fib_level": 0.618},
            {"price": 52000.0, "percentage": 50, "fib_level": 1.0}
        ],
        'initial_stop': 49000.0,
        'trailing_activated': False,
        'partial_exits': []
    }
    
    # Test stop loss hit
    should_exit, exit_info = await strategy.check_exit_conditions(position_id, 48900.0)
    assert should_exit
    assert exit_info['reason'] == 'stop_loss'
    assert exit_info['percentage'] == 100
    
    # Test take profit hit
    should_exit, exit_info = await strategy.check_exit_conditions(position_id, 51100.0)
    assert should_exit
    assert exit_info['reason'] == 'take_profit'
    assert exit_info['percentage'] == 50
    
    # Test trap detection exit
    mock_redis.get.return_value = json.dumps({
        'probability': 0.85,
        'trap_type': 'bull_trap'
    })
    
    should_exit, exit_info = await strategy.check_exit_conditions(position_id, 50500.0)
    assert should_exit
    assert exit_info['reason'] == 'trap_detected'
    assert 'trap_type' in exit_info

@pytest.mark.asyncio
async def test_process_partial_exit(exit_strategy):
    """Test partial exit processing."""
    strategy, _ = exit_strategy
    
    # Setup test position
    position_id = "test_position"
    strategy.active_positions[position_id] = {
        'entry_price': 50000.0,
        'direction': 'long',
        'size': 0.1,
        'leverage': 5.0,
        'stop_loss': 49000.0,
        'take_profits': [
            {"price": 51000.0, "percentage": 50, "fib_level": 0.618},
            {"price": 52000.0, "percentage": 50, "fib_level": 1.0}
        ],
        'initial_stop': 49000.0,
        'trailing_activated': False,
        'partial_exits': []
    }
    
    # Test partial take profit exit
    exit_info = {
        'reason': 'take_profit',
        'price': 51000.0,
        'percentage': 50,
        'fib_level': 0.618
    }
    
    is_closed = await strategy.process_partial_exit(position_id, exit_info)
    assert not is_closed  # Position still active
    assert len(strategy.active_positions[position_id]['partial_exits']) == 1
    assert len(strategy.active_positions[position_id]['take_profits']) == 1
    assert strategy.active_positions[position_id]['size'] == 0.05  # Half size remaining
    
    # Test full exit
    exit_info = {
        'reason': 'stop_loss',
        'price': 49000.0,
        'percentage': 100
    }
    
    is_closed = await strategy.process_partial_exit(position_id, exit_info)
    assert is_closed  # Position fully closed
    assert position_id not in strategy.active_positions  # Position removed from tracking 