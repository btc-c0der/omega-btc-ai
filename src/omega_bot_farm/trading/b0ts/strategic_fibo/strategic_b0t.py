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
Strategic Trader Bot for Omega Bot Farm

This module implements a strategic trader with a disciplined, trend-following approach.
"""

import random
import os
from typing import Dict, List, Tuple, Optional, Any
import logging

from src.omega_bot_farm.trading.core_b0t.trader_base_b0t import TraderProfile
from src.omega_bot_farm.trading.b0ts.trading_analyser.trading_analyzer_b0t import TradingAnalyzerB0t
from src.omega_bot_farm.utils.redis_client import RedisClient
from src.omega_bot_farm.utils.cosmic_factor_service import CosmicFactorService, MoonPhase, SchumannFrequency, MarketLiquidity, GlobalSentiment

logger = logging.getLogger("strategic_b0t")

class StrategicTraderB0t(TraderProfile):
    """
    Strategic trader with patient, analytical, disciplined approach.
    
    This trader focuses on:
    - Medium to long-term trades
    - Strong risk management
    - Trend following with confirmation
    - Conservative position sizing
    """
    
    def __init__(self, initial_capital: float = 10000.0, name: str = "Strategic_B0t", 
                 redis_client: Optional[RedisClient] = None, 
                 cosmic_config_path: Optional[str] = None):
        """Initialize the strategic trader bot."""
        super().__init__(initial_capital, name, redis_client)
        
        # Initialize analyzer
        self.analyzer = TradingAnalyzerB0t()
        
        # Strategic trader specific attributes
        self.patience_score = 0.8  # High patience (0.0-1.0)
        self.avg_trade_duration = 16.0  # Hours
        self.position_sizing_factor = 0.02  # Conservative position sizing
        self.min_trend_confirmation = 0.65  # Require strong trend confirmation
        self.risk_reward_target = 3.0  # Seek 3:1 reward:risk ratio
        self.max_leverage = 3.0  # Conservative leverage
        
        # Initialize cosmic factor service
        if cosmic_config_path is None:
            # Try to get default config path
            default_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                "config", 
                "cosmic_factors.yaml"
            )
            if os.path.exists(default_path):
                cosmic_config_path = default_path
                
        self.cosmic_service = CosmicFactorService(config_path=cosmic_config_path)
        logger.info(f"Cosmic Factor Service initialized. Enabled: {self.cosmic_service.is_enabled()}")
        
        logger.info(f"Strategic Trader Bot '{name}' initialized with ${initial_capital:,.2f}")
    
    def _get_current_cosmic_conditions(self, market_context: Dict) -> Dict:
        """Extract cosmic conditions from market context."""
        # Extract conditions from market context if available
        # Or set some defaults based on current market state
        conditions = {
            "moon_phase": market_context.get("moon_phase", MoonPhase.FULL_MOON),
            "schumann_frequency": market_context.get("schumann_frequency", SchumannFrequency.BASELINE),
            "market_liquidity": market_context.get("market_liquidity", MarketLiquidity.NORMAL),
            "global_sentiment": market_context.get("global_sentiment", GlobalSentiment.NEUTRAL),
            "mercury_retrograde": market_context.get("mercury_retrograde", False),
            "trader_latitude": market_context.get("trader_latitude", 40.0),
            "trader_longitude": market_context.get("trader_longitude", -74.0),
            "day_of_week": market_context.get("day_of_week", 0),
            "hour_of_day": market_context.get("hour_of_day", 12),
        }
        return conditions
        
    def should_enter_trade(self, market_context: Dict) -> Tuple[bool, str, str, float]:
        """
        Determine if we should enter a trade based on market context.
        
        Returns tuple of (should_enter, direction, reason, leverage)
        """
        # Extract relevant market data
        price = market_context.get("price", 0.0)
        trend = market_context.get("trend", "sideways")
        regime = market_context.get("regime", "neutral")
        
        # Get price history for analysis
        price_history = market_context.get("price_history", [])
        if not price_history and price > 0:
            price_history = [price]  # Fallback
            
        # Strategic traders require more data and confirmation
        if len(price_history) < 10:
            return False, "none", "Insufficient historical data", 1.0
            
        # Analyze trend strength
        detected_trend = self.analyzer.analyze_trend(price_history)
        
        # Confirm trend with more sophisticated analysis
        trend_match = (trend == detected_trend)
        regime_supports_trend = False
        
        # Check if market regime supports the trend
        if (regime in ["bullish", "bullish_volatile"] and detected_trend == "uptrend") or \
           (regime in ["bearish", "bearish_volatile"] and detected_trend == "downtrend"):
            regime_supports_trend = True
            
        # Strategic traders need multiple confirmations
        confirmation_score = 0.0
        if trend_match:
            confirmation_score += 0.4
        if regime_supports_trend:
            confirmation_score += 0.3
            
        # Additional patterns recognition
        if len(price_history) >= 20:
            # Simple pattern: consecutive higher lows for uptrend
            if detected_trend == "uptrend":
                min_price_recent = min(price_history[-10:])
                min_price_older = min(price_history[-20:-10])
                if min_price_recent > min_price_older:
                    confirmation_score += 0.2
            # Simple pattern: consecutive lower highs for downtrend
            elif detected_trend == "downtrend":
                max_price_recent = max(price_history[-10:])
                max_price_older = max(price_history[-20:-10])
                if max_price_recent < max_price_older:
                    confirmation_score += 0.2
                    
        # Apply some randomness to account for other factors
        confirmation_score += random.uniform(-0.05, 0.05)
        
        # Create a decision object that can be modified by cosmic factors
        decision = {
            "entry_threshold": self.min_trend_confirmation,
            "confidence": confirmation_score
        }
        
        # Get cosmic conditions from market context
        cosmic_conditions = self._get_current_cosmic_conditions(market_context)
        
        # Calculate cosmic influences
        cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
        
        # Apply cosmic influences to decision
        modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
        
        # Get modified confirmation score and entry threshold
        confirmation_score = modified_decision.get("confidence", confirmation_score)
        entry_threshold = modified_decision.get("entry_threshold", self.min_trend_confirmation)
        
        # Strategic traders only enter with sufficient confirmation
        if confirmation_score < entry_threshold:
            return False, "none", "Insufficient trend confirmation", 1.0
            
        # Determine direction based on trend
        if detected_trend == "uptrend":
            direction = "long"
            reason = f"Confirmed uptrend with {confirmation_score:.2f} confidence"
        elif detected_trend == "downtrend":
            direction = "short"
            reason = f"Confirmed downtrend with {confirmation_score:.2f} confidence"
        else:
            return False, "none", "No clear trend direction", 1.0
            
        # Set leverage based on confirmation level
        leverage = 1.0 + (confirmation_score - 0.5) * 2
        leverage = min(leverage, self.max_leverage)
        
        # Apply emotional state filter - using the cosmic factor service
        if self.state.emotional_state == "fearful" and random.random() < 0.7:
            return False, "none", "Cautious due to fearful state", 1.0
            
        return True, direction, reason, leverage
        
    def determine_position_size(self, direction: str, entry_price: float) -> float:
        """Calculate conservative position size based on risk management rules."""
        # Base position size on capital and risk factor
        base_position_size = self.capital * self.position_sizing_factor
        
        # Adjust based on risk appetite
        risk_multiplier = 0.5 + self.state.risk_appetite
        position_size = base_position_size * risk_multiplier
        
        # Convert to BTC amount
        btc_amount = position_size / entry_price
        
        # Create a decision object for cosmic factor service
        decision = {
            "position_size": btc_amount,
            "entry_price": entry_price,
            "direction": direction
        }
        
        # Get current cosmic conditions
        # This would normally come from market context
        # but we'll use default values for simplicity
        cosmic_conditions = {
            "moon_phase": MoonPhase.FULL_MOON,
            "schumann_frequency": SchumannFrequency.BASELINE,
            "market_liquidity": MarketLiquidity.NORMAL,
            "global_sentiment": GlobalSentiment.NEUTRAL,
            "mercury_retrograde": False,
            "trader_latitude": 40.0,
            "trader_longitude": -74.0,
            "day_of_week": 0,
            "hour_of_day": 12,
        }
        
        # Calculate cosmic influences
        cosmic_influences = self.cosmic_service.calculate_cosmic_influences(cosmic_conditions)
        
        # Apply cosmic influences to position size
        modified_decision = self.cosmic_service.apply_cosmic_factors(decision, cosmic_influences)
        
        # Get modified position size
        btc_amount = modified_decision.get("position_size", btc_amount)
        
        # Apply emotional state adjustments - already handled by cosmic service
        # but we'll keep this for backward compatibility
        if self.state.emotional_state == "greedy":
            btc_amount *= 0.8  # Reduce position size when greedy
        elif self.state.emotional_state == "fearful":
            btc_amount *= 0.6  # Reduce position size when fearful
            
        # Log the decision
        self.logger.info(
            f"Position size: {btc_amount:.4f} BTC (${position_size:.2f}) " + 
            f"based on risk appetite {self.state.risk_appetite:.2f}"
        )
        
        return btc_amount
        
    def set_stop_loss(self, direction: str, entry_price: float) -> float:
        """Set strategic stop loss with sufficient room for market noise."""
        # Strategic traders use wider stops to avoid noise
        stop_percentage = 0.03  # 3% default stop
        
        # Adjust based on market volatility if available
        # in a real implementation this would use more sophisticated volatility analysis
        
        if direction == "long":
            stop_level = entry_price * (1 - stop_percentage)
        else:  # short
            stop_level = entry_price * (1 + stop_percentage)
            
        self.logger.info(f"Stop loss set at: ${stop_level:.2f}")
        return stop_level
        
    def set_take_profit(self, direction: str, entry_price: float, stop_loss: float) -> List[Dict]:
        """Set multiple take profit targets based on risk:reward ratio."""
        risk_amount = abs(entry_price - stop_loss)
        
        # Strategic traders use multiple targets
        targets = []
        
        # First target at 2:1 R:R with 40% of position
        first_target_distance = risk_amount * 2
        if direction == "long":
            price = entry_price + first_target_distance
        else:
            price = entry_price - first_target_distance
            
        targets.append({
            "price": price,
            "percentage": 0.4  # Exit 40% of position
        })
        
        # Second target at 3:1 R:R with 40% of position
        second_target_distance = risk_amount * 3
        if direction == "long":
            price = entry_price + second_target_distance
        else:
            price = entry_price - second_target_distance
            
        targets.append({
            "price": price,
            "percentage": 0.4  # Exit 40% of position
        })
        
        # Third target at 5:1 R:R with 20% of position
        third_target_distance = risk_amount * 5
        if direction == "long":
            price = entry_price + third_target_distance
        else:
            price = entry_price - third_target_distance
            
        targets.append({
            "price": price,
            "percentage": 0.2  # Exit remaining 20% of position
        })
        
        return targets 