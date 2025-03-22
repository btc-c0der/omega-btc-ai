#!/usr/bin/env python3

"""
Enhanced Exit Strategy for OMEGA BTC AI
=====================================

This module implements an advanced exit strategy that combines:
- Fibonacci-based take profit levels
- Dynamic trailing stops
- Scalping opportunities
- Strategic position scaling
- Market maker trap awareness
"""

import logging
import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import redis
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class EnhancedExitStrategy:
    """Enhanced exit strategy combining multiple approaches."""
    
    def __init__(
        self,
        base_risk_percent: float = 1.0,
        fib_levels: List[float] = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618],
        enable_scalping: bool = True,
        scalping_coefficient: float = 0.3,
        strategic_coefficient: float = 0.6,
        aggressive_coefficient: float = 0.1,
        enable_trailing_stop: bool = True,
        trailing_activation_threshold: float = 1.0,  # 1% profit to activate trailing
        trailing_distance_factor: float = 0.3,  # Trail at 30% of profit
        min_tp_distance: float = 0.5,  # Minimum 0.5% for take profit
        max_tp_levels: int = 4,
        redis_host: str = "localhost",
        redis_port: int = 6379
    ):
        """Initialize the enhanced exit strategy."""
        self.base_risk_percent = base_risk_percent
        self.fib_levels = fib_levels
        self.enable_scalping = enable_scalping
        self.scalping_coefficient = scalping_coefficient
        self.strategic_coefficient = strategic_coefficient
        self.aggressive_coefficient = aggressive_coefficient
        self.enable_trailing_stop = enable_trailing_stop
        self.trailing_activation_threshold = trailing_activation_threshold
        self.trailing_distance_factor = trailing_distance_factor
        self.min_tp_distance = min_tp_distance
        self.max_tp_levels = max_tp_levels
        
        # Initialize Redis connection
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        
        # Active positions tracking
        self.active_positions = {}
        self.trailing_stops = {}
        
    def set_position_exit_strategy(
        self,
        position_id: str,
        entry_price: float,
        direction: str,
        size: float,
        leverage: float,
        market_data: Optional[Dict] = None
    ) -> Dict:
        """Set comprehensive exit strategy for a position."""
        # Calculate base stop distance using ATR if available
        atr = market_data.get('atr', entry_price * 0.01)  # Default to 1% if no ATR
        base_stop_distance = max(
            entry_price * (self.base_risk_percent / 100),
            atr * 1.5  # Use at least 1.5x ATR
        )
        
        # Calculate stop loss price
        if direction.lower() == 'long':
            stop_loss = entry_price - base_stop_distance
        else:  # short
            stop_loss = entry_price + base_stop_distance
        
        # Calculate take profit levels using Fibonacci extensions
        take_profits = self._calculate_fib_take_profits(
            entry_price,
            stop_loss,
            direction,
            leverage
        )
        
        # Apply scalping influence if enabled
        if self.enable_scalping and self.scalping_coefficient > 0:
            take_profits = self._apply_scalping_influence(
                take_profits,
                direction,
                entry_price
            )
        
        # Store strategy for this position
        self.active_positions[position_id] = {
            'entry_price': entry_price,
            'direction': direction,
            'size': size,
            'leverage': leverage,
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'initial_stop': stop_loss,
            'trailing_activated': False,
            'partial_exits': []
        }
        
        return {
            'stop_loss': stop_loss,
            'take_profits': take_profits
        }
    
    def _calculate_fib_take_profits(
        self,
        entry_price: float,
        stop_loss: float,
        direction: str,
        leverage: float
    ) -> List[Dict]:
        """Calculate take profit levels based on Fibonacci extensions."""
        risk_distance = abs(entry_price - stop_loss)
        base_reward = risk_distance * 2.5  # Minimum 2.5:1 reward:risk
        
        # Fibonacci extensions for TP levels
        extensions = [0.618, 1.0, 1.618, 2.618][:self.max_tp_levels]
        
        # Calculate size allocation for each level
        total_parts = sum(range(1, len(extensions) + 1))
        size_allocations = []
        for i in range(len(extensions)):
            allocation = (len(extensions) - i) / total_parts
            size_allocations.append(allocation)
        
        take_profits = []
        for i, (ext, size_alloc) in enumerate(zip(extensions, size_allocations)):
            tp_distance = base_reward * ext
            
            if direction.lower() == 'long':
                tp_price = entry_price + tp_distance
            else:
                tp_price = entry_price - tp_distance
            
            # Ensure minimum distance
            min_distance = entry_price * (self.min_tp_distance / 100)
            if direction.lower() == 'long':
                tp_price = max(tp_price, entry_price + min_distance)
            else:
                tp_price = min(tp_price, entry_price - min_distance)
            
            take_profits.append({
                "price": tp_price,
                "percentage": round(size_alloc * 100),  # Convert to percentage
                "fib_level": ext
            })
        
        return take_profits
    
    def _apply_scalping_influence(
        self,
        take_profits: List[Dict],
        direction: str,
        entry_price: float
    ) -> List[Dict]:
        """Apply scalping influence to take profit strategy."""
        if not take_profits:
            return take_profits
        
        # Increase size of first TP
        original_size = take_profits[0]["percentage"]
        adjusted_size = original_size + (original_size * self.scalping_coefficient)
        
        # Adjust other TP sizes proportionally
        remaining_tps = take_profits[1:]
        if remaining_tps:
            total_remaining = sum(tp["percentage"] for tp in remaining_tps)
            for tp in remaining_tps:
                reduction_factor = (tp["percentage"] / total_remaining) * (adjusted_size - original_size)
                tp["percentage"] = max(5, tp["percentage"] - reduction_factor)
        
        # Update first TP
        take_profits[0]["percentage"] = min(90, adjusted_size)
        
        # Move first TP closer
        first_tp = take_profits[0]["price"]
        movement_factor = 0.3 * self.scalping_coefficient
        if direction.lower() == 'long':
            take_profits[0]["price"] = first_tp - ((first_tp - entry_price) * movement_factor)
        else:
            take_profits[0]["price"] = first_tp + ((entry_price - first_tp) * movement_factor)
        
        return take_profits
    
    async def update_trailing_stop(
        self,
        position_id: str,
        current_price: float
    ) -> Optional[float]:
        """Update trailing stop based on price movement."""
        if not self.enable_trailing_stop:
            return None
        
        position = self.active_positions.get(position_id)
        if not position:
            return None
        
        entry_price = position['entry_price']
        direction = position['direction']
        initial_stop = position['initial_stop']
        current_stop = position['stop_loss']
        
        # Check if we should activate trailing
        if not position['trailing_activated']:
            # Calculate profit percentage
            if direction.lower() == 'long':
                profit_pct = (current_price - entry_price) / entry_price * 100
            else:
                profit_pct = (entry_price - current_price) / entry_price * 100
            
            # Activate if profit exceeds threshold
            if profit_pct >= self.trailing_activation_threshold:
                position['trailing_activated'] = True
                self.trailing_stops[position_id] = {
                    'activation_price': current_price,
                    'current_stop': current_stop
                }
        
        # Update trailing stop if activated
        if position['trailing_activated']:
            if direction.lower() == 'long':
                profit = current_price - entry_price
                if profit <= 0:
                    return current_stop
                
                # Trail at percentage of profit
                trail_distance = profit * self.trailing_distance_factor
                new_stop = current_price - trail_distance
                
                # Only move stop up
                if new_stop > current_stop:
                    position['stop_loss'] = new_stop
                    self.trailing_stops[position_id]['current_stop'] = new_stop
                    return new_stop
            else:  # short
                profit = entry_price - current_price
                if profit <= 0:
                    return current_stop
                
                trail_distance = profit * self.trailing_distance_factor
                new_stop = current_price + trail_distance
                
                # Only move stop down
                if new_stop < current_stop:
                    position['stop_loss'] = new_stop
                    self.trailing_stops[position_id]['current_stop'] = new_stop
                    return new_stop
        
        return current_stop
    
    async def check_exit_conditions(
        self,
        position_id: str,
        current_price: float,
        market_data: Optional[Dict] = None
    ) -> Tuple[bool, Optional[Dict]]:
        """Check if any exit conditions are met."""
        position = self.active_positions.get(position_id)
        if not position:
            return False, None
        
        direction = position['direction']
        stop_loss = position['stop_loss']
        take_profits = position['take_profits']
        
        # Check for stop loss hit
        if direction.lower() == 'long' and current_price <= stop_loss:
            return True, {
                'reason': 'stop_loss',
                'price': stop_loss,
                'percentage': 100
            }
        elif direction.lower() == 'short' and current_price >= stop_loss:
            return True, {
                'reason': 'stop_loss',
                'price': stop_loss,
                'percentage': 100
            }
        
        # Check for take profit hits
        for tp in take_profits:
            tp_price = tp['price']
            tp_percentage = tp['percentage']
            
            if direction.lower() == 'long' and current_price >= tp_price:
                return True, {
                    'reason': 'take_profit',
                    'price': tp_price,
                    'percentage': tp_percentage,
                    'fib_level': tp.get('fib_level')
                }
            elif direction.lower() == 'short' and current_price <= tp_price:
                return True, {
                    'reason': 'take_profit',
                    'price': tp_price,
                    'percentage': tp_percentage,
                    'fib_level': tp.get('fib_level')
                }
        
        # Check for market maker trap exit
        trap_data = await self._get_trap_data()
        if trap_data and trap_data.get('probability', 0) > 0.7:
            trap_type = trap_data.get('trap_type', '').lower()
            
            if (direction.lower() == 'long' and trap_type in ['bull_trap', 'fake_pump']) or \
               (direction.lower() == 'short' and trap_type in ['bear_trap', 'fake_dump']):
                # Exit percentage based on trap probability
                exit_percentage = min(50, int(trap_data.get('probability', 0) * 50))
                
                return True, {
                    'reason': 'trap_detected',
                    'price': current_price,
                    'percentage': exit_percentage,
                    'trap_type': trap_type
                }
        
        return False, None
    
    async def _get_trap_data(self) -> Optional[Dict]:
        """Get current market maker trap data from Redis."""
        try:
            trap_data = self.redis.get('current_trap_probability')
            if trap_data:
                import json
                return json.loads(trap_data)
        except Exception as e:
            logger.error(f"Error getting trap data: {e}")
        return None
    
    async def process_partial_exit(
        self,
        position_id: str,
        exit_info: Dict
    ) -> bool:
        """Process a partial exit and update position tracking."""
        position = self.active_positions.get(position_id)
        if not position:
            return False
        
        exit_percentage = exit_info.get('percentage', 0)
        exit_price = exit_info.get('price', 0)
        reason = exit_info.get('reason', 'unknown')
        
        # Record the exit
        position['partial_exits'].append({
            'timestamp': datetime.now().isoformat(),
            'percentage': exit_percentage,
            'price': exit_price,
            'reason': reason,
            'fib_level': exit_info.get('fib_level'),
            'trap_type': exit_info.get('trap_type')
        })
        
        # Remove hit take profit level
        if reason == 'take_profit':
            position['take_profits'] = [tp for tp in position['take_profits']
                                      if abs(tp['price'] - exit_price) > 0.01]
        
        # Handle full exit
        if reason == 'stop_loss' or exit_percentage >= 100:
            del self.active_positions[position_id]
            if position_id in self.trailing_stops:
                del self.trailing_stops[position_id]
            return True
        
        # Adjust remaining size
        position['size'] = position['size'] * (1 - exit_percentage/100)
        
        # Close if very small position left
        if position['size'] < 0.001:  # Threshold depends on asset
            return True
        
        return False  # Position still active 