#!/usr/bin/env python3

"""
AggressiveTrader Profile for OmegaBTC AI

This module simulates an aggressive trader who takes high-risk, high-reward trades
with quick entries and exits.
"""

import random
from typing import Dict, List, Tuple, Optional

from .trader_base import TraderProfile, RiskParameters

class AggressiveTrader(TraderProfile):
    """Aggressive trader that takes high-risk, high-reward trades."""
    
    def __init__(self, initial_capital: float = 10000.0):
        """Initialize the aggressive trader with high-risk approach."""
        super().__init__(initial_capital)
        
        # Set trader name
        self.name = "Aggressive Momentum Trader"
        
        # Aggressive trader specific attributes
        self.patience_score = random.uniform(0.3, 0.6)  # Lower patience
        self.analysis_depth = random.uniform(0.4, 0.7)  # Quicker analysis
        self.fomo_resistance = random.uniform(0.3, 0.6)  # Lower resistance to FOMO
        
        # Aggressive parameters
        self.momentum_threshold = 0.7  # How strong momentum must be to enter
        self.volume_threshold = 1.5  # Minimum volume increase to consider entry
        self.quick_exit_threshold = 0.02  # 2% quick exit target
    
    def _get_risk_parameters(self) -> RiskParameters:
        """Get risk parameters specific to aggressive trader profile."""
        return RiskParameters(
            max_risk_per_trade=0.05,  # 5% risk per trade
            base_leverage=5.0,        # High base leverage
            max_leverage=10.0,        # Very high max leverage
            min_risk_reward_ratio=random.uniform(1.2, 2.0),  # Lower R:R for quicker trades
            position_sizing_volatility_factor=1.2,  # Increase size in high volatility
            stop_loss_multiplier=0.8,  # Tighter stops for quick exits
            take_profit_multiplier=1.5  # Quicker take profits
        )
    
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if a trade should be entered based on market context."""
        current_price = market_context.get("price", 0)
        trend = market_context.get("trend", "neutral")
        momentum = market_context.get("momentum", 0)
        volume = market_context.get("volume", 0)
        
        # Check for strong momentum
        if momentum < self.momentum_threshold:
            return False, "Insufficient momentum", "NEUTRAL", self.risk_params.base_leverage
        
        # Check for volume confirmation
        if volume < self.volume_threshold:
            return False, "Insufficient volume", "NEUTRAL", self.risk_params.base_leverage
        
        # Calculate leverage based on market conditions
        leverage = self._calculate_current_leverage(market_context)
        
        # Determine trade direction and reason
        if trend == "uptrend" and momentum > self.momentum_threshold:
            return True, "Strong upward momentum", "LONG", leverage
        elif trend == "downtrend" and momentum < -self.momentum_threshold:
            return True, "Strong downward momentum", "SHORT", leverage
        
        return False, "No clear entry signal", "NEUTRAL", leverage
    
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on risk parameters and market conditions."""
        # Base position size on risk per trade
        risk_amount = self.capital * self.risk_params.max_risk_per_trade
        
        # Adjust for volatility
        volatility_factor = self.risk_params.position_sizing_volatility_factor
        if self.volatility > 0.02:  # High volatility
            volatility_factor *= 1.2  # Increase size in high volatility
        
        # Calculate position size
        position_size = risk_amount * volatility_factor
        
        # Ensure position size doesn't exceed capital
        return min(position_size, self.capital)
    
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Set stop loss level based on aggressive trader's risk management rules."""
        # Calculate base stop distance
        stop_distance = entry_price * 0.01  # 1% base stop
        
        # Adjust based on volatility
        stop_distance *= (1 + self.volatility)
        
        # Apply profile-specific multiplier
        stop_distance *= self.risk_params.stop_loss_multiplier
        
        if direction == "LONG":
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance
    
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set take profit levels based on aggressive trader's profit-taking strategy."""
        # Calculate risk distance
        risk_distance = abs(entry_price - stop_loss)
        
        # Calculate minimum reward based on risk:reward ratio
        min_reward = risk_distance * self.risk_params.min_risk_reward_ratio
        
        # Create multiple take profit levels
        take_profits = []
        
        # First target: Quick exit at 1.2x risk
        take_profits.append({
            "price": entry_price + (min_reward * 0.4) if direction == "LONG" else entry_price - (min_reward * 0.4),
            "percentage": 0.5  # 50% of position
        })
        
        # Second target: 1.5x risk
        take_profits.append({
            "price": entry_price + (min_reward * 0.8) if direction == "LONG" else entry_price - (min_reward * 0.8),
            "percentage": 0.3  # 30% of position
        })
        
        # Third target: 2x risk
        take_profits.append({
            "price": entry_price + (min_reward * 1.2) if direction == "LONG" else entry_price - (min_reward * 1.2),
            "percentage": 0.2  # 20% of position
        })
        
        return take_profits
    
    def _calculate_current_leverage(self, market_context: Optional[Dict] = None) -> float:
        """Calculate current leverage based on market conditions and profile."""
        leverage = self.risk_params.base_leverage
        
        # Adjust based on volatility
        if market_context and "recent_volatility" in market_context:
            volatility = market_context["recent_volatility"]
            if volatility > 0.02:  # High volatility
                leverage *= 1.2  # Increase leverage in high volatility
            elif volatility < 0.01:  # Low volatility
                leverage *= 0.8  # Decrease leverage in low volatility
        
        # Cap at max leverage
        return min(leverage, self.risk_params.max_leverage)