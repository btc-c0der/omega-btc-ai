#!/usr/bin/env python3

"""
ScalperTrader Profile for OmegaBTC AI

This module simulates a scalper trader who takes small, quick profits
with high frequency trades and tight risk management.
"""

import random
from typing import Dict, List, Tuple, Optional

from .trader_base import TraderProfile, RiskParameters

class ScalperTrader(TraderProfile):
    """Scalper trader that takes small, quick profits with high frequency."""
    
    def __init__(self, initial_capital: float = 10000.0):
        """Initialize the scalper trader with tight risk management."""
        super().__init__(initial_capital)
        
        # Set trader name
        self.name = "Quick Profit Scalper"
        
        # Scalper specific attributes
        self.patience_score = random.uniform(0.4, 0.7)  # Moderate patience
        self.analysis_depth = random.uniform(0.5, 0.8)  # Quick analysis
        self.fomo_resistance = random.uniform(0.5, 0.8)  # Moderate resistance to FOMO
        
        # Scalper parameters
        self.min_profit_threshold = 0.001  # 0.1% minimum profit target
        self.max_loss_threshold = 0.002   # 0.2% maximum loss
        self.volume_threshold = 1.2       # Minimum volume increase to consider entry
    
    def _get_risk_parameters(self) -> RiskParameters:
        """Get risk parameters specific to scalper trader profile."""
        return RiskParameters(
            max_risk_per_trade=0.01,  # 1% risk per trade
            base_leverage=2.0,        # Low base leverage
            max_leverage=3.0,         # Low max leverage
            min_risk_reward_ratio=random.uniform(1.5, 2.0),  # Higher R:R for quick trades
            position_sizing_volatility_factor=0.8,  # Reduce size in high volatility
            stop_loss_multiplier=0.5,  # Very tight stops
            take_profit_multiplier=1.0  # Quick take profits
        )
    
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if a trade should be entered based on market context."""
        current_price = market_context.get("price", 0)
        trend = market_context.get("trend", "neutral")
        volume = market_context.get("volume", 0)
        spread = market_context.get("spread", 0)
        
        # Check for sufficient volume
        if volume < self.volume_threshold:
            return False, "Insufficient volume", "NEUTRAL", self.risk_params.base_leverage
        
        # Check if spread is too wide
        if spread > self.min_profit_threshold * 2:
            return False, "Spread too wide", "NEUTRAL", self.risk_params.base_leverage
        
        # Calculate leverage based on market conditions
        leverage = self._calculate_current_leverage(market_context)
        
        # Determine trade direction and reason
        if trend == "uptrend" and volume > self.volume_threshold:
            return True, "Strong volume in uptrend", "LONG", leverage
        elif trend == "downtrend" and volume > self.volume_threshold:
            return True, "Strong volume in downtrend", "SHORT", leverage
        
        return False, "No clear entry signal", "NEUTRAL", leverage
    
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on risk parameters and market conditions."""
        # Base position size on risk per trade
        risk_amount = self.capital * self.risk_params.max_risk_per_trade
        
        # Adjust for volatility
        volatility_factor = self.risk_params.position_sizing_volatility_factor
        if self.volatility > 0.01:  # High volatility
            volatility_factor *= 0.8  # Reduce size in high volatility
        
        # Calculate position size
        position_size = risk_amount * volatility_factor
        
        # Ensure position size doesn't exceed capital
        return min(position_size, self.capital)
    
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Set stop loss level based on scalper trader's risk management rules."""
        # Calculate base stop distance
        stop_distance = entry_price * 0.002  # 0.2% base stop
        
        # Adjust based on volatility
        stop_distance *= (1 + self.volatility)
        
        # Apply profile-specific multiplier
        stop_distance *= self.risk_params.stop_loss_multiplier
        
        if direction == "LONG":
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance
    
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set take profit levels based on scalper trader's profit-taking strategy."""
        # Calculate risk distance
        risk_distance = abs(entry_price - stop_loss)
        
        # Calculate minimum reward based on risk:reward ratio
        min_reward = risk_distance * self.risk_params.min_risk_reward_ratio
        
        # Create multiple take profit levels
        take_profits = []
        
        # First target: Quick exit at 1.5x risk
        take_profits.append({
            "price": entry_price + (min_reward * 0.6) if direction == "LONG" else entry_price - (min_reward * 0.6),
            "percentage": 0.6  # 60% of position
        })
        
        # Second target: 2x risk
        take_profits.append({
            "price": entry_price + (min_reward * 1.0) if direction == "LONG" else entry_price - (min_reward * 1.0),
            "percentage": 0.4  # 40% of position
        })
        
        return take_profits
    
    def _calculate_current_leverage(self, market_context: Optional[Dict] = None) -> float:
        """Calculate current leverage based on market conditions and profile."""
        leverage = self.risk_params.base_leverage
        
        # Adjust based on volatility
        if market_context and "recent_volatility" in market_context:
            volatility = market_context["recent_volatility"]
            if volatility > 0.01:  # High volatility
                leverage *= 0.8  # Decrease leverage in high volatility
            elif volatility < 0.005:  # Low volatility
                leverage *= 1.2  # Increase leverage in low volatility
        
        # Cap at max leverage
        return min(leverage, self.risk_params.max_leverage)