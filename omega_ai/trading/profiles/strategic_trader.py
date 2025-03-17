#!/usr/bin/env python3

"""
StrategicTrader Profile for OmegaBTC AI

This module simulates a disciplined trader who uses technical analysis and 
follows rules-based approaches with moderate risk management.
"""

import random
from typing import Dict, List, Tuple, Optional
import time

from omega_ai.trading.trader_base import (
    TraderProfile,  # This is the correct class name 
    RESET, GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, WHITE, BOLD
)

class StrategicTrader(TraderProfile):
    """Strategic trader that uses Fibonacci levels, market structure, and patience."""
    
    def __init__(self, initial_capital: float = 10000.0):
        """Initialize the strategic trader with calculated approach."""
        super().__init__(initial_capital)
        
        # Set trader name and type
        self.name = "Strategic Fibonacci Trader"
        self.type = "strategic"
        
        # Explicitly set base_leverage (even though it's in parent class)
        self.base_leverage = 3.0  # Strategic traders use moderate leverage
        
        # Strategic trader specific attributes
        self.patience_score = random.uniform(0.6, 0.9)  # Higher patience
        self.analysis_depth = random.uniform(0.7, 1.0)  # Deep analysis
        self.fomo_resistance = random.uniform(0.7, 0.95)  # High resistance to FOMO
        
        # Risk management parameters
        self.max_risk_per_trade = 0.02  # 2% risk per trade
        self.position_sizing_volatility_factor = 0.7  # Reduce size in high volatility
        
        # Strategic parameters
        self.min_risk_reward_ratio = random.uniform(1.5, 3.0)  # Minimum R:R to enter
        self.fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618]
        self.fib_proximity_threshold = 0.02  # 2% proximity to consider price near a Fibonacci level
        self.trend_confirmation_threshold = 0.6  # How strong trend must be to consider entry
        self.overbought_threshold = 0.8  # RSI-like threshold
        self.oversold_threshold = 0.2  # RSI-like threshold
        self.market_regime_accuracy = 0.7  # How accurate is regime identification
        
        # Track performance metrics
        self.avg_trade_duration = 0
        self.trade_durations = []
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0

    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Strategic entry based on Fibonacci levels and trend alignment."""
        price = market_context.get("price", 0)
        if price <= 0:
            return False, "No price data", "", 0
        
        # Get Fibonacci levels from market context
        fib_levels = market_context.get("fib_levels", {})
        if not fib_levels:
            # Try to get from Redis directly
            fib_data = self.redis_conn.hgetall("realtime_fibonacci_levels")
            if fib_data:
                for level_name, price_str in fib_data.items():
                    if level_name != "timestamp":
                        try:
                            # Convert level name to float if possible
                            try:
                                level_value = float(level_name)
                                if level_value in self.key_fib_levels:
                                    fib_levels[level_value] = float(price_str)
                            except ValueError:
                                # Handle format like "R0.618"
                                if level_name.startswith("R"):
                                    level_str = level_name[1:]
                                    try:
                                        level_value = float(level_str)
                                        if level_value in self.key_fib_levels:
                                            fib_levels[level_value] = float(price_str)
                                    except ValueError:
                                        pass
                        except ValueError:
                            pass
        
        # Get key support/resistance levels
        sr_levels = self._get_support_resistance_levels()
        
        # Calculate current leverage based on current market conditions
        current_leverage = self._calculate_current_leverage(market_context)
        
        # Signal variables
        entry_signal = False
        direction = ""
        reason = ""
        
        # Check for retest of key Fibonacci levels
        nearest_fib = self._find_nearest_level(price, fib_levels)
        nearest_sr = self._find_nearest_level(price, sr_levels)
        
        # Calculate distances as percentages
        fib_distance_pct = abs(price - nearest_fib["price"]) / price if nearest_fib else 1.0
        sr_distance_pct = abs(price - nearest_sr["price"]) / price if nearest_sr else 1.0
        
        # Get market bias for directional alignment
        market_bias = market_context.get("market_bias", "")
        
        # Check if price is near key technical level
        near_key_level = (nearest_fib and fib_distance_pct < self.fib_proximity_threshold) or \
                         (nearest_sr and sr_distance_pct < self.fib_proximity_threshold)
                         
        # Check for retest confirmation
        retest_confirmed = self._check_retest_confirmation(price, nearest_fib, nearest_sr)
        
        # LONG setup - Price retesting support level in bullish market
        if near_key_level and retest_confirmed and \
           (("Bullish" in market_bias and self._is_support_level(price, nearest_fib, nearest_sr)) or \
            ("Strong Bullish" in market_bias)):
            entry_signal = True
            direction = "LONG"
            level_type = "Fibonacci" if nearest_fib and fib_distance_pct < sr_distance_pct else "Support"
            level_value = nearest_fib["level"] if level_type == "Fibonacci" else nearest_sr["level"]
            reason = f"{level_type} level {level_value} retest confirmed in {market_bias} market"
        
        # SHORT setup - Price retesting resistance level in bearish market
        elif near_key_level and retest_confirmed and \
             (("Bearish" in market_bias and self._is_resistance_level(price, nearest_fib, nearest_sr)) or \
              ("Strong Bearish" in market_bias)):
            entry_signal = True
            direction = "SHORT"
            level_type = "Fibonacci" if nearest_fib and fib_distance_pct < sr_distance_pct else "Resistance"
            level_value = nearest_fib["level"] if level_type == "Fibonacci" else nearest_sr["level"]
            reason = f"{level_type} level {level_value} retest confirmed in {market_bias} market"
        
        # Skip trades in choppy markets where bias is neutral
        if entry_signal and "Neutral" in market_bias:
            # Disciplined approach - skip dubious setups
            if random.random() > self.patience_score:  # Higher patience means more likely to skip
                self.discipline_metrics["entries_skipped"] += 1
                return False, "", "", 0
        
        # Psychological override - may rarely break rules due to FOMO
        # Much less likely than aggressive trader
        if not entry_signal and self.state.emotional_state == "greedy" and random.random() < 0.15:
            # Only 15% chance to break rules when greedy (compared to 40% for aggressive)
            self.discipline_metrics["rules_broken"] += 1
            entry_signal = True
            direction = "LONG" if "Bullish" in market_bias else "SHORT"
            reason = "Breaking rules due to FOMO (greedy state)"
        
        # If we found a valid setup, note that we followed rules
        if entry_signal and "Breaking rules" not in reason:
            self.discipline_metrics["rules_followed"] += 1
        
        return entry_signal, direction, reason, current_leverage
    
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate strategic position size based on risk parameters."""
        # Strategic traders are more consistent with position sizing
        base_risk_pct = self.min_risk_per_trade
        
        # Less emotional variation than aggressive trader
        if self.state.emotional_state == "greedy":
            risk_pct = min(base_risk_pct * 1.3, self.max_risk_per_trade)
        elif self.state.emotional_state == "fearful":
            risk_pct = base_risk_pct * 0.7
        else:
            risk_pct = base_risk_pct
        
        # Smaller adjustments based on recent performance
        if self.state.consecutive_wins >= 3:
            # Small size increase after winning streak
            risk_pct *= (1 + min(self.state.consecutive_wins * 0.05, 0.2))
        elif self.state.consecutive_losses >= 2:
            # Small size decrease after losing streak
            risk_pct *= (1 - min(self.state.consecutive_losses * 0.05, 0.2))
        
        # Calculate position size in BTC
        amount_at_risk = self.capital * risk_pct
        leverage = self._calculate_current_leverage(None)
        
        # Strategic traders use wider stops, typically 2-3%
        stop_distance_pct = self.base_stop_pct
        
        position_size = amount_at_risk / (entry_price * stop_distance_pct)
        position_size = position_size / leverage  # Adjust for leverage
        
        # Cap to avoid over-leveraging
        max_size = self.capital * leverage / entry_price * 0.9  # More conservative cap
        position_size = min(position_size, max_size)
        
        return position_size
    
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Determine strategic stop-loss level (wider than aggressive)."""
        # Strategic traders use wider initial stops
        stop_pct = self.base_stop_pct
        
        # Small adjustments based on emotional state
        if self.state.emotional_state == "greedy":
            stop_pct *= 0.9  # 10% tighter when greedy
        elif self.state.emotional_state == "fearful":
            stop_pct *= 1.1  # 10% wider when fearful
        
        # Calculate stop price
        if direction == "LONG":
            stop_price = entry_price * (1 - stop_pct)
        else:  # SHORT
            stop_price = entry_price * (1 + stop_pct)
        
        return stop_price
    
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set take-profit levels with 1:2 risk-reward for first target."""
        take_profits = []
        
        # Calculate risk in dollars
        risk = abs(entry_price - stop_loss)
        
        # First take-profit at 1:2 risk/reward (strategic approach)
        if direction == "LONG":
            tp1_price = entry_price + (risk * 2)  # 1:2 risk reward
            tp2_price = entry_price + (risk * 3)  # 1:3 risk reward
            tp3_price = entry_price + (risk * 5)  # 1:5 risk reward
        else:  # SHORT
            tp1_price = entry_price - (risk * 2)  # 1:2 risk reward
            tp2_price = entry_price - (risk * 3)  # 1:3 risk reward
            tp3_price = entry_price - (risk * 5)  # 1:5 risk reward
        
        # Strategic traders have more consistent take-profit approach
        # Less affected by emotional state
        take_profits = [
            {"price": tp1_price, "percentage": 0.4, "hit": False},
            {"price": tp2_price, "percentage": 0.4, "hit": False},
            {"price": tp3_price, "percentage": 0.2, "hit": False}
        ]
        
        return take_profits
    
    def process_trade_result(self, result: float, trade_duration: float) -> None:
        """Process the outcome of a trade with strategic discipline."""
        # Update standard metrics
        super().process_trade_result(result, trade_duration)
        
        # Update discipline metrics
        if result > 0:
            # For winning trades, were targets reached?
            if trade_duration > 5.0:  # Longer duration suggests targets were reached
                self.discipline_metrics["targets_reached"] += 1
            else:
                self.discipline_metrics["early_exits"] += 1
                
        # Strategic traders' emotional states are more stable
        # Reduce emotional swings by overriding the emotional state updates
        if self.state.emotional_state == "greedy" and result < 0:
            # Losses more quickly return greedy traders to neutral
            self.state.emotional_state = "neutral"
            self.state.risk_appetite = max(0.3, self.state.risk_appetite - 0.1)
        elif self.state.emotional_state == "fearful" and result > 0:
            # Wins more quickly restore confidence from fearful state
            self.state.emotional_state = "neutral"
            self.state.risk_appetite = min(0.7, self.state.risk_appetite + 0.1)
    
    def print_status(self) -> None:
        """Print current trader status with added discipline metrics."""
        # Call the parent class method to print standard metrics
        super().print_status()
        
        # Add discipline metrics
        wins = self.state.winning_trades
        losses = self.state.losing_trades
        total_trades = wins + losses
        
        if total_trades > 0:
            rules_followed_pct = (self.discipline_metrics["rules_followed"] / total_trades) * 100
            targets_reached_pct = (self.discipline_metrics["targets_reached"] / max(1, wins)) * 100
            
            print(f"\n{CYAN}Discipline Metrics:{RESET}")
            print(f"Rules Followed: {self.discipline_metrics['rules_followed']}/{total_trades} ({rules_followed_pct:.1f}%)")
            print(f"Entries Skipped: {self.discipline_metrics['entries_skipped']}")
            print(f"Rules Broken: {self.discipline_metrics['rules_broken']}")
            print(f"Targets Reached: {self.discipline_metrics['targets_reached']}/{wins} ({targets_reached_pct:.1f}%)")
            print(f"Early Exits: {self.discipline_metrics['early_exits']}")
            
            # Calculate and display patience score
            patience_ratio = self.discipline_metrics["entries_skipped"] / max(1, self.discipline_metrics["entries_skipped"] + total_trades)
            self.patience_score = 0.3 + (patience_ratio * 0.7)  # Scale to 0.3-1.0 range
            print(f"Patience Score: {self.patience_score:.2f}/1.00")
    
    def _find_nearest_level(self, price: float, levels_dict: Dict) -> Optional[Dict]:
        """Find the nearest technical level to current price."""
        if not levels_dict:
            return None
            
        nearest_level = None
        nearest_distance = float('inf')
        
        for level, level_price in levels_dict.items():
            distance = abs(price - level_price)
            if distance < nearest_distance:
                nearest_distance = distance
                # Convert level to float if possible
                try:
                    level_float = float(level)
                except (ValueError, TypeError):
                    level_float = level  # Keep as string if conversion fails
                
                nearest_level = {"level": level_float, "price": level_price, "distance": distance}
        
        return nearest_level
    
    def _get_support_resistance_levels(self) -> Dict:
        """Get support/resistance levels from Redis."""
        try:
            sr_data = self.redis_conn.hgetall("support_resistance_levels")
            sr_levels = {}
            
            for level_name, price_str in sr_data.items():
                if level_name != "timestamp":
                    try:
                        sr_levels[level_name] = float(price_str)
                    except ValueError:
                        pass
                        
            return sr_levels
        except Exception:
            return {}
    
    def _is_support_level(self, price: float, fib_level: Optional[Dict], sr_level: Optional[Dict]) -> bool:
        """Determine if the nearest level is a support level (below current price)."""
        # For Fibonacci, levels below 0.5 are supports in an uptrend
        if fib_level and fib_level["level"] <= 0.5:
            return price > fib_level["price"]
        
        # For S/R, check if level is labeled as support
        if sr_level and "support" in str(sr_level["level"]).lower():
            return True
            
        # Otherwise check if price is above the level
        if sr_level:
            return price > sr_level["price"]
            
        return False
    
    def _is_resistance_level(self, price: float, fib_level: Optional[Dict], sr_level: Optional[Dict]) -> bool:
        """Determine if the nearest level is a resistance level (above current price)."""
        # For Fibonacci, levels above 0.5 are resistances in a downtrend
        if fib_level and fib_level["level"] >= 0.5:
            return price < fib_level["price"]
        
        # For S/R, check if level is labeled as resistance
        if sr_level and "resistance" in str(sr_level["level"]).lower():
            return True
            
        # Otherwise check if price is below the level
        if sr_level:
            return price < sr_level["price"]
            
        return False
    
    def _check_retest_confirmation(self, price: float, fib_level: Optional[Dict], sr_level: Optional[Dict]) -> bool:
        """Check if a retest of a level has been confirmed by price action."""
        # In a real system, this would analyze recent candles for confirmation
        # For simulation, use a probability-based approach that improves with patience
        
        # Get the level we're checking
        level_price = None
        if fib_level and sr_level:
            # Use the closer level
            if fib_level["distance"] < sr_level["distance"]:
                level_price = fib_level["price"]
            else:
                level_price = sr_level["price"]
        elif fib_level:
            level_price = fib_level["price"]
        elif sr_level:
            level_price = sr_level["price"]
        else:
            return False
        
        # Check if we had recent confirmation
        last_retest_time = self.redis_conn.get("last_level_retest_time")
        if last_retest_time:
            time_since_retest = time.time() - float(last_retest_time)
            if time_since_retest < self.min_retest_waiting_period:
                # Not enough time has passed to confirm retest
                return False
        
        # Higher patience score increases confirmation probability
        confirmation_chance = 0.3 + (0.4 * self.patience_score)
        is_confirmed = random.random() < confirmation_chance
        
        if is_confirmed:
            # Store confirmation time
            self.redis_conn.set("last_level_retest_time", time.time())
            
        return is_confirmed
    
    def _calculate_current_leverage(self, market_context: Optional[Dict]) -> float:
        """Calculate appropriate leverage based on market conditions and trader state."""
        # Base leverage range is 5-10x
        leverage = self.base_leverage
        
        # Get volatility info if available
        volatility_factor = 1.0
        if market_context:
            # Lower leverage in high volatility
            volatility = market_context.get("recent_volatility", 0)
            if volatility > 300:
                volatility_factor = 0.8
            elif volatility > 500:
                volatility_factor = 0.7
        
        # Adjust leverage based on emotional state (less variation than aggressive)
        if self.state.emotional_state == "greedy":
            leverage *= 1.2  # 20% increase when greedy
        elif self.state.emotional_state == "fearful":
            leverage *= 0.8  # 20% decrease when fearful
        
        # Applying volatility factor
        leverage *= volatility_factor
        
        # Ensure leverage stays within 5x-10x range
        return max(5, min(leverage, 10))