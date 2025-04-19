
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

import asyncio
import logging
from datetime import datetime, timedelta
import numpy as np
import redis
import json
from typing import Dict, List, Tuple, Optional, Any

class EnhancedFibonacciExitManager:
    """Advanced exit manager for Fibonacci-based strategic trader."""
    
    def __init__(self, 
                 redis_client=None,
                 base_risk_percent=1.0,
                 tp_layers=4,
                 sl_multiplier=1.0,
                 enable_trailing=True,
                 trailing_activation_pct=1.0,
                 fib_levels=[0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618],
                 risk_reward_ratio=2.5,
                 scalper_coefficient=0.3,
                 aggressive_coefficient=0.1,
                 trap_sensitivity=0.7):
        """Initialize the enhanced Fibonacci exit manager."""
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.base_risk_percent = base_risk_percent
        self.tp_layers = tp_layers
        self.sl_multiplier = sl_multiplier
        self.enable_trailing = enable_trailing
        self.trailing_activation_pct = trailing_activation_pct
        self.fib_levels = fib_levels
        self.risk_reward_ratio = risk_reward_ratio
        self.scalper_coefficient = scalper_coefficient
        self.aggressive_coefficient = aggressive_coefficient
        self.trap_sensitivity = trap_sensitivity
        
        # Active position tracking
        self.active_positions = {}
        self.trailing_stops = {}
        self.partial_exits = {}
        
        # Logger setup
        self.logger = logging.getLogger('fibonacci_exit_manager')
    
    async def calculate_exit_strategy(self, 
                                      position_id: str, 
                                      entry_price: float, 
                                      direction: str, 
                                      size: float, 
                                      leverage: float) -> Dict[str, Any]:
        """Calculate comprehensive exit strategy for a position."""
        # Get current market volatility using ATR
        atr = await self._get_adaptive_atr()
        
        # Calculate base stop distance as percentage of entry price
        # Adjusted by the ATR for more dynamic positioning
        base_stop_distance = entry_price * (self.base_risk_percent / 100) * self.sl_multiplier
        adjusted_stop_distance = max(base_stop_distance, atr * 1.5)  # Use at least 1.5x ATR
        
        # Set stop loss based on direction
        if direction.lower() == 'long':
            stop_loss = entry_price - adjusted_stop_distance
        else:  # short
            stop_loss = entry_price + adjusted_stop_distance
            
        # Calculate take profit layers using Fibonacci extensions
        take_profits = self._calculate_fib_take_profits(
            entry_price, stop_loss, direction, self.tp_layers
        )
        
        # Apply scalper influence for first TP layer (closer and larger size)
        if self.scalper_coefficient > 0:
            take_profits = self._apply_scalper_influence(take_profits, entry_price, direction)
            
        # Apply aggressive influence for last TP layer (further and higher reward)
        if self.aggressive_coefficient > 0:
            take_profits = self._apply_aggressive_influence(take_profits, entry_price, direction)
            
        # Store strategy for this position
        self.active_positions[position_id] = {
            'entry_price': entry_price,
            'direction': direction,
            'size': size,
            'leverage': leverage,
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'initial_stop': stop_loss,  # Track initial stop for trailing
            'trailing_activated': False,
            'partial_exits': [],
            'created_at': datetime.now().isoformat()
        }
        
        # Log the strategy
        self.logger.info(f"Exit strategy calculated for {position_id}: SL={stop_loss}, TPs={take_profits}")
        
        # Return the calculated exit points
        return {
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'position_id': position_id
        }
    
    def _calculate_fib_take_profits(self, entry_price: float, 
                                  stop_loss: float, 
                                  direction: str, 
                                  layers: int = 4) -> List[Dict[str, Any]]:
        """Calculate take profit levels based on Fibonacci extensions."""
        risk_distance = abs(entry_price - stop_loss)
        
        # Base reward distance (from entry to first TP)
        base_reward = risk_distance * self.risk_reward_ratio
        
        # Create multiple take profit levels using Fibonacci extensions
        take_profits = []
        
        # Fibonacci extensions to use for TP levels
        # For long positions: use values like 0.618, 1.0, 1.618, 2.618
        # For shorts, the approach is similar but reversed
        extensions = [0.618, 1.0, 1.618, 2.618, 4.236][:layers]
        
        # Calculate size allocation for each level
        # More weight to early TPs for scalper influence, more to later for strategic
        total_parts = sum(range(1, layers + 1))  # 1+2+3+...+layers
        size_allocations = []
        for i in range(layers):
            allocation = (layers - i) / total_parts
            size_allocations.append(allocation)
            
        for i, (ext, size_alloc) in enumerate(zip(extensions, size_allocations)):
            tp_distance = base_reward * ext
            
            if direction.lower() == 'long':
                tp_price = entry_price + tp_distance
            else:  # short
                tp_price = entry_price - tp_distance
                
            take_profits.append({
                "price": tp_price,
                "percentage": round(size_alloc * 100)  # Convert to percentage
            })
            
        return take_profits
    
    def _apply_scalper_influence(self, take_profits: List[Dict[str, Any]], 
                               entry_price: float, 
                               direction: str) -> List[Dict[str, Any]]:
        """Apply scalper profile influence to take profit strategy."""
        if not take_profits:
            return take_profits
            
        # Increase size of first TP (scalpers take profits quickly)
        original_size = take_profits[0]["percentage"]
        adjusted_size = original_size + (original_size * self.scalper_coefficient)
        
        # Adjust other TP sizes proportionally
        total_adjustment = adjusted_size - original_size
        remaining_tps = take_profits[1:]
        
        if remaining_tps:
            # Distribute the adjustment proportionally among remaining TPs
            total_remaining = sum(tp["percentage"] for tp in remaining_tps)
            for tp in remaining_tps:
                reduction_factor = (tp["percentage"] / total_remaining) * total_adjustment
                tp["percentage"] = max(5, tp["percentage"] - reduction_factor)  # Min 5%
                
        # Update first TP
        take_profits[0]["percentage"] = min(90, adjusted_size)  # Max 90%
        
        # Also move first TP slightly closer (scalper influence)
        first_tp = take_profits[0]["price"]
        
        if entry_price > 0:
            # Move 10-30% closer depending on scalper coefficient
            movement_factor = 0.3 * self.scalper_coefficient
            if direction.lower() == 'long':
                take_profits[0]["price"] = first_tp - ((first_tp - entry_price) * movement_factor)
            else:
                take_profits[0]["price"] = first_tp + ((entry_price - first_tp) * movement_factor)
        
        return take_profits
    
    def _apply_aggressive_influence(self, take_profits: List[Dict[str, Any]], 
                                  entry_price: float, 
                                  direction: str) -> List[Dict[str, Any]]:
        """Apply aggressive trader influence to take profit strategy."""
        if len(take_profits) < 2:
            return take_profits
            
        # Increase distance of last TP (aggressive traders aim for bigger wins)
        last_tp = take_profits[-1]
        
        if entry_price > 0:
            # Extend final TP by 10-50% depending on aggressive coefficient
            extension_factor = 0.5 * self.aggressive_coefficient
            
            if direction.lower() == 'long':
                tp_distance = last_tp["price"] - entry_price
                last_tp["price"] = last_tp["price"] + (tp_distance * extension_factor)
            else:
                tp_distance = entry_price - last_tp["price"]
                last_tp["price"] = last_tp["price"] - (tp_distance * extension_factor)
        
        return take_profits
    
    async def update_trailing_stop(self, position_id: str, current_price: float) -> Optional[float]:
        """Update trailing stop based on price movement and Fibonacci levels."""
        if not self.enable_trailing:
            return None
            
        position = self.active_positions.get(position_id)
        if not position:
            return None
            
        entry_price = position['entry_price']
        direction = position['direction'].lower()
        initial_stop = position['initial_stop']
        current_stop = position['stop_loss']
        
        # Determine if we should activate trailing
        if not position['trailing_activated']:
            # Calculate profit percentage
            if direction == 'long':
                profit_pct = (current_price - entry_price) / entry_price * 100
            else:
                profit_pct = (entry_price - current_price) / entry_price * 100
                
            # Check if profit exceeds activation threshold
            if profit_pct >= self.trailing_activation_pct:
                position['trailing_activated'] = True
                self.trailing_stops[position_id] = {
                    'activation_price': current_price,
                    'current_stop': current_stop
                }
                
                self.logger.info(f"Trailing stop activated for {position_id} at {current_price}")
                
        # If trailing is activated, update stop loss
        if position['trailing_activated']:
            atr = await self._get_adaptive_atr()
            
            if direction == 'long':
                # For long positions
                profit = current_price - entry_price
                if profit <= 0:
                    return current_stop  # No profit, no trailing
                    
                # Base trailing distance on ATR and profit percentage
                trail_distance = max(atr * 2, profit * 0.3)
                
                # Use Fibonacci retracement levels for trailing
                # As price moves up, trail at key Fibonacci retracement levels
                # This provides more intelligent trailing aligned with market structure
                fib_stop = self._calculate_fib_trailing_stop(entry_price, current_price, 'long')
                new_stop = max(fib_stop, current_price - trail_distance)
                
                # Only move stop up, never down
                if new_stop > current_stop:
                    position['stop_loss'] = new_stop
                    self.trailing_stops[position_id]['current_stop'] = new_stop
                    
                    # Store update in Redis for UI
                    self._update_position_in_redis(position_id, position)
                    
                    self.logger.info(f"Updated trailing stop for {position_id} to {new_stop}")
                    return new_stop
            else:
                # For short positions
                profit = entry_price - current_price
                if profit <= 0:
                    return current_stop
                    
                trail_distance = max(atr * 2, profit * 0.3)
                
                # Use Fibonacci retracement levels for trailing
                fib_stop = self._calculate_fib_trailing_stop(entry_price, current_price, 'short')
                new_stop = min(fib_stop, current_price + trail_distance)
                
                # Only move stop down, never up
                if new_stop < current_stop:
                    position['stop_loss'] = new_stop
                    self.trailing_stops[position_id]['current_stop'] = new_stop
                    
                    # Store update in Redis for UI
                    self._update_position_in_redis(position_id, position)
                    
                    self.logger.info(f"Updated trailing stop for {position_id} to {new_stop}")
                    return new_stop
                    
        return current_stop
    
    def _calculate_fib_trailing_stop(self, entry_price: float, 
                                   current_price: float, 
                                   direction: str) -> float:
        """Calculate trailing stop based on Fibonacci retracement levels."""
        if direction == 'long':
            # For long positions, calculate retracement levels from entry to current
            price_range = current_price - entry_price
            
            # Use 0.382 Fibonacci level for initial trailing
            # As price moves higher, this creates a trailing stop at 38.2% retracement
            fib_stop = current_price - (price_range * 0.382)
            
            # Make sure stop is never below entry once in profit
            return max(fib_stop, entry_price)
        else:
            # For short positions, calculate retracement levels from entry to current
            price_range = entry_price - current_price
            
            # Use 0.382 Fibonacci level for initial trailing
            fib_stop = current_price + (price_range * 0.382)
            
            # Make sure stop is never above entry once in profit
            return min(fib_stop, entry_price)
    
    async def _get_adaptive_atr(self, timeframe='1h', lookback=14) -> float:
        """Calculate Adaptive ATR for dynamic stop loss placement."""
        try:
            # Try to get ATR from Redis first
            atr_key = f"atr:{timeframe}:{lookback}"
            atr_value = self.redis_client.get(atr_key)
            
            if atr_value:
                return float(atr_value)
            
            # Fallback value based on typical BTC volatility
            # In a full implementation, this would calculate ATR from price data
            return 50.0
        except Exception as e:
            self.logger.error(f"Error calculating ATR: {e}")
            return 50.0  # Fallback default
    
    async def check_for_exits(self, position_id: str, 
                            current_price: float, 
                            trap_data: Optional[Dict] = None) -> Tuple[bool, Optional[Dict]]:
        """Check if any exit conditions are met for the position."""
        position = self.active_positions.get(position_id)
        if not position:
            return False, None
            
        direction = position['direction'].lower()
        stop_loss = position['stop_loss']
        take_profits = position['take_profits']
        
        # Check for stop loss hit
        if direction == 'long' and current_price <= stop_loss:
            return True, {
                'reason': 'stop_loss',
                'price': stop_loss,
                'percentage': 100
            }
        elif direction == 'short' and current_price >= stop_loss:
            return True, {
                'reason': 'stop_loss',
                'price': stop_loss,
                'percentage': 100
            }
            
        # Check for take profit hits
        for tp in take_profits:
            tp_price = tp['price']
            tp_percentage = tp['percentage']
            
            if direction == 'long' and current_price >= tp_price:
                return True, {
                    'reason': 'take_profit',
                    'price': tp_price,
                    'percentage': tp_percentage
                }
            elif direction == 'short' and current_price <= tp_price:
                return True, {
                    'reason': 'take_profit',
                    'price': tp_price,
                    'percentage': tp_percentage
                }
                
        # Check for market maker trap exit
        if trap_data and trap_data.get('probability', 0) > self.trap_sensitivity:
            trap_type = trap_data.get('trap_type', '').lower()
            
            if (direction == 'long' and trap_type in ['bull_trap', 'fake_pump']) or \
               (direction == 'short' and trap_type in ['bear_trap', 'fake_dump']):
                # Exit trap-based percentage of position
                exit_percentage = min(50, int(trap_data.get('probability', 0) * 50))
                
                return True, {
                    'reason': 'trap_detected',
                    'price': current_price,
                    'percentage': exit_percentage,
                    'trap_type': trap_type
                }
                
        # No exit conditions met
        return False, None
    
    async def process_partial_exit(self, position_id: str, exit_info: Dict) -> bool:
        """Process a partial exit and update position tracking."""
        position = self.active_positions.get(position_id)
        if not position:
            return False
            
        exit_percentage = exit_info.get('percentage', 0)
        exit_price = exit_info.get('price', 0)
        reason = exit_info.get('reason', 'unknown')
        
        # Record this exit
        exit_record = {
            'timestamp': datetime.now().isoformat(),
            'percentage': exit_percentage,
            'price': exit_price,
            'reason': reason
        }
        
        position['partial_exits'].append(exit_record)
        
        # Update the partial exits in Redis for tracking
        self.partial_exits.setdefault(position_id, []).append(exit_record)
        self._update_exits_in_redis(position_id)
        
        # If take profit hit, remove that level
        if reason == 'take_profit':
            position['take_profits'] = [tp for tp in position['take_profits'] 
                                      if abs(tp['price'] - exit_price) > 0.01]
                                      
        # If stop loss hit or 100% exit, remove position tracking
        if reason == 'stop_loss' or exit_percentage >= 100:
            del self.active_positions[position_id]
            if position_id in self.trailing_stops:
                del self.trailing_stops[position_id]
                
            # Don't delete from partial_exits to keep history
            return True
            
        # Adjust remaining size
        position['size'] = position['size'] * (1 - exit_percentage/100)
        
        # If very small position left, close it completely
        if position['size'] < 0.001:  # Threshold depends on asset
            return True
            
        # Update position in Redis
        self._update_position_in_redis(position_id, position)
            
        return False  # Position still active
    
    def _update_position_in_redis(self, position_id: str, position_data: Dict) -> None:
        """Update position data in Redis for UI and monitoring."""
        try:
            position_key = f"position:{position_id}"
            self.redis_client.set(position_key, json.dumps(position_data))
        except Exception as e:
            self.logger.error(f"Error updating position in Redis: {e}")
    
    def _update_exits_in_redis(self, position_id: str) -> None:
        """Update partial exits in Redis for UI and monitoring."""
        try:
            exits_key = f"exits:{position_id}"
            exits_data = self.partial_exits.get(position_id, [])
            self.redis_client.set(exits_key, json.dumps(exits_data))
        except Exception as e:
            self.logger.error(f"Error updating exits in Redis: {e}")