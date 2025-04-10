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
StrategicTrader Profile for OmegaBTC AI

This module simulates a disciplined trader who uses technical analysis and 
follows rules-based approaches with moderate risk management.
"""

import random
from typing import Dict, List, Tuple, Optional, Any
import time
from datetime import datetime
import logging

from .trader_base import TraderProfile, RiskParameters

# Configure logger
logger = logging.getLogger(__name__)

class StrategicTrader(TraderProfile):
    """Strategic trader that uses Fibonacci levels, market structure, and patience."""
    
    def __init__(self, initial_capital: float = 10000.0):
        """Initialize the strategic trader with calculated approach."""
        super().__init__(initial_capital)
        
        # Set trader name and type
        self.name = "Strategic Fibonacci Trader"
        
        # Strategic trader specific attributes
        self.patience_score = random.uniform(0.6, 0.9)  # Higher patience
        self.analysis_depth = random.uniform(0.7, 1.0)  # Deep analysis
        self.fomo_resistance = random.uniform(0.7, 0.95)  # High resistance to FOMO
        
        # Strategic parameters
        self.fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618]
        self.fib_proximity_threshold = 0.02  # 2% proximity to consider price near a Fibonacci level
        self.trend_confirmation_threshold = 0.6  # How strong trend must be to consider entry
        self.overbought_threshold = 0.8  # RSI-like threshold
        self.oversold_threshold = 0.2  # RSI-like threshold
        self.market_regime_accuracy = 0.7  # How accurate is regime identification
        
        # Fibonacci trading parameters
        self.primary_entry_level = 0.618  # Primary Fibonacci entry level
        self.secondary_entry_level = 0.786  # Secondary Fibonacci entry level
        self.stop_loss_level = 1.0  # Stop loss Fibonacci level
        self.take_profit_levels = [0.382, 0.236, 0.0]  # Take profit Fibonacci levels
        self.extension_take_profit = 1.618  # Extension target
        
        # OMEGA-FIED POSITION SCALING PARAMETERS
        self.enable_position_scaling = True  # Enable position scaling feature
        self.max_position_additions = 3  # Maximum number of times to add to a position
        self.position_additions_count = {}  # Track additions per symbol
        self.scale_size_multiplier = 0.5  # Each additional position is 50% of original
        self.scaling_fib_levels = [1.618, 2.618, 4.236]  # Fibonacci levels for scaling
        self.scale_proximity_threshold = 0.01  # 1% proximity for scaling levels
        self.scale_min_volume_factor = 1.2  # Minimum volume factor required to scale
        self.max_stack_limit = 5  # Never exceed this many position additions
        self.recent_scaling_operations = {}  # Track recent scaling operations for cooling period
        self.scaling_cooldown_seconds = 3600  # 1 hour cooldown between scale operations
        
        # Initialize the Fibonacci swing points tracking
        self.last_swing_high = None
        self.last_swing_low = None
        self.current_uptrend = None  # True if in uptrend, False if in downtrend, None if not determined
        self.fibonacci_retracements = {}  # Store calculated retracement levels
    
    def _get_risk_parameters(self) -> RiskParameters:
        """Get risk parameters specific to strategic trader profile."""
        return RiskParameters(
            max_risk_per_trade=0.02,  # 2% risk per trade
            base_leverage=11.0,       # High leverage setting (was 3.0)
            max_leverage=15.0,        # Increased max leverage (was 5.0) 
            min_risk_reward_ratio=random.uniform(1.5, 3.0),  # Minimum R:R to enter
            position_sizing_volatility_factor=0.7,  # Reduce size in high volatility
            stop_loss_multiplier=2.0,  # Wide stops based on market structure
            take_profit_multiplier=2.5  # Multiple take profit levels
        )
    
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if a trade should be entered based on market context."""
        current_price = market_context.get("price", 0)
        trend = market_context.get("trend", "neutral")
        regime = market_context.get("regime", "neutral")
        volatility = market_context.get("recent_volatility", 0)
        
        # Get Fibonacci levels and support/resistance
        fib_levels = self._get_support_resistance_levels()
        nearest_level = self._find_nearest_level(current_price, fib_levels)
        
        # Check if price is near a key level
        if not nearest_level:
            return False, "No key level nearby", "NEUTRAL", self.risk_params.base_leverage
        
        # Determine if we're at support or resistance
        is_support = self._is_support_level(current_price, nearest_level, None)
        is_resistance = self._is_resistance_level(current_price, nearest_level, None)
        
        # Check for retest confirmation
        if not self._check_retest_confirmation(current_price, nearest_level, None):
            return False, "No retest confirmation", "NEUTRAL", self.risk_params.base_leverage
        
        # Calculate leverage based on market conditions
        leverage = self._calculate_current_leverage(market_context)
        
        # Determine trade direction and reason
        if is_support and trend == "uptrend":
            return True, "Price at support in uptrend", "LONG", leverage
        elif is_resistance and trend == "downtrend":
            return True, "Price at resistance in downtrend", "SHORT", leverage
        
        return False, "No clear entry signal", "NEUTRAL", leverage
    
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on risk parameters and market conditions."""
        # Base position size on risk per trade
        risk_amount = self.capital * self.risk_params.max_risk_per_trade
        
        # Adjust for volatility
        volatility_factor = self.risk_params.position_sizing_volatility_factor
        if self.volatility > 0.02:  # High volatility
            volatility_factor *= 0.8
        
        # Calculate position size
        position_size = risk_amount * volatility_factor
        
        # Ensure position size doesn't exceed capital
        return min(position_size, self.capital)
    
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Set stop loss level based on strategic trader's risk management rules."""
        # Calculate base stop distance
        stop_distance = entry_price * 0.02  # 2% base stop
        
        # Adjust based on volatility
        stop_distance *= (1 + self.volatility)
        
        # Apply profile-specific multiplier
        stop_distance *= self.risk_params.stop_loss_multiplier
        
        if direction == "LONG":
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance
    
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set take profit levels based on strategic trader's profit-taking strategy."""
        # Calculate risk distance
        risk_distance = abs(entry_price - stop_loss)
        
        # Calculate minimum reward based on risk:reward ratio
        min_reward = risk_distance * self.risk_params.min_risk_reward_ratio
        
        # Create multiple take profit levels
        take_profits = []
        
        # First target: 1.5x risk
        take_profits.append({
            "price": entry_price + (min_reward * 0.6) if direction == "LONG" else entry_price - (min_reward * 0.6),
            "percentage": 0.4  # 40% of position
        })
        
        # Second target: 2.5x risk
        take_profits.append({
            "price": entry_price + (min_reward * 1.0) if direction == "LONG" else entry_price - (min_reward * 1.0),
            "percentage": 0.4  # 40% of position
        })
        
        # Third target: 3.5x risk
        take_profits.append({
            "price": entry_price + (min_reward * 1.5) if direction == "LONG" else entry_price - (min_reward * 1.5),
            "percentage": 0.2  # 20% of position
        })
        
        return take_profits
    
    def _find_nearest_level(self, price: float, levels_dict: Dict) -> Optional[Dict]:
        """Find the nearest Fibonacci or support/resistance level."""
        if not levels_dict:
            return None
            
        nearest = None
        min_distance = float('inf')
        
        for level in levels_dict.values():
            distance = abs(price - level["price"])
            if distance < min_distance:
                min_distance = distance
                nearest = level
        
        return nearest if min_distance <= price * self.fib_proximity_threshold else None
    
    def _get_support_resistance_levels(self) -> Dict:
        """Get support and resistance levels based on Fibonacci retracements."""
        levels = {}
        
        # Calculate Fibonacci levels
        for fib in self.fib_levels:
            levels[f"fib_{fib}"] = {
                "price": self.current_price * fib,
                "type": "fibonacci",
                "strength": 0.7
            }
        
        return levels
    
    def _is_support_level(self, price: float, fib_level: Optional[Dict], sr_level: Optional[Dict]) -> bool:
        """Determine if a level is acting as support."""
        if not fib_level:
            return False
            
        # Check if price is near the level
        if abs(price - fib_level["price"]) > price * self.fib_proximity_threshold:
            return False
            
        # Check if price is bouncing up from the level
        return self.trend_strength > self.trend_confirmation_threshold
    
    def _is_resistance_level(self, price: float, fib_level: Optional[Dict], sr_level: Optional[Dict]) -> bool:
        """Determine if a level is acting as resistance."""
        if not fib_level:
            return False
            
        # Check if price is near the level
        if abs(price - fib_level["price"]) > price * self.fib_proximity_threshold:
            return False
            
        # Check if price is bouncing down from the level
        return self.trend_strength > self.trend_confirmation_threshold
    
    def _check_retest_confirmation(self, price: float, fib_level: Optional[Dict], sr_level: Optional[Dict]) -> bool:
        """Check if price is confirming a level with a retest."""
        if not fib_level:
            return False
            
        # Check if price has recently tested the level
        recent_trades = self.state.recent_trades[-5:]  # Look at last 5 trades
        for trade in recent_trades:
            if abs(trade["price"] - fib_level["price"]) <= price * self.fib_proximity_threshold:
                return True
                
        return False
    
    def _calculate_current_leverage(self, market_context: Optional[Dict] = None) -> float:
        """Calculate current leverage based on market conditions and profile."""
        leverage = self.risk_params.base_leverage
        
        # Adjust based on volatility
        if market_context and "recent_volatility" in market_context:
            volatility = market_context["recent_volatility"]
            if volatility > 0.02:  # High volatility
                leverage *= 0.8
            elif volatility < 0.01:  # Low volatility
                leverage *= 1.2
        
        # Cap at max leverage
        return min(leverage, self.risk_params.max_leverage)
    
    # ======== Fibonacci-specific methods for integration with FibonacciProfileTrader ========
    
    def determine_entry_level(self, fib_levels: Dict[str, float], pattern_type: str) -> float:
        """
        Determine entry price level based on Fibonacci levels and pattern type.
        
        Args:
            fib_levels: Dictionary of calculated Fibonacci levels
            pattern_type: Type of pattern detected (e.g., "Bullish Gartley")
            
        Returns:
            Entry price level
        """
        # Primary entry is at 0.618 retracement for most patterns
        if 'bullish' in pattern_type.lower():
            # For bullish patterns, enter at 0.618 retracement
            return fib_levels.get('0.618', fib_levels.get('0.5', list(fib_levels.values())[0]))
        else:
            # For bearish patterns, enter at 0.618 retracement
            return fib_levels.get('0.618', fib_levels.get('0.5', list(fib_levels.values())[0]))
    
    def determine_stop_loss(self, fib_levels: Dict[str, float], pattern_type: str, entry_price: float) -> float:
        """
        Determine stop loss price based on Fibonacci levels and pattern type.
        
        Args:
            fib_levels: Dictionary of calculated Fibonacci levels
            pattern_type: Type of pattern detected
            entry_price: Entry price level
            
        Returns:
            Stop loss price level
        """
        # Stop loss at 1.0 level for retracement patterns
        if 'bullish' in pattern_type.lower():
            # For bullish patterns, stop below 1.0 level
            stop_level = fib_levels.get('1.0', fib_levels.get('0.786', entry_price * 0.95))
            # Add a small buffer
            return stop_level * 1.01
        else:
            # For bearish patterns, stop above 1.0 level
            stop_level = fib_levels.get('1.0', fib_levels.get('0.786', entry_price * 1.05))
            # Add a small buffer
            return stop_level * 0.99
    
    def determine_take_profit(self, fib_levels: Dict[str, float], pattern_type: str, entry_price: float) -> float:
        """
        Determine take profit price based on Fibonacci levels and pattern type.
        
        Args:
            fib_levels: Dictionary of calculated Fibonacci levels
            pattern_type: Type of pattern detected
            entry_price: Entry price level
            
        Returns:
            Take profit price level
        """
        # Take profit at extension level
        if 'bullish' in pattern_type.lower():
            # For bullish patterns, target 1.618 extension
            return fib_levels.get('1.618', entry_price * 1.05)
        else:
            # For bearish patterns, target 1.618 extension
            return fib_levels.get('1.618', entry_price * 0.95)
    
    def calculate_risk_levels(self, entry_price: float, risk_percent: float, account_size: float) -> Dict[str, float]:
        """
        Calculate comprehensive risk levels for a trade.
        
        Args:
            entry_price: Entry price level
            risk_percent: Risk percentage for the trade
            account_size: Current account size
            
        Returns:
            Dictionary with position size, stop loss, and take profit levels
        """
        # Get risk parameters
        risk_params = self._get_risk_parameters()
        
        # Calculate stop distance (2% of entry price by default)
        stop_distance = entry_price * 0.02 * risk_params.stop_loss_multiplier
        
        # Calculate stop loss
        stop_loss = entry_price - stop_distance  # For long position
        
        # Calculate take profit levels
        take_profit_distance = stop_distance * risk_params.min_risk_reward_ratio
        take_profit = entry_price + take_profit_distance  # For long position
        
        # Calculate position size based on risk
        risk_amount = account_size * (risk_percent / 100)
        position_size = risk_amount / stop_distance
        
        return {
            "position_size": position_size,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_amount": risk_amount
        }
    
    def validate_trade_signal(self, signal: Any) -> bool:
        """
        Validate a trading signal based on strategic trader criteria.
        
        Args:
            signal: Trading signal object
            
        Returns:
            True if signal is valid, False otherwise
        """
        # Calculate risk-reward ratio
        risk = abs(signal.entry_price - signal.stop_loss)
        reward = abs(signal.take_profit - signal.entry_price)
        risk_reward_ratio = reward / risk if risk > 0 else 0
        
        # Validate pattern confidence
        min_confidence = 0.65  # Strategic traders want high confidence
        if signal.confidence < min_confidence:
            return False
        
        # Validate risk-reward ratio
        min_rr = self._get_risk_parameters().min_risk_reward_ratio
        if risk_reward_ratio < min_rr:
            return False
        
        # Validate risk percent
        max_risk = self._get_risk_parameters().max_risk_per_trade * 100
        if signal.risk_percent > max_risk:
            return False
        
        return True
    
    def calculate_trailing_stop(self, position: Dict[str, Any], current_price: float) -> float:
        """
        Calculate trailing stop price based on position and current price.
        
        Args:
            position: Position data including entry price and side
            current_price: Current market price
            
        Returns:
            Updated stop loss price
        """
        entry_price = float(position.get('entryPrice', 0))
        position_side = position.get('side', '')
        
        # No trailing stop until 1.5% profit
        min_profit_percent = 0.015  # 1.5%
        
        if position_side == 'long':
            profit_percent = (current_price - entry_price) / entry_price
            if profit_percent < min_profit_percent:
                return 0  # No trailing stop yet
                
            # Move stop to breakeven + 0.5% when 1.5% in profit
            if profit_percent >= min_profit_percent and profit_percent < 0.03:
                return entry_price * 1.005
                
            # Trail at 50% of profit when >3% in profit
            if profit_percent >= 0.03:
                trail_distance = (current_price - entry_price) * 0.5
                return current_price - trail_distance
        else:  # short
            profit_percent = (entry_price - current_price) / entry_price
            if profit_percent < min_profit_percent:
                return 0  # No trailing stop yet
                
            # Move stop to breakeven + 0.5% when 1.5% in profit
            if profit_percent >= min_profit_percent and profit_percent < 0.03:
                return entry_price * 0.995
                
            # Trail at 50% of profit when >3% in profit
            if profit_percent >= 0.03:
                trail_distance = (entry_price - current_price) * 0.5
                return current_price + trail_distance
        
        return 0  # Default fallback
    
    def check_for_position_scaling(self, symbol: str, current_price: float, 
                                  current_positions: List[Dict], 
                                  market_data: Optional[Dict] = None) -> Tuple[bool, Optional[Dict]]:
        """
        Check if we should scale (add to) an existing position based on Fibonacci levels.
        
        Args:
            symbol: Trading symbol
            current_price: Current market price
            current_positions: List of current open positions
            market_data: Additional market data (volume, etc.)
            
        Returns:
            Tuple[bool, Optional[Dict]]: (should_scale, scaling_info)
        """
        # Skip if scaling is disabled
        if not self.enable_position_scaling:
            return False, None
            
        # Get all open positions for the symbol
        open_positions = [p for p in current_positions if 
                          p.get('symbol') == symbol and 
                          p.get('contracts', 0) > 0]
        
        if not open_positions:
            return False, None
            
        # Only scale LONG positions for now (modify logic for shorts if needed)
        long_positions = [p for p in open_positions if p.get('direction', '').upper() == 'LONG']
        if not long_positions:
            return False, None
            
        # Check if we've reached the maximum number of additions
        symbol_key = symbol.replace('/', '_').replace(':', '_')
        current_additions = self.position_additions_count.get(symbol_key, 0)
        if current_additions >= self.max_position_additions:
            return False, None
            
        # Check for cooldown period
        last_scale_time = self.recent_scaling_operations.get(symbol_key, 0)
        current_time = time.time()
        if (current_time - last_scale_time) < self.scaling_cooldown_seconds:
            # Still in cooldown period
            return False, None
            
        # Calculate weighted average entry price and total size
        total_size = sum(float(p.get('contracts', 0)) for p in long_positions)
        weighted_entry = sum(float(p.get('entryPrice', 0)) * float(p.get('contracts', 0)) 
                            for p in long_positions) / total_size
        
        # Generate Fibonacci retracement levels from our high and low
        # Either use stored high/low swing points or derive from position entry
        if self.last_swing_high is None or self.last_swing_low is None:
            # If we don't have swing points, use entry price +/- 5% for estimation
            high_price = weighted_entry * 1.05
            low_price = weighted_entry * 0.95
        else:
            high_price = self.last_swing_high
            low_price = self.last_swing_low
        
        # Calculate Fibonacci retracement levels
        fib_levels = self.calculate_fibonacci_retracements(high_price, low_price)
        
        # Check if current price is near a scaling Fibonacci level
        for fib_level in self.scaling_fib_levels:
            level_key = str(fib_level)
            if level_key in fib_levels:
                level_price = fib_levels[level_key]
                
                # Check if price is within proximity threshold of this level
                price_diff_pct = abs(current_price - level_price) / level_price
                
                if price_diff_pct <= self.scale_proximity_threshold:
                    # We're at a scaling fib level - check volume if available
                    if self.check_volume_confirmation(market_data):
                        # Check for MM traps before scaling
                        if self.check_for_mm_traps(current_price, symbol):
                            # Calculate the size for this addition
                            base_size = float(long_positions[0].get('contracts', 0))
                            # Use a progressively smaller size for each addition
                            adjustment_factor = self.scale_size_multiplier / (1 + current_additions * 0.25)
                            scale_size = base_size * adjustment_factor
                            
                            # Calculate new stop loss based on weighted average
                            new_stop_loss = self.calculate_dynamic_stop_loss(
                                weighted_entry, 
                                current_additions + 1,
                                current_price
                            )
                            
                            # Prepare scaling info
                            scaling_info = {
                                'side': 'long',
                                'size': scale_size,
                                'reason': f"Adding at {level_key} Fibonacci level",
                                'current_price': current_price,
                                'weighted_entry': weighted_entry,
                                'fib_level': level_key,
                                'stop_loss': new_stop_loss
                            }
                            
                            # Update records
                            self.position_additions_count[symbol_key] = current_additions + 1
                            self.recent_scaling_operations[symbol_key] = current_time
                            
                            return True, scaling_info
        
        return False, None
    
    def calculate_fibonacci_retracements(self, high_price: float, low_price: float) -> Dict[str, float]:
        """
        Calculate Fibonacci retracement and extension levels for scaling decisions.
        
        Args:
            high_price: The swing high price
            low_price: The swing low price
            
        Returns:
            Dict of Fibonacci levels with prices
        """
        # Calculate the price range
        price_range = high_price - low_price
        
        # Standard Fibonacci retracement levels
        levels = {
            '0': low_price,
            '0.236': low_price + 0.236 * price_range,
            '0.382': low_price + 0.382 * price_range,
            '0.5': low_price + 0.5 * price_range,
            '0.618': low_price + 0.618 * price_range,
            '0.786': low_price + 0.786 * price_range,
            '1.0': high_price,
        }
        
        # Add Fibonacci extension levels (these are below the low for downward extensions)
        levels.update({
            '1.618': low_price - 0.618 * price_range,  # Extension below
            '2.618': low_price - 1.618 * price_range,  # Deeper extension
            '4.236': low_price - 3.236 * price_range,  # Major extension
        })
        
        # Store for future reference
        self.fibonacci_retracements = levels
        
        return levels
    
    def check_volume_confirmation(self, market_data: Optional[Dict]) -> bool:
        """
        Check if volume supports adding to the position.
        
        Args:
            market_data: Market data with volume information
            
        Returns:
            bool: True if volume supports scaling, False otherwise
        """
        if not market_data:
            # Default to conservative approach if no data
            return False
            
        # Extract volume info
        current_volume = market_data.get('volume', 0)
        avg_volume = market_data.get('average_volume', 0)
        
        # Ensure we have both values
        if current_volume <= 0 or avg_volume <= 0:
            return False
            
        # Check if current volume exceeds our threshold compared to average
        volume_factor = current_volume / avg_volume
        
        return volume_factor >= self.scale_min_volume_factor
    
    def check_for_mm_traps(self, current_price: float, symbol: str) -> bool:
        """
        Check for market maker traps before scaling.
        
        Args:
            current_price: Current market price
            symbol: Trading symbol
            
        Returns:
            bool: True if no trap detected, False if trap detected
        """
        try:
            # Simple implementation - in a real system, integrate with mm_trap_detector
            # You would normally import and use your trap detector here
            
            # Create a random chance of trap detection for this demo
            # This is a placeholder - implement real trap detection logic
            random_value = random.random()
            trap_detected = random_value < 0.2  # 20% chance of trap detection
            
            if trap_detected:
                logger.warning(f"MM TRAP DETECTED at {current_price} for {symbol} - Avoiding position scaling")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking MM traps: {str(e)}")
            # Default to being cautious if detector fails
            return False
    
    def calculate_dynamic_stop_loss(self, weighted_entry: float, additions_count: int, 
                                   current_price: float) -> float:
        """
        Calculate a dynamic stop loss based on weighted average entry and number of additions.
        
        Args:
            weighted_entry: Weighted average entry price
            additions_count: Number of additions to the position
            current_price: Current market price
            
        Returns:
            float: New stop loss price
        """
        # Base risk percentage - decrease with each addition (tighten stop loss)
        base_risk_pct = self.risk_params.max_risk_per_trade * (1 - (additions_count * 0.1))
        
        # Don't let the risk go below 0.5%
        risk_pct = max(0.005, base_risk_pct)
        
        # Calculate stop loss below weighted entry
        stop_loss = weighted_entry * (1 - risk_pct)
        
        # If price has moved up significantly, implement a trailing stop
        upside_buffer = weighted_entry * 0.01  # 1% buffer
        if current_price > (weighted_entry + upside_buffer):
            # Price has moved up - implement trailing stop at (price - trailing_distance)
            trailing_distance = current_price * risk_pct * 1.5  # 1.5x normal distance for trailing
            trailing_stop = current_price - trailing_distance
            
            # Use the higher of the two stops
            stop_loss = max(stop_loss, trailing_stop)
        
        return stop_loss
    
    def update_swing_points(self, new_price: float, timestamp: datetime) -> None:
        """
        Update the swing high/low points used for Fibonacci calculations.
        
        Args:
            new_price: The latest price
            timestamp: The timestamp of the price
        """
        # In a full implementation, this would use a proper swing point detection algorithm
        # For this demo, we'll use a simple approach:
        
        # Initialize swing points if they don't exist
        if self.last_swing_high is None:
            self.last_swing_high = new_price * 1.05  # Estimate
        if self.last_swing_low is None:
            self.last_swing_low = new_price * 0.95  # Estimate
        
        # Update swing high if we have a new high
        if new_price > self.last_swing_high:
            self.last_swing_high = new_price
            # If we make a new high, we might be in an uptrend
            self.current_uptrend = True
            
        # Update swing low if we have a new low
        if new_price < self.last_swing_low:
            self.last_swing_low = new_price
            # If we make a new low, we might be in a downtrend
            self.current_uptrend = False