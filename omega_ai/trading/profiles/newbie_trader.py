#!/usr/bin/env python3

"""
NewbieTrader Profile for OmegaBTC AI

This module simulates a new trader who is learning the market,
taking conservative trades with strict risk management.
"""

import random
from typing import Dict, List, Tuple, Optional

from .trader_base import TraderProfile, RiskParameters

class NewbieTrader(TraderProfile):
    """Newbie trader that takes conservative trades with strict risk management."""
    
    def __init__(self, initial_capital: float = 10000.0):
        """Initialize the newbie trader with conservative approach."""
        super().__init__(initial_capital)
        
        # Set trader name
        self.name = "Learning Trader"
        
        # Newbie specific attributes
        self.patience_score = random.uniform(0.7, 0.95)  # High patience
        self.analysis_depth = random.uniform(0.3, 0.6)  # Basic analysis
        self.fomo_resistance = random.uniform(0.8, 0.95)  # High resistance to FOMO
        
        # Newbie parameters
        self.min_trend_strength = 0.7  # Require strong trend confirmation
        self.min_volume_threshold = 1.3  # Require higher volume confirmation
        self.max_daily_trades = 3  # Limit number of trades per day
    
    def _get_risk_parameters(self) -> RiskParameters:
        """Get risk parameters specific to newbie trader profile."""
        return RiskParameters(
            max_risk_per_trade=0.005,  # 0.5% risk per trade
            base_leverage=1.0,        # No leverage
            max_leverage=1.5,         # Very low max leverage
            min_risk_reward_ratio=random.uniform(2.0, 3.0),  # Higher R:R for safer trades
            position_sizing_volatility_factor=0.6,  # Conservative sizing
            stop_loss_multiplier=1.2,  # Wider stops for safety
            take_profit_multiplier=2.0  # Conservative take profits
        )
    
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """Determine if a trade should be entered based on market context."""
        current_price = market_context.get("price", 0)
        trend = market_context.get("trend", "neutral")
        trend_strength = market_context.get("trend_strength", 0)
        volume = market_context.get("volume", 0)
        
        # Check for strong trend confirmation
        if trend_strength < self.min_trend_strength:
            return False, "Trend not strong enough", "NEUTRAL", self.risk_params.base_leverage
        
        # Check for sufficient volume
        if volume < self.min_volume_threshold:
            return False, "Insufficient volume", "NEUTRAL", self.risk_params.base_leverage
        
        # Calculate leverage based on market conditions
        leverage = self._calculate_current_leverage(market_context)
        
        # Determine trade direction and reason
        if trend == "uptrend" and trend_strength > self.min_trend_strength:
            return True, "Strong uptrend with volume", "LONG", leverage
        elif trend == "downtrend" and trend_strength > self.min_trend_strength:
            return True, "Strong downtrend with volume", "SHORT", leverage
        
        return False, "No clear entry signal", "NEUTRAL", leverage
    
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate position size based on risk parameters and market conditions."""
        # Base position size on risk per trade
        risk_amount = self.capital * self.risk_params.max_risk_per_trade
        
        # Adjust for volatility
        volatility_factor = self.risk_params.position_sizing_volatility_factor
        if self.volatility > 0.01:  # High volatility
            volatility_factor *= 0.6  # Very conservative in high volatility
        
        # Calculate position size
        position_size = risk_amount * volatility_factor
        
        # Ensure position size doesn't exceed capital
        return min(position_size, self.capital)
    
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Set stop loss level based on newbie trader's risk management rules."""
        # Calculate base stop distance
        stop_distance = entry_price * 0.03  # 3% base stop
        
        # Adjust based on volatility
        stop_distance *= (1 + self.volatility)
        
        # Apply profile-specific multiplier
        stop_distance *= self.risk_params.stop_loss_multiplier
        
        if direction == "LONG":
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance
    
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set take profit levels based on newbie trader's profit-taking strategy."""
        # Calculate risk distance
        risk_distance = abs(entry_price - stop_loss)
        
        # Calculate minimum reward based on risk:reward ratio
        min_reward = risk_distance * self.risk_params.min_risk_reward_ratio
        
        # Create multiple take profit levels
        take_profits = []
        
        # First target: Conservative 2x risk
        take_profits.append({
            "price": entry_price + (min_reward * 0.5) if direction == "LONG" else entry_price - (min_reward * 0.5),
            "percentage": 0.5  # 50% of position
        })
        
        # Second target: 2.5x risk
        take_profits.append({
            "price": entry_price + (min_reward * 0.8) if direction == "LONG" else entry_price - (min_reward * 0.8),
            "percentage": 0.3  # 30% of position
        })
        
        # Third target: 3x risk
        take_profits.append({
            "price": entry_price + (min_reward * 1.0) if direction == "LONG" else entry_price - (min_reward * 1.0),
            "percentage": 0.2  # 20% of position
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
                leverage *= 1.1  # Slight increase in low volatility
        
        # Cap at max leverage
        return min(leverage, self.risk_params.max_leverage)