#!/usr/bin/env python3

"""
Enhanced Exit Strategy for trading positions with advanced exit management.

This module implements sophisticated exit strategies for trading positions,
including trailing stops, fibonacci-based take profits, and trap awareness.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple, Union
import redis
import json
import asyncio
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class EnhancedExitStrategy:
    """
    Enhanced exit strategy implementation with multiple exit mechanisms.
    
    This class provides advanced exit strategy functionality including:
    - Multiple take profit levels
    - Trailing stops
    - Dynamic exit based on market conditions
    - Trap awareness
    - Partial exits
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the enhanced exit strategy.
        
        Args:
            config: Configuration dictionary containing parameters for the strategy
        """
        # Risk management parameters
        self.base_risk_percent = config.get('base_risk_percent', 1.0)
        
        # Scalping parameters
        self.enable_scalping = config.get('enable_scalping', True)
        self.scalping_coefficient = config.get('scalping_coefficient', 0.3)
        
        # Strategic parameters
        self.strategic_coefficient = config.get('strategic_coefficient', 0.6)
        self.aggressive_coefficient = config.get('aggressive_coefficient', 0.1)
        
        # Position tracking
        self.positions = {}
        self.take_profits = {}
        self.stop_losses = {}
        self.trailing_stops = {}
        self.position_states = {}
        
        # Redis for market data
        try:
            self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
            logger.info("Connected to Redis for market data")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}")
            self.redis = None
            
        logger.info("Enhanced exit strategy initialized")
        
    def should_exit(self, position_data: Dict[str, Any]) -> bool:
        """
        Determine if a position should be exited based on current conditions.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Boolean indicating whether to exit the position
        """
        position_id = position_data.get('id')
        current_price = position_data.get('current_price')
        
        if not position_id or not current_price:
            return False
            
        return False
        
    def calculate_exit_price(self, position_data: Dict[str, Any]) -> Optional[float]:
        """
        Calculate the optimal exit price for a position.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Optional float representing the exit price, or None if not applicable
        """
        return None
        
    def update_state(self, market_data: Dict[str, Any]) -> None:
        """
        Update internal state based on new market data.
        
        Args:
            market_data: Dictionary containing market information
        """
        pass
        
    async def update_trailing_stop(
        self, 
        position_id: str,
        current_price: float
    ) -> Optional[float]:
        """
        Update the trailing stop for a position based on current price.
        
        Args:
            position_id: Identifier for the position
            current_price: Current market price
            
        Returns:
            Optional float representing the new stop loss price, or None if unchanged
        """
        if position_id not in self.positions:
            logger.warning(f"Position {position_id} not found for trailing stop update")
            return None
            
        position = self.positions[position_id]
        direction = position.get('direction', '').lower()
        entry_price = position.get('entry_price', 0)
        
        current_stop = self.stop_losses.get(position_id)
        if not current_stop:
            logger.warning(f"No stop loss found for position {position_id}")
            return None
            
        # Implement trailing stop logic based on direction
        if direction == 'long' and current_price > entry_price:
            # For long positions, move stop up as price increases
            profit_distance = current_price - entry_price
            new_stop = entry_price + (profit_distance * 0.5)  # Trail at 50% of profit
            
            if new_stop > current_stop:
                logger.info(f"Updating trailing stop for position {position_id} from {current_stop} to {new_stop}")
                self.stop_losses[position_id] = new_stop
                return new_stop
                
        elif direction == 'short' and current_price < entry_price:
            # For short positions, move stop down as price decreases
            profit_distance = entry_price - current_price
            new_stop = entry_price - (profit_distance * 0.5)  # Trail at 50% of profit
            
            if new_stop < current_stop:
                logger.info(f"Updating trailing stop for position {position_id} from {current_stop} to {new_stop}")
                self.stop_losses[position_id] = new_stop
                return new_stop
                
        return None
        
    async def check_exit_conditions(
        self,
        position_id: str,
        current_price: float,
        market_data: Optional[Dict] = None
    ) -> Tuple[bool, Optional[Dict]]:
        """
        Check if any exit conditions are met for a position.
        
        Args:
            position_id: Identifier for the position
            current_price: Current market price
            market_data: Optional dictionary containing additional market information
            
        Returns:
            Tuple of (should_exit, exit_info)
        """
        if position_id not in self.positions:
            logger.warning(f"Position {position_id} not found for exit check")
            return False, None
            
        position = self.positions[position_id]
        direction = position.get('direction', '').lower()
        entry_price = position.get('entry_price', 0)
        
        # Get stop loss and take profits
        stop_loss = self.stop_losses.get(position_id)
        take_profits = self.take_profits.get(position_id, [])
        
        # Check stop loss
        if stop_loss:
            if (direction == 'long' and current_price <= stop_loss) or \
               (direction == 'short' and current_price >= stop_loss):
                return True, {
                    'reason': 'stop_loss',
                    'price': stop_loss,
                    'percentage': 100  # Exit full position
                }
                
        # Check take profits
        for tp in take_profits:
            tp_price = tp.get('price', 0)
            tp_percentage = tp.get('percentage', 0)
            
            if (direction == 'long' and current_price >= tp_price) or \
               (direction == 'short' and current_price <= tp_price):
                return True, {
                    'reason': 'take_profit',
                    'price': tp_price,
                    'percentage': tp_percentage
                }
                
        # Check for trap-based exits
        trap_data = await self._get_trap_data()
        if trap_data and trap_data.get('probability', 0) > 0.8:
            trap_type = trap_data.get('type', '')
            
            # Exit if trap type opposes position direction
            if (direction == 'long' and trap_type in ['bull_trap', 'fake_pump']) or \
               (direction == 'short' and trap_type in ['bear_trap', 'fake_dump']):
                return True, {
                    'reason': 'trap_detected',
                    'trap_type': trap_type,
                    'probability': trap_data.get('probability', 0),
                    'percentage': 100  # Exit full position
                }
                
        return False, None
        
    async def process_partial_exit(
        self,
        position_id: str,
        exit_info: Dict[str, Any]
    ) -> None:
        """
        Process a partial exit for a position.
        
        Args:
            position_id: Identifier for the position
            exit_info: Dictionary containing exit information
        """
        if position_id not in self.positions:
            logger.warning(f"Position {position_id} not found for partial exit")
            return
            
        position = self.positions[position_id]
        exit_percentage = exit_info.get('percentage', 0)
        
        if exit_percentage >= 100:
            # Full exit
            logger.info(f"Processing full exit for position {position_id}")
            self.remove_position(position_id)
        else:
            # Partial exit
            logger.info(f"Processing partial exit ({exit_percentage}%) for position {position_id}")
            
            # Update position size
            original_size = position.get('size', 0)
            exit_size = original_size * (exit_percentage / 100)
            remaining_size = original_size - exit_size
            
            position['size'] = remaining_size
            self.positions[position_id] = position
            
            # Update take profits (remove the triggered one)
            take_profits = self.take_profits.get(position_id, [])
            if exit_info.get('reason') == 'take_profit':
                take_profits = [tp for tp in take_profits if tp.get('price') != exit_info.get('price')]
                self.take_profits[position_id] = take_profits
                
    def add_position(
        self,
        position_id: str,
        entry_price: float,
        size: float,
        stop_loss: Optional[float] = None,
        take_profits: Optional[List[Dict]] = None
    ) -> None:
        """
        Add a new position to be managed by the exit strategy.
        
        Args:
            position_id: Identifier for the position
            entry_price: Entry price for the position
            size: Position size
            stop_loss: Optional stop loss price
            take_profits: Optional list of take profit levels
        """
        self.positions[position_id] = {
            'id': position_id,
            'entry_price': entry_price,
            'size': size,
            'timestamp': datetime.now(timezone.utc).timestamp()
        }
        
        if stop_loss:
            self.stop_losses[position_id] = stop_loss
            
        if take_profits:
            self.take_profits[position_id] = take_profits
            
        logger.info(f"Added position {position_id} with entry price {entry_price} and size {size}")
        
    def remove_position(self, position_id: str) -> None:
        """
        Remove a position from management.
        
        Args:
            position_id: Identifier for the position
        """
        self.positions.pop(position_id, None)
        self.stop_losses.pop(position_id, None)
        self.take_profits.pop(position_id, None)
        self.trailing_stops.pop(position_id, None)
        self.position_states.pop(position_id, None)
        
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
        atr = market_data.get('atr', entry_price * 0.01) if market_data else entry_price * 0.01  # Default to 1% if no ATR
        base_stop_distance = max(
            entry_price * (self.base_risk_percent / 100),
            atr * 1.5  # Use at least 1.5x ATR
        )
        
        # Set stop loss based on direction
        if direction.lower() == 'long':
            stop_loss = entry_price - base_stop_distance
        else:
            stop_loss = entry_price + base_stop_distance
            
        # Calculate take profits using Fibonacci levels
        take_profits = self._calculate_fib_take_profits(
            entry_price,
            stop_loss,
            direction,
            leverage
        )
        
        # Apply scalping influence if enabled
        if self.enable_scalping:
            take_profits = self._apply_scalping_influence(
                take_profits,
                direction,
                entry_price
            )
            
        # Store the strategy
        self.positions[position_id] = {
            'id': position_id,
            'entry_price': entry_price,
            'direction': direction,
            'size': size,
            'leverage': leverage,
            'timestamp': datetime.now(timezone.utc).timestamp()
        }
        
        self.stop_losses[position_id] = stop_loss
        self.take_profits[position_id] = take_profits
        
        # Return the strategy for reference
        return {
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'initial_risk': self.base_risk_percent
        }
            
    def _calculate_fib_take_profits(
        self,
        entry_price: float,
        stop_loss: float,
        direction: str,
        leverage: float
    ) -> List[Dict]:
        """
        Calculate take profit levels based on Fibonacci extensions.
        
        Args:
            entry_price: Entry price for the position
            stop_loss: Stop loss price
            direction: Trade direction ('long' or 'short')
            leverage: Position leverage
            
        Returns:
            List of dictionaries containing take profit information
        """
        # Calculate risk distance
        risk_distance = abs(entry_price - stop_loss)
        
        # Fibonacci extension levels
        fib_levels = [1.0, 1.618, 2.618, 3.618, 4.236]
        
        # Adjust levels based on leverage
        if leverage > 10:
            # For high leverage, use more conservative targets
            fib_levels = [0.5, 0.786, 1.0, 1.618, 2.0]
        elif leverage > 5:
            # For medium leverage
            fib_levels = [0.786, 1.0, 1.618, 2.618, 3.0]
            
        # Calculate take profit prices and percentages
        take_profits = []
        cumulative_percentage = 0
        
        for i, level in enumerate(fib_levels):
            # Determine percentage of position to exit at this level
            if i == len(fib_levels) - 1:
                # Last level takes remaining position
                percentage = 100 - cumulative_percentage
            else:
                # Distribute percentages, more weight to earlier levels
                percentage = max(5, 100 / len(fib_levels) - (i * 3))
                cumulative_percentage += percentage
                
            # Calculate take profit price based on direction
            if direction.lower() == 'long':
                tp_price = entry_price + (risk_distance * level)
            else:
                tp_price = entry_price - (risk_distance * level)
                
            take_profits.append({
                'price': tp_price,
                'percentage': percentage,
                'fib_level': level
            })
            
        return take_profits
        
    def _apply_scalping_influence(
        self,
        take_profits: List[Dict],
        direction: str,
        entry_price: float
    ) -> List[Dict]:
        """
        Apply scalping influence to take profit levels.
        
        Args:
            take_profits: List of take profit dictionaries
            direction: Trade direction ('long' or 'short')
            entry_price: Entry price for the position
            
        Returns:
            Modified list of take profit dictionaries
        """
        if not take_profits or self.scalping_coefficient <= 0:
            return take_profits
            
        # Apply scalping influence (bring early take profits closer)
        for i, tp in enumerate(take_profits):
            if i < 2:  # Only adjust the first two take profits
                original_distance = abs(tp['price'] - entry_price)
                adjusted_distance = original_distance * (1 - (self.scalping_coefficient * (2-i) / 2))
                
                if direction.lower() == 'long':
                    tp['price'] = entry_price + adjusted_distance
                else:
                    tp['price'] = entry_price - adjusted_distance
                    
        return take_profits
        
    async def _get_trap_data(self) -> Optional[Dict]:
        """Get current market maker trap data from Redis."""
        try:
            if not self.redis:
                return None
                
            trap_data = self.redis.get('current_trap_probability')
            if trap_data:
                return json.loads(trap_data)
                
        except Exception as e:
            logger.error(f"Error getting trap data: {e}")
            
        return None 