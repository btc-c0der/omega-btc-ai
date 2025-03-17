#!/usr/bin/env python3

"""
Scalper Trader Profile for OmegaBTC AI

This module implements a high-frequency scalping trader profile that operates
on very short timeframes, using order book data and liquidity zones to make
quick entries and exits with the aim of profiting from small price movements.
"""

import random
import datetime
import numpy as np
from typing import Dict, List, Any, Tuple, Optional

from omega_ai.trading.trader_base import TraderProfile
from omega_ai.trading.trade_simulation import TradeSimulator

class ScalperTrader(TraderProfile):
    """
    Implements a scalping trading strategy focusing on very short timeframes.
    
    Characteristics:
    - Extremely short trade durations (seconds to minutes)
    - Tight stop losses and take profits
    - Reliance on order book data and liquidity zones
    - High trading frequency
    - Moderate to high leverage (10x-20x)
    """
    
    def __init__(self, initial_capital: float = 10000):
        """Initialize the scalper trader with specific attributes."""
        super().__init__(initial_capital)
        
        # Scalper-specific attributes
        self.focus_level = random.uniform(0.7, 0.95)  # High focus required
        self.stress_threshold = random.uniform(0.5, 0.8)  # Moderate to high stress tolerance
        self.stress_level = 0.0
        self.burnout_risk = 0.0
        self.consecutive_trades = 0
        self.trade_durations = []
        self.avg_holding_period = random.randint(30, 300)  # seconds
        
        # Trading parameters
        self.default_leverage = random.randint(10, 20)
        self.stop_loss_percent = random.uniform(0.1, 0.3)  # Very tight stops
        self.take_profit_percent = random.uniform(0.2, 0.5)  # Small targets
        self.max_trades_per_hour = random.randint(5, 20)
        self.trade_count_this_hour = 0
        self.last_hour_reset = datetime.datetime.now().hour
        
        # Technical indicators focus
        self.indicators = {
            "orderbook_imbalance": random.uniform(0.7, 0.9),  # High importance
            "liquidity_zones": random.uniform(0.7, 0.9),      # High importance
            "volume_profile": random.uniform(0.6, 0.8),
            "vwap": random.uniform(0.6, 0.8),
            "short_term_momentum": random.uniform(0.5, 0.7),
            "price_action": random.uniform(0.6, 0.8)
        }
        
        # Psychological factors
        self.patience = random.uniform(0.2, 0.4)  # Low patience (wants quick results)
        self.discipline = random.uniform(0.6, 0.9)  # High discipline required
        self.fomo_susceptibility = random.uniform(0.4, 0.7)  # Moderate FOMO
        
    def update_psychological_state(self, market_volatility: float, pnl: float,
                                  trade_duration: float) -> None:
        """Update psychological state based on market conditions and results."""
        # Reset trade count if hour has changed
        current_hour = datetime.datetime.now().hour
        if current_hour != self.last_hour_reset:
            self.trade_count_this_hour = 0
            self.last_hour_reset = current_hour
        
        # Increase stress based on volatility and consecutive trades
        self.stress_level += market_volatility * 0.2
        self.stress_level += self.consecutive_trades * 0.05
        
        # Reduce stress on successful trades, increase on losing trades
        if pnl > 0:
            self.stress_level -= 0.1
        else:
            self.stress_level += 0.15
            
        # Burnout increases with sustained stress
        if self.stress_level > self.stress_threshold:
            self.burnout_risk += 0.1
            
        # Cap values
        self.stress_level = max(0, min(1, self.stress_level))
        self.burnout_risk = max(0, min(1, self.burnout_risk))
        
        # Psychological impact on focus
        effective_focus = self.focus_level
        if self.burnout_risk > 0.7:
            effective_focus *= (1 - (self.burnout_risk - 0.7))
        
        # Track trade stats
        self.trade_count_this_hour += 1
        self.trade_durations.append(trade_duration)
        self.avg_holding_period = sum(self.trade_durations[-20:]) / min(len(self.trade_durations[-20:]), 20)
        
    def make_decision(self, current_price: float,
                     orderbook_data: Optional[Dict] = None,
                     market_volatility: float = 0.5) -> Dict[str, Any]:
        """
        Make a trading decision based on current market conditions.
        Specifically built for scalping strategy focusing on order book.
        
        Args:
            current_price: Current BTC price
            orderbook_data: Order book snapshot data
            market_volatility: Current market volatility level (0-1)
            
        Returns:
            Dictionary with trading decision
        """
        # Check if we've exceeded max trades per hour
        if self.trade_count_this_hour >= self.max_trades_per_hour:
            return {"action": "WAIT", "reason": "Max trades per hour reached"}
            
        # Check if burnout risk is too high
        if self.burnout_risk > 0.8:
            return {"action": "WAIT", "reason": "Trader burnout risk high, taking a break"}
            
        # Analyze order book for imbalances (simplified simulation)
        buy_pressure = random.uniform(0.3, 0.7)
        sell_pressure = random.uniform(0.3, 0.7)
        
        # Adjust based on burnout and stress
        effective_analysis = self.focus_level * (1 - (self.burnout_risk * 0.5))
        
        # Detect strong imbalances
        imbalance_threshold = 0.2 * effective_analysis
        
        if buy_pressure > sell_pressure + imbalance_threshold:
            # Long opportunity detected
            leverage = self.calculate_leverage(market_volatility)
            
            # Calculate entry/exit points
            stop_loss = current_price * (1 - self.stop_loss_percent / 100)
            
            # Higher volatility = higher potential reward
            tp_multiplier = 1.0 + (market_volatility * 0.5) 
            take_profit = current_price * (1 + (self.take_profit_percent * tp_multiplier) / 100)
            
            return {
                "action": "ENTER",
                "direction": "LONG",
                "reason": f"Order book buy imbalance detected ({buy_pressure:.2f} vs {sell_pressure:.2f})",
                "stop_loss": stop_loss,
                "take_profits": [{"price": take_profit, "percentage": 1.0}],
                "size": self.calculate_position_size(current_price, stop_loss),
                "leverage": leverage
            }
            
        elif sell_pressure > buy_pressure + imbalance_threshold:
            # Short opportunity detected
            leverage = self.calculate_leverage(market_volatility)
            
            # Calculate entry/exit points
            stop_loss = current_price * (1 + self.stop_loss_percent / 100)
            take_profit = current_price * (1 - (self.take_profit_percent * 1.5) / 100)
            
            return {
                "action": "ENTER",
                "direction": "SHORT",
                "reason": f"Order book sell imbalance detected ({sell_pressure:.2f} vs {buy_pressure:.2f})",
                "stop_loss": stop_loss,
                "take_profits": [{"price": take_profit, "percentage": 1.0}],
                "size": self.calculate_position_size(current_price, stop_loss),
                "leverage": leverage
            }
        
        # No clear signal
        return {"action": "WAIT", "reason": "No significant order book imbalance detected"}
            
    def calculate_leverage(self, volatility: float) -> int:
        """Calculate appropriate leverage based on market conditions and trader state."""
        # Reduce leverage when stressed or experiencing burnout
        base_leverage = self.default_leverage
        
        # Higher volatility = lower leverage
        volatility_adjustment = max(0, 1 - (volatility * 1.5))
        
        # Psychological state impacts risk taking
        psychological_adjustment = 1.0
        if self.stress_level > self.stress_threshold:
            psychological_adjustment *= 0.8
        if self.burnout_risk > 0.6:
            psychological_adjustment *= 0.7
            
        effective_leverage = base_leverage * volatility_adjustment * psychological_adjustment
        
        # Ensure it stays within reasonable bounds
        return max(1, min(20, round(effective_leverage)))
        
    def calculate_position_size(self, price: float, stop_loss: float) -> float:
        """Calculate position size based on risk parameters."""
        # Risk 1-2% of capital per trade for scalping
        risk_percentage = random.uniform(1.0, 2.0) / 100
        
        # Adjust risk based on psychological state
        if self.stress_level > self.stress_threshold:
            risk_percentage *= 0.8  # Reduce risk when stressed
        if self.burnout_risk > 0.7:
            risk_percentage *= 0.7  # Reduce risk when burning out
            
        risk_amount = self.capital * risk_percentage
        
        # Calculate price distance to stop
        price_distance = abs(price - stop_loss)
        if price_distance == 0:  # Avoid division by zero
            price_distance = price * 0.001
            
        # Position size in BTC
        position_size = risk_amount / price_distance
        
        return position_size

    # Rename this method to match other profiles
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if trader should enter a trade based on order book data."""
        current_price = market_context.get("price", 0)
        if current_price <= 0:
            return False, "", "", 0
            
        # Get market volatility - add safe conversion
        try:
            recent_volatility = market_context.get("recent_volatility", 0)
            from omega_ai.trading.trading_analyzer import safe_float_convert
            market_volatility = safe_float_convert(recent_volatility) / 1000.0
        except Exception as e:
            print(f"[WARNING] Could not process volatility: {e}")
            market_volatility = 0.5  # Default value
        
        # Get order book data if available
        orderbook_data = market_context.get("orderbook", None)
        
        # Call the original implementation
        decision = self.make_decision(current_price, orderbook_data, market_volatility)
        
        if decision["action"] == "ENTER":
            return (
                True, 
                decision["direction"], 
                decision["reason"], 
                decision["leverage"]
            )
        
        return False, "", decision.get("reason", ""), 0