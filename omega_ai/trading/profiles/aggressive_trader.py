#!/usr/bin/env python3

"""
AggressiveTrader Profile for OmegaBTC AI

This module simulates a high-leverage momentum trader focused on rapid moves and volume spikes.
Aggressive traders are characterized by:
- Higher leverage (20x-50x)
- Faster entries on momentum signals
- Tighter stop losses (0.5-1.5%)
- Shorter holding periods
- More emotional decision-making
"""

import random
from typing import Dict, List, Tuple, Optional
import time

from omega_ai.trading.trader_base import (
    TraderProfile, 
    RESET, GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, WHITE, BOLD
)

class AggressiveTrader(TraderProfile):
    """
    A high-leverage aggressive trader focused on momentum and volume.
    
    This trader profile specializes in short-term momentum trading with high leverage,
    tight stops, and quick profit-taking. They're particularly sensitive to
    technical indicators like RSI, MACD, and volume spikes.
    """
    
    def __init__(self, initial_capital: float = 10000.0):
        super().__init__(initial_capital, name="Aggressive Momentum Trader")
        # Trading parameters
        self.base_leverage = 20        # Base leverage (will scale up to 50x)
        self.min_risk_per_trade = 0.05  # 5% of capital at risk per trade
        self.max_risk_per_trade = 0.15  # Up to 15% of capital at risk per trade
        
        # Technical indicator thresholds
        self.rsi_period = 14
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        self.volume_spike_threshold = 1.8  # Volume spike multiplier threshold
        self.momentum_threshold = 0.005    # 0.5% price change threshold for momentum
        
        # Psychological traits
        self.state.risk_appetite = 0.8    # Starts with high risk appetite
        self.state.confidence = 0.7       # Starts confident
        self.state.emotional_state = "excited"  # Starts excited
        self.impulsiveness = 0.7          # Tendency for impulsive decisions (0-1)
        self.fomo_susceptibility = 0.8    # Susceptibility to FOMO (0-1)
        
        # Performance tracking
        self.trade_durations = []         # Track how long trades are held
        self.emotion_trade_correlation = {"greedy": 0, "fearful": 0, "neutral": 0, "excited": 0}
        self.successful_signals = {       # Track which signals perform best
            "rsi_oversold": {"wins": 0, "losses": 0},
            "rsi_overbought": {"wins": 0, "losses": 0},
            "macd_crossover": {"wins": 0, "losses": 0},
            "volume_spike": {"wins": 0, "losses": 0},
            "momentum_breakout": {"wins": 0, "losses": 0},
            "emotional_entry": {"wins": 0, "losses": 0}
        }
        self.last_trade_signal = None     # Track which signal triggered last trade
        
        print(f"{YELLOW}Initialized {self.name} with ${initial_capital:.2f}{RESET}")
    
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """
        Determine if the trader should enter a trade based on momentum and volume.
        
        Aggressive traders look for:
        - RSI overbought/oversold conditions
        - MACD crossovers
        - Volume spikes
        - Short-term momentum breakouts
        - Price moves above/below key moving averages
        
        They're also susceptible to emotional trading in certain states.
        """
        price = market_context.get("price", 0)
        if price <= 0:
            return False, "No price data", "", 0
            
        # Get technical indicator values from Redis
        rsi = self._get_indicator_value("rsi_14")
        macd = self._get_indicator_value("macd")
        macd_signal = self._get_indicator_value("macd_signal")
        sma_20 = self._get_indicator_value("sma_20")
        sma_50 = self._get_indicator_value("sma_50")
        volume_change = self._calculate_volume_change()
        price_change_1h = market_context.get("price_change_1h", 0)
        recent_price_direction = market_context.get("recent_change", 0)
        
        # Calculate current leverage based on emotional state
        current_leverage = self._calculate_current_leverage()
        
        # Signal variables
        entry_signal = False
        direction = ""
        reason = ""
        signal_strength = 0.0  # 0.0-1.0 score of signal confidence
        
        # 1. Check for RSI conditions
        if rsi is not None:
            if rsi < self.rsi_oversold:
                signal_strength = 0.7 + (self.rsi_oversold - rsi) / 30  # Stronger as RSI gets lower
                entry_signal = True
                direction = "LONG"
                reason = f"RSI oversold ({rsi:.1f})"
                # Add additional context if MACD also confirms
                if macd is not None and macd_signal is not None and macd > macd_signal:
                    reason += " with bullish MACD crossover"
                    signal_strength += 0.2
            elif rsi > self.rsi_overbought:
                signal_strength = 0.7 + (rsi - self.rsi_overbought) / 30  # Stronger as RSI gets higher
                entry_signal = True
                direction = "SHORT"
                reason = f"RSI overbought ({rsi:.1f})"
                # Add additional context if MACD also confirms
                if macd is not None and macd_signal is not None and macd < macd_signal:
                    reason += " with bearish MACD crossover"
                    signal_strength += 0.2
        
        # 2. Check for momentum breakouts - strong and quick moves
        if abs(price_change_1h) > self.momentum_threshold:
            momentum_signal_strength = min(1.0, abs(price_change_1h) * 100)  # Scale based on move size
            if (not entry_signal) or momentum_signal_strength > signal_strength:
                entry_signal = True
                direction = "LONG" if price_change_1h > 0 else "SHORT"
                reason = f"Momentum breakout ({price_change_1h:.2%} 1h change)"
                signal_strength = momentum_signal_strength
        
        # 3. Volume spike can trigger entry in trending direction
        if volume_change > self.volume_spike_threshold:
            market_bias = market_context.get("market_bias", "")
            volume_signal_strength = min(1.0, 0.6 + (volume_change - self.volume_spike_threshold) * 0.2)
            
            # If no signal yet or volume signal is stronger
            if (not entry_signal) or (volume_signal_strength > signal_strength):
                if "Bullish" in market_bias:
                    entry_signal = True
                    direction = "LONG"
                    reason = f"Volume spike ({volume_change:.1f}x) in bullish market"
                    signal_strength = volume_signal_strength
                elif "Bearish" in market_bias:
                    entry_signal = True
                    direction = "SHORT"
                    reason = f"Volume spike ({volume_change:.1f}x) in bearish market"
                    signal_strength = volume_signal_strength
        
        # 4. Moving average crossover checks
        if sma_20 is not None and sma_50 is not None:
            # Price crossing above/below both MAs
            if (price > sma_20 > sma_50) and (not entry_signal or signal_strength < 0.8):
                entry_signal = True
                direction = "LONG"
                reason = "Price above both 20 & 50 SMAs (bullish)"
                signal_strength = 0.8
            elif (price < sma_20 < sma_50) and (not entry_signal or signal_strength < 0.8):
                entry_signal = True
                direction = "SHORT"
                reason = "Price below both 20 & 50 SMAs (bearish)"
                signal_strength = 0.8
        
        # 5. Emotional overrides - impulsive entries
        emotional_override = False
        if self._should_make_emotional_entry():
            if self.state.emotional_state == "greedy":
                # FOMO entry based on recent price direction
                entry_signal = True
                direction = "LONG" if recent_price_direction > 0 else "SHORT"
                reason = f"FOMO entry on {direction} momentum"
                signal_strength = 0.4  # Lower quality signal
                self.emotion_trade_correlation["greedy"] += 1
                emotional_override = True
            
            elif self.state.emotional_state == "fearful" and self.state.consecutive_losses >= 2:
                # Revenge trade after losses
                entry_signal = True
                # Often reverses previous losing direction
                prev_losing_direction = "SHORT" if self.last_trade_direction == "LONG" else "LONG"
                direction = prev_losing_direction
                reason = f"Revenge trade after {self.state.consecutive_losses} losses"
                signal_strength = 0.3  # Even lower quality signal
                self.emotion_trade_correlation["fearful"] += 1
                emotional_override = True
        
        # Store which signal generated this trade for later analysis
        if entry_signal:
            if "RSI oversold" in reason:
                self.last_trade_signal = "rsi_oversold"
            elif "RSI overbought" in reason:
                self.last_trade_signal = "rsi_overbought"
            elif "MACD" in reason:
                self.last_trade_signal = "macd_crossover"
            elif "Volume spike" in reason:
                self.last_trade_signal = "volume_spike"
            elif "Momentum breakout" in reason:
                self.last_trade_signal = "momentum_breakout"
            elif emotional_override:
                self.last_trade_signal = "emotional_entry"
            
            # Store direction for later reference
            self.last_trade_direction = direction
        
        return entry_signal, direction, reason, current_leverage
    
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """
        Calculate aggressive position size based on risk parameters and emotional state.
        
        Aggressive traders will:
        - Increase size after winning streaks
        - Decrease size after losing streaks
        - Size up when greedy
        - Size down when fearful
        - Never risk more than max_risk_per_trade of capital
        """
        # Base risk percentage varies with emotional state
        if self.state.emotional_state == "greedy":
            risk_pct = self.max_risk_per_trade * (1 + self.fomo_susceptibility * 0.3)
            risk_pct = min(risk_pct, self.max_risk_per_trade * 1.5)  # Cap at 150% of max
        elif self.state.emotional_state == "fearful":
            risk_pct = self.min_risk_per_trade * 0.8  # Reduce size when fearful
        elif self.state.emotional_state == "excited":
            risk_pct = self.max_risk_per_trade * 0.9  # Almost max size when excited
        else:  # neutral
            risk_pct = self.min_risk_per_trade + (self.max_risk_per_trade - self.min_risk_per_trade) * self.state.risk_appetite
        
        # Scale based on recent performance - aggressive traders chase performance
        if self.state.consecutive_wins >= 2:
            # Size up aggressively after winning streak
            streak_multiplier = 1 + min(self.state.consecutive_wins * 0.15, 0.6)
            risk_pct *= streak_multiplier
        elif self.state.consecutive_losses >= 2:
            # Size down after losing streak
            risk_pct *= (1 - min(self.state.consecutive_losses * 0.15, 0.7))
        
        # Calculate position size in BTC
        amount_at_risk = self.capital * risk_pct
        leverage = self._calculate_current_leverage()
        
        # Calculate stop distance for this specific trade
        stop_distance_pct = self._calculate_stop_distance(direction)
        
        position_size = amount_at_risk / (entry_price * stop_distance_pct)
        position_size = position_size / leverage  # Adjust for leverage
        
        # Cap to avoid over-leveraging - aggressive traders tend toward max capacity
        max_size = self.capital * leverage / entry_price * 0.95
        position_size = min(position_size, max_size)
        
        return position_size
    
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """
        Determine aggressive stop-loss level (tight stops).
        
        Aggressive traders typically use tight stops (0.5-1.5%)
        adjusted based on volatility and emotional state.
        """
        # Get recent volatility from market context
        try:
            recent_volatility = float(self.redis_conn.get("recent_volatility") or 0)
        except (TypeError, ValueError):
            recent_volatility = 0
            
        # Base stop percentage, adjusted for volatility
        volatility_factor = max(1.0, min(2.0, recent_volatility / 300))
        base_stop_pct = 0.01 * volatility_factor  # 1% base, adjusted by volatility
        
        # Adjust based on emotional state
        if self.state.emotional_state == "greedy":
            # Tighter stops when greedy (overconfident)
            stop_pct = base_stop_pct * 0.7
        elif self.state.emotional_state == "fearful":
            # Wider stops when fearful
            stop_pct = base_stop_pct * 1.4
        elif self.state.emotional_state == "excited":
            # Very tight stops when excited
            stop_pct = base_stop_pct * 0.6
        else:
            stop_pct = base_stop_pct
        
        # Make sure stop isn't too tight based on recent volatility
        min_stop = recent_volatility / 10000 if recent_volatility > 0 else 0.005
        stop_pct = max(stop_pct, min_stop)
        
        # Calculate stop price
        if direction == "LONG":
            stop_price = entry_price * (1 - stop_pct)
        else:  # SHORT
            stop_price = entry_price * (1 + stop_pct)
        
        return stop_price
    
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """
        Set multiple take-profit levels with risk-reward ratios.
        
        Aggressive traders typically target initial 1:1 risk-reward
        and scale into 1:2 and 1:3 for the remainder of the position.
        """
        # Calculate risk in dollars
        risk = abs(entry_price - stop_loss)
        
        # Set take-profit levels based on risk multiples
        if direction == "LONG":
            tp1_price = entry_price + risk
            tp2_price = entry_price + (risk * 2)
            tp3_price = entry_price + (risk * 3)
        else:  # SHORT
            tp1_price = entry_price - risk
            tp2_price = entry_price - (risk * 2)
            tp3_price = entry_price - (risk * 3)
        
        # Adjust based on current emotional state
        if self.state.emotional_state == "greedy":
            # When greedy, push profit targets further (unrealistic)
            tp1_price = self._adjust_tp_for_greed(direction, tp1_price, 1.2)
            tp2_price = self._adjust_tp_for_greed(direction, tp2_price, 1.3)
            tp3_price = self._adjust_tp_for_greed(direction, tp3_price, 1.5)
            
            # When greedy, takes profits more gradually to "let winners run"
            take_profits = [
                {"price": tp1_price, "percentage": 0.3, "hit": False},
                {"price": tp2_price, "percentage": 0.3, "hit": False},
                {"price": tp3_price, "percentage": 0.4, "hit": False}
            ]
        elif self.state.emotional_state == "fearful":
            # When fearful, takes profits very quickly
            take_profits = [
                {"price": tp1_price, "percentage": 0.8, "hit": False},
                {"price": tp2_price, "percentage": 0.2, "hit": False}
            ]
        elif self.state.emotional_state == "excited":
            # When excited, uses a more balanced but still aggressive approach
            take_profits = [
                {"price": tp1_price, "percentage": 0.4, "hit": False},
                {"price": tp2_price, "percentage": 0.4, "hit": False},
                {"price": tp3_price, "percentage": 0.2, "hit": False}
            ]
        else:
            # Standard take-profit distribution
            take_profits = [
                {"price": tp1_price, "percentage": 0.5, "hit": False},
                {"price": tp2_price, "percentage": 0.3, "hit": False},
                {"price": tp3_price, "percentage": 0.2, "hit": False}
            ]
        
        return take_profits
    
    def process_trade_result(self, result: float, trade_duration: float) -> None:
        """
        Process the outcome of a trade and update the trader state.
        
        For aggressive traders, also update:
        - Trade duration stats
        - Signal performance metrics
        - Emotional state evolution
        """
        # Call the parent method to update basic stats
        super().process_trade_result(result, trade_duration)
        
        # Track trade duration
        self.trade_durations.append(trade_duration)
        
        # Update signal performance metrics
        if self.last_trade_signal:
            if result > 0:
                self.successful_signals[self.last_trade_signal]["wins"] += 1
            else:
                self.successful_signals[self.last_trade_signal]["losses"] += 1
        
        # Reset last trade signal
        self.last_trade_signal = None
    
    def print_status(self) -> None:
        """Print current trader status with additional aggressive trader metrics."""
        # Call parent to print base metrics
        super().print_status()
        
        # Calculate additional aggressive trader metrics
        avg_duration = sum(self.trade_durations) / max(1, len(self.trade_durations))
        
        # Calculate best and worst signals
        best_signal = max(self.successful_signals.items(), 
                          key=lambda x: x[1]["wins"] / max(1, (x[1]["wins"] + x[1]["losses"])), 
                          default=("none", {"wins": 0, "losses": 0}))
        
        worst_signal = min(self.successful_signals.items(),
                          key=lambda x: x[1]["wins"] / max(1, (x[1]["wins"] + x[1]["losses"])), 
                          default=("none", {"wins": 0, "losses": 0}))
        
        # Print aggressive trader specific info
        print(f"\n{YELLOW}Aggressive Strategy Metrics:{RESET}")
        print(f"Avg Hold Time: {avg_duration:.2f} hours")
        print(f"Current Leverage: {self._calculate_current_leverage()}x")
        print(f"Best Signal: {best_signal[0]} ({best_signal[1]['wins']}/{best_signal[1]['wins'] + best_signal[1]['losses']})")
        print(f"Worst Signal: {worst_signal[0]} ({worst_signal[1]['wins']}/{worst_signal[1]['wins'] + worst_signal[1]['losses']})")
        
    def _adjust_tp_for_greed(self, direction: str, tp_price: float, multiplier: float) -> float:
        """Adjust take-profit targets when trader is greedy (pushes them further)."""
        if direction == "LONG":
            # For longs, increase the TP price
            distance = tp_price - self._get_indicator_value("price")
            return tp_price + (distance * (multiplier - 1))
        else:  # SHORT
            # For shorts, decrease the TP price
            distance = self._get_indicator_value("price") - tp_price
            return tp_price - (distance * (multiplier - 1))
    
    def _calculate_volume_change(self) -> float:
        """Calculate recent volume change ratio from market data."""
        try:
            # Get recent volume data from Redis
            recent_volumes = self.redis_conn.lrange("recent_volume_data", -5, -1)
            if len(recent_volumes) < 2:
                return 1.0
                
            # Convert to floats
            volumes = [float(vol) for vol in recent_volumes]
            
            # Calculate average of previous volumes
            prev_avg = sum(volumes[:-1]) / len(volumes[:-1])
            current_vol = volumes[-1]
            
            if prev_avg > 0:
                return current_vol / prev_avg
            return 1.0
        except Exception:
            return 1.0
    
    def _get_indicator_value(self, indicator_name: str) -> Optional[float]:
        """Get technical indicator value from Redis or cache."""
        try:
            value = self.redis_conn.get(indicator_name)
            if value:
                return float(value)
            return None
        except Exception:
            return None
    
    def _calculate_current_leverage(self) -> int:
        """
        Calculate current leverage based on trader state.
        
        Aggressive traders adjust leverage dynamically based on:
        - Emotional state (greedy, fearful, etc.)
        - Recent performance (consecutive wins/losses)
        - Overall confidence
        """
        # Base leverage is 20x
        leverage = self.base_leverage
        
        # Adjust leverage based on emotional state and confidence
        if self.state.emotional_state == "greedy":
            # When greedy, maxes out leverage
            leverage = min(50, leverage * (1 + self.state.confidence * 0.5))
        elif self.state.emotional_state == "fearful":
            # When fearful, reduces leverage
            leverage = max(10, leverage * (1 - self.state.confidence * 0.5))
        elif self.state.emotional_state == "excited":
            # When excited, increases leverage moderately
            leverage = min(40, leverage * (1 + self.state.confidence * 0.3))
        else:
            # Normal adjustments based on confidence
            leverage += (self.state.confidence - 0.5) * 20
        
        # Additional adjustments based on performance
        if self.state.consecutive_wins >= 2:
            # Increase leverage on winning streak - chasing performance
            streak_multiplier = 1 + min(self.state.consecutive_wins * 0.08, 0.5)
            leverage *= streak_multiplier
        elif self.state.consecutive_losses >= 2:
            # Decrease leverage on losing streak - becoming cautious
            leverage *= (1 - min(self.state.consecutive_losses * 0.1, 0.5))
        
        # Ensure leverage stays within 10x-50x range
        return max(10, min(int(leverage), 50))
    
    def _calculate_stop_distance(self, direction: str) -> float:
        """Calculate appropriate stop distance based on market conditions and strategy."""
        # Default stop distance
        stop_distance = 0.01  # 1%
        
        # Get market volatility if available
        try:
            volatility = float(self.redis_conn.get("recent_volatility") or 0)
            if volatility > 0:
                # Scale stop distance with volatility
                stop_distance = max(0.005, min(0.02, volatility / 7500))
        except (TypeError, ValueError):
            pass
            
        # Adjust based on emotional state
        if self.state.emotional_state == "greedy":
            stop_distance *= 0.8  # Tighter stops when greedy
        elif self.state.emotional_state == "fearful":
            stop_distance *= 1.3  # Wider stops when fearful
            
        return stop_distance
    
    def _should_make_emotional_entry(self) -> bool:
        """
        Determine if trader should make an emotional entry based on state and impulsiveness.
        
        More impulsive traders and those in extreme emotional states are more likely
        to enter trades based on emotions rather than signals.
        """
        # Base probability depends on impulsiveness trait
        base_probability = self.impulsiveness * 0.3  # 0-30% base chance
        
        # Adjust based on emotional state
        if self.state.emotional_state == "greedy":
            base_probability += self.fomo_susceptibility * 0.2  # Add 0-20% for FOMO
        elif self.state.emotional_state == "fearful" and self.state.consecutive_losses >= 2:
            base_probability += 0.15  # Add 15% for revenge trading after losses
            
        # Check against random number
        return random.random() < base_probability