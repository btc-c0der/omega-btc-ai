#!/usr/bin/env python3
"""
OMEGA BTC AI - Persona-Based Entry Strategy
===========================================

This module provides entry recommendations for positions based on different trader personas.
The personas analyze market conditions and suggest entries with confidence levels.

Author: OMEGA BTC AI Team
Version: 1.0.0
"""

import os
import sys
import time
import json
import logging
import asyncio
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from dotenv import load_dotenv
import argparse

# CCXT for BitGet API integration
try:
    import ccxt
    HAVE_CCXT = True
except ImportError:
    HAVE_CCXT = False
    print("⚠️ ccxt module not found. Real market data functionality will be limited.")
    print("Install it with: pip install ccxt")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('persona_entry_strategy')

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    RESET = '\033[0m'

@dataclass
class PersonaEntryRecommendation:
    """Entry recommendation from a specific trader persona."""
    persona_name: str
    confidence: float  # 0.0 to 1.0
    side: str  # "long" or "short"
    target_price: float
    reasons: List[str]
    risk_level: str  # "conservative", "moderate", "aggressive"
    time_horizon: str  # "immediate", "short-term", "long-term"
    explanation: str
    trap_awareness: float  # 0.0 to 1.0
    position_size: float  # Recommended position size as percentage of capital
    stop_loss: float  # Recommended stop loss price
    take_profit: float  # Recommended take profit price
    color_code: str = Colors.YELLOW
    action: str = "ENTER"  # "ENTER" or "WAIT"

    def __post_init__(self):
        # Set color based on confidence
        if self.confidence >= 0.8:
            self.color_code = Colors.GREEN if self.action == "ENTER" else Colors.BLUE
        elif self.confidence >= 0.5:
            self.color_code = Colors.YELLOW if self.action == "ENTER" else Colors.CYAN
        else:
            self.color_code = Colors.RED if self.action == "ENTER" else Colors.PURPLE

@dataclass
class PersonaBasedEntryStrategy:
    """
    Container for entry strategy recommendations from multiple personas.
    """
    market_symbol: str
    current_price: float
    recommendations: List[PersonaEntryRecommendation] = field(default_factory=list)
    summary: str = ""
    
    def add_recommendation(self, recommendation: PersonaEntryRecommendation):
        """Add a recommendation to the strategy."""
        self.recommendations.append(recommendation)
    
    def generate_summary(self):
        """Generate a summary of the recommendations."""
        # Count how many personas recommend entering vs waiting
        enter_count = len([r for r in self.recommendations if r.action == "ENTER"])
        total_count = len(self.recommendations)
        
        # If enough personas recommend entering
        if enter_count > 0:
            # Determine side with highest support
            long_count = len([r for r in self.recommendations if r.action == "ENTER" and r.side == "long"])
            short_count = len([r for r in self.recommendations if r.action == "ENTER" and r.side == "short"])
            
            if long_count > short_count:
                final_side = "long"
            elif short_count > long_count:
                final_side = "short"
            else:
                # If tied, use average confidence for each side
                long_confidence = sum([r.confidence for r in self.recommendations if r.action == "ENTER" and r.side == "long"]) / max(1, long_count)
                short_confidence = sum([r.confidence for r in self.recommendations if r.action == "ENTER" and r.side == "short"]) / max(1, short_count)
                
                final_side = "long" if long_confidence >= short_confidence else "short"
            
            # Find highest confidence entry recommendation
            highest_conf_rec = max([r for r in self.recommendations if r.action == "ENTER"], key=lambda x: x.confidence)
            
            # Set summary
            self.summary = f"ENTER {final_side.upper()}: {highest_conf_rec.persona_name} recommends entry"
            
        else:
            self.summary = f"NO ENTRY SIGNAL: {total_count} personas recommend waiting"
        
        return self.summary

class PersonaEntryManager:
    """
    Manager for persona-based entry recommendations.
    
    This class manages multiple trader personas and generates entry recommendations
    based on their individual analyses of market conditions.
    """
    
    def __init__(self, min_confidence: float = 0.5, use_color: bool = True, continuous_mode: bool = False):
        """
        Initialize PersonaEntryManager.
        
        Args:
            min_confidence: Minimum confidence level for recommendations (0.0-1.0)
            use_color: Whether to use colored terminal output
            continuous_mode: Whether running in continuous monitoring mode
        """
        self.min_confidence = min_confidence
        self.use_color = use_color
        self.continuous_mode = continuous_mode
        self.min_personas_for_entry = 2  # Minimum number of personas needed to recommend entry
        
        # List of available trader personas
        self.trader_personas = [
            "strategic",    # Technical/fundamental analysis, disciplined
            "aggressive",   # Takes more risk, momentum-based
            "newbie",       # Inexperienced, trend-following
            "contrarian",   # Goes against the crowd
            "patient",      # Waits for perfect setups
            "cosmic"        # Uses time cycles and cosmic patterns
        ]
        
        # Store previous recommendations for change detection
        self.previous_recommendations = {}
        
        # Last fetch time
        self.last_fetch_time = None
        
        print(f"Initialized PersonaEntryManager with {len(self.trader_personas)} trader personas")
    
    def colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.use_color:
            return f"{color}{text}{Colors.END}"
        return text

    def analyze_market(self, market_data: Dict[str, Any]) -> None:
        """
        Analyze a single market and print recommendations from all personas.
        
        Args:
            market_data: Dictionary containing market data for a single symbol
        """
        symbol = market_data["symbol"]
        current_price = market_data["current_price"]
        
        print(f"\n{self.colorize(Colors.CYAN, f'Analyzing {symbol} at {current_price:.2f} USDT')}")
        
        # Get recommendations from all personas
        entry_strategy = self.generate_entry_recommendations(market_data)
        
        # Print recommendations with market details
        print(self.format_recommendations_display(entry_strategy.recommendations, symbol, current_price))
    
    def generate_entry_recommendations(self, market_data: Dict[str, Any]) -> PersonaBasedEntryStrategy:
        """
        Generate entry recommendations based on different trader personas.
        
        Args:
            market_data: Market data dictionary with price, volume, etc.
            
        Returns:
            PersonaBasedEntryStrategy object with recommendations
        """
        current_price = market_data.get("current_price", 0)
        symbol = market_data.get("symbol", "UNKNOWN")
        
        # Generate recommendations for each persona
        recommendations = []
        
        # Strategic trader (disciplined, technical)
        strategic_rec = self._get_strategic_entry(market_data, current_price)
        if strategic_rec:
            recommendations.append(strategic_rec)
            
        # Aggressive trader (volatility-focused, momentum-based)
        aggressive_rec = self._get_aggressive_entry(market_data, current_price)
        if aggressive_rec:
            recommendations.append(aggressive_rec)
            
        # Newbie trader (follows trends, less sophisticated)
        newbie_rec = self._get_newbie_entry(market_data, current_price)
        if newbie_rec:
            recommendations.append(newbie_rec)
            
        # Contrarian trader (fades extremes)
        contrarian_rec = self._get_contrarian_entry(market_data, current_price)
        if contrarian_rec:
            recommendations.append(contrarian_rec)
            
        # Patient trader (waits for perfect setups)
        patient_rec = self._get_patient_entry(market_data, current_price)
        if patient_rec:
            recommendations.append(patient_rec)
            
        # Cosmic trader (uses time-based and astrology factors)
        cosmic_rec = self._get_cosmic_entry(market_data, current_price)
        if cosmic_rec:
            recommendations.append(cosmic_rec)
        
        # Determine overall entry signal
        # Count how many personas recommend entering vs waiting
        enter_count = len([r for r in recommendations if r.action == "ENTER"])
        total_count = len(recommendations)
        
        # Create strategy object
        strategy = PersonaBasedEntryStrategy(
            market_symbol=symbol,
            current_price=current_price,
            recommendations=recommendations
        )
        
        # Check if enough personas recommend entering
        if enter_count >= self.min_personas_for_entry:
            # Calculate average confidence for entry
            avg_confidence = sum([r.confidence for r in recommendations if r.action == "ENTER"]) / max(1, enter_count)
            
            # Determine side with highest support among entering personas
            long_count = len([r for r in recommendations if r.action == "ENTER" and r.side == "long"])
            short_count = len([r for r in recommendations if r.action == "ENTER" and r.side == "short"])
            
            if long_count > short_count:
                final_side = "long"
            elif short_count > long_count:
                final_side = "short"
            else:
                # If tied, use average confidence for each side
                long_confidence = sum([r.confidence for r in recommendations if r.action == "ENTER" and r.side == "long"]) / max(1, long_count)
                short_confidence = sum([r.confidence for r in recommendations if r.action == "ENTER" and r.side == "short"]) / max(1, short_count)
                
                final_side = "long" if long_confidence >= short_confidence else "short"
            
            # Set signal summary
            strategy.summary = f"ENTER {final_side.upper()}: {enter_count} out of {total_count} personas recommend entry with average confidence {avg_confidence:.2f}"
        else:
            # No entry signal
            strategy.summary = f"NO ENTRY SIGNAL: {enter_count} personas recommend entry, {total_count - enter_count} recommend waiting"
        
        # Return entry strategy with all recommendations
        return strategy
    
    def _get_persona_recommendation(
        self,
        persona_name: str,
        market_data: Dict[str, Any],
        current_price: float
    ) -> Optional[PersonaEntryRecommendation]:
        """
        Get entry recommendation from a specific trader persona.
        
        Args:
            persona_name: Name of the trader persona
            market_data: Market data
            current_price: Current market price
            
        Returns:
            PersonaEntryRecommendation
        """
        # Each persona has different entry criteria
        if persona_name == "strategic":
            return self._get_strategic_entry(market_data, current_price)
        elif persona_name == "aggressive":
            return self._get_aggressive_entry(market_data, current_price)
        elif persona_name == "newbie":
            return self._get_newbie_entry(market_data, current_price)
        elif persona_name == "scalper":
            return self._get_scalper_entry(market_data, current_price)
        elif persona_name == "cosmic":
            return self._get_cosmic_entry(market_data, current_price)
        elif persona_name == "patient":
            return self._get_patient_entry(market_data, current_price)
        
        return None
        
    def _get_strategic_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Strategic entry recommendation logic."""
        symbol = market_data["symbol"]
        
        # Extract key market data for analysis
        recent_high = market_data.get("recent_high", current_price * 1.05)
        recent_low = market_data.get("recent_low", current_price * 0.95)
        change_24h = market_data.get("change_24h", 0)
        low_24h = market_data.get("low_24h", 0)
        high_24h = market_data.get("high_24h", 0)
        
        # Calculate Fibonacci retracement levels
        fib_levels = {
            "0.236": recent_low + (recent_high - recent_low) * 0.236,
            "0.382": recent_low + (recent_high - recent_low) * 0.382,
            "0.5": recent_low + (recent_high - recent_low) * 0.5,
            "0.618": recent_low + (recent_high - recent_low) * 0.618,
            "0.786": recent_low + (recent_high - recent_low) * 0.786
        }
        
        # Define reasons list to store entry signals
        reasons = []
        confidence = 0.0
        side = "long"  # Default side
        target_price = current_price
        
        # Check for price at key Fibonacci retracement level
        near_fib_level = False
        nearest_fib = ""
        nearest_fib_dist_pct = float('inf')
        
        for level_name, level_price in fib_levels.items():
            dist_pct = abs(current_price - level_price) / current_price * 100
            if dist_pct < nearest_fib_dist_pct:
                nearest_fib_dist_pct = dist_pct
                nearest_fib = level_name
            
            # Consider price near a Fibonacci level if within 0.5%
            if dist_pct < 0.5:
                near_fib_level = True
                reasons.append(f"Price near {level_name} Fibonacci retracement level")
                confidence += 0.2
        
        # Market trend analysis
        if change_24h > 2.0:
            reasons.append(f"Bullish trend: {change_24h:.2f}% increase in 24h")
            side = "long"
            confidence += 0.15
        elif change_24h < -2.0:
            reasons.append(f"Bearish trend: {change_24h:.2f}% decrease in 24h")
            side = "short"
            confidence += 0.15
        
        # Check if price is near support or resistance
        if current_price < low_24h * 1.01:  # Within 1% of 24h low
            reasons.append(f"Price near 24h support level: {low_24h:.2f}")
            side = "long"  # Prefer long at support
            confidence += 0.2
            target_price = current_price  # Enter at current price
        elif current_price > high_24h * 0.99:  # Within 1% of 24h high
            reasons.append(f"Price near 24h resistance level: {high_24h:.2f}")
            side = "short"  # Prefer short at resistance
            confidence += 0.2
            target_price = current_price  # Enter at current price
        
        # Strategic trader values confluence of multiple signals
        if len(reasons) >= 2:
            confidence += 0.1  # Bonus for multiple confirmations
        
        # Set risk management parameters
        stop_loss = 0.0
        take_profit = 0.0
        if side == "long":
            stop_loss = current_price * 0.985  # 1.5% stop loss for long
            take_profit = current_price * 1.03  # 3% take profit for long
        else:
            stop_loss = current_price * 1.015  # 1.5% stop loss for short
            take_profit = current_price * 0.97  # 3% take profit for short
        
        # Additional check for confluence with technical levels
        if near_fib_level and (
            (side == "long" and current_price < low_24h * 1.05) or
            (side == "short" and current_price > high_24h * 0.95)
        ):
            confidence += 0.15
            reasons.append(f"Confluence of Fibonacci {nearest_fib} level and price near support/resistance")
        
        # Adjust confidence based on position vs. trend
        if side == "long" and change_24h < 0:
            confidence *= 0.8  # Reduce confidence for counter-trend trade
            reasons.append("Counter-trend trade with reduced confidence")
        elif side == "short" and change_24h > 0:
            confidence *= 0.8  # Reduce confidence for counter-trend trade
            reasons.append("Counter-trend trade with reduced confidence")
        
        # Determine final action based on confidence
        action = "WAIT"
        if confidence >= self.min_confidence:
            action = "ENTER"
        
        # Generate explanation
        if len(reasons) == 0:
            reasons.append("No compelling strategic entry signal")
            explanation = "Strategic analysis shows no clear entry opportunity at this time."
        else:
            explanation = f"Strategic entry signal with {confidence:.2f} confidence based on " + \
                          f"technical analysis and risk management principles."
        
        # Create and return recommendation object
        return PersonaEntryRecommendation(
            persona_name="Strategic Trader",
            confidence=confidence,
            side=side,
            target_price=target_price,
            reasons=reasons,
            risk_level="moderate",
            time_horizon="long-term",
            explanation=explanation,
            trap_awareness=0.8,  # Strategic traders have high trap awareness
            position_size=5.0,  # Conservative position size as percentage of capital
            stop_loss=stop_loss,
            take_profit=take_profit,
            action=action
        )
    
    def _get_aggressive_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Aggressive entry recommendation logic."""
        symbol = market_data["symbol"]
        
        # Extract key market data for analysis
        recent_high = market_data.get("recent_high", current_price * 1.05)
        recent_low = market_data.get("recent_low", current_price * 0.95)
        change_24h = market_data.get("change_24h", 0)
        volume = market_data.get("volume", 0)
        avg_volume = market_data.get("avg_volume", 1) or 1  # Prevent division by zero
        
        # Define reasons list to store entry signals
        reasons = []
        confidence = 0.0
        side = "long"  # Default side
        target_price = current_price
        
        # Volume-based entry signals (aggressive traders love high volume opportunities)
        volume_ratio = volume / avg_volume if avg_volume > 0 else 1.0
        if volume_ratio > 1.5:
            reasons.append(f"High volume ({volume_ratio:.2f}x average)")
            confidence += 0.15
        
        # Momentum-based entry signals
        if change_24h > 1.0:  # Aggressive traders enter on smaller moves
            reasons.append(f"Upward momentum: {change_24h:.2f}% increase in 24h")
            side = "long"
            confidence += 0.2
        elif change_24h < -1.0:
            reasons.append(f"Downward momentum: {change_24h:.2f}% decrease in 24h")
            side = "short"
            confidence += 0.2
        
        # Volatility-based entry signals (aggressive traders thrive on volatility)
        price_range_pct = (recent_high - recent_low) / recent_low * 100
        if price_range_pct > 3.0:  # More than 3% range in recent period
            reasons.append(f"High volatility ({price_range_pct:.2f}% range)")
            confidence += 0.2
            
            # Determine side based on current price position in range
            range_position = (current_price - recent_low) / (recent_high - recent_low)
            if range_position < 0.3:  # Bottom 30% of range
                side = "long"
                reasons.append("Price near bottom of recent range")
                confidence += 0.1
            elif range_position > 0.7:  # Top 30% of range
                side = "short"
                reasons.append("Price near top of recent range")
                confidence += 0.1
        
        # Aggressive traders take more risk with cosmic influences
        cosmic_confidence = market_data.get("cosmic_confidence", 0)
        cosmic_adjustment = market_data.get("cosmic_risk_adjustment", 0)
        if cosmic_confidence + cosmic_adjustment > 0:
            reasons.append("Positive cosmic alignment")
            confidence += 0.15
        
        # Moon phase consideration
        moon_phase = market_data.get("moon_phase", "unknown")
        if moon_phase in ["new", "full"]:
            reasons.append(f"{moon_phase.capitalize()} moon volatility opportunity")
            confidence += 0.1
        
        # Set aggressive risk management parameters
        stop_loss = 0.0
        take_profit = 0.0
        if side == "long":
            stop_loss = current_price * 0.97  # 3% stop loss for long
            take_profit = current_price * 1.06  # 6% take profit for long
        else:
            stop_loss = current_price * 1.03  # 3% stop loss for short
            take_profit = current_price * 0.94  # 6% take profit for short
        
        # Determine final action based on confidence
        action = "WAIT"
        if confidence >= self.min_confidence:
            action = "ENTER"
        
        # Generate explanation
        if len(reasons) == 0:
            reasons.append("No compelling aggressive entry signal")
            explanation = "Aggressive analysis shows no clear entry opportunity at this time."
        else:
            explanation = f"Aggressive entry signal with {confidence:.2f} confidence based on " + \
                          f"momentum, volatility, and market dynamics."
        
        # Create and return recommendation object
        return PersonaEntryRecommendation(
            persona_name="Aggressive Trader",
            confidence=confidence,
            side=side,
            target_price=target_price,
            reasons=reasons,
            risk_level="high",
            time_horizon="short-term",
            explanation=explanation,
            trap_awareness=0.4,  # Aggressive traders have lower trap awareness
            position_size=10.0,  # Larger position size as percentage of capital
            stop_loss=stop_loss,
            take_profit=take_profit,
            action=action
        )
    
    def _get_newbie_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Newbie entry recommendation logic."""
        symbol = market_data["symbol"]
        
        # Extract key market data for analysis
        change_24h = market_data.get("change_24h", 0)
        high_24h = market_data.get("high_24h", 0)
        low_24h = market_data.get("low_24h", 0)
        
        # Define reasons list to store entry signals
        reasons = []
        confidence = 0.0
        side = "long"  # Default side for newbies
        target_price = current_price
        
        # Newbie traders tend to follow strong market movements
        if change_24h > 5.0:  # Significant upward movement
            reasons.append(f"Strong uptrend: {change_24h:.2f}% increase in 24h")
            side = "long"
            confidence += 0.3
            reasons.append("Following the clear upward trend")
        elif change_24h < -5.0:  # Significant downward movement
            reasons.append(f"Strong downtrend: {change_24h:.2f}% decrease in 24h")
            side = "short"
            confidence += 0.25  # Slightly less confident with shorting
            reasons.append("Following the clear downward trend")
        
        # Newbies tend to enter after a large move has already happened
        if current_price > 0.95 * high_24h and change_24h > 2.0:
            reasons.append("Price near 24h high with positive momentum")
            side = "long"
            confidence += 0.2
        elif current_price < 1.05 * low_24h and change_24h < -2.0:
            reasons.append("Price near 24h low with negative momentum")
            side = "short"
            confidence += 0.2
        
        # Newbies are often influenced by "round number" price levels
        price_str = str(int(current_price))
        if price_str.endswith('000'):  # e.g., 50000
            reasons.append(f"Psychologically significant price level: {price_str}")
            confidence += 0.2
        elif price_str.endswith('500'):  # e.g., 50500
            reasons.append(f"Mid-point price level: {price_str}")
            confidence += 0.1
        
        # Newbies are heavily influenced by cosmic factors
        cosmic_confidence = market_data.get("cosmic_confidence", 0)
        if cosmic_confidence > 0:
            reasons.append("Positive cosmic alignment")
            confidence += 0.25  # Newbies give more weight to cosmic factors
        
        # Newbies prefer long positions (optimistic bias)
        if side == "short" and len(reasons) < 2:
            side = "long"
            reasons.append("Default preference for long positions")
            confidence = max(0.05, confidence - 0.1)  # Reduce confidence when defaulting to long
        
        # Set beginner-level risk management parameters
        stop_loss = 0.0
        take_profit = 0.0
        if side == "long":
            stop_loss = current_price * 0.95  # 5% stop loss for long
            take_profit = current_price * 1.1  # 10% take profit for long
        else:
            stop_loss = current_price * 1.05  # 5% stop loss for short
            take_profit = current_price * 0.9  # 10% take profit for short
        
        # Determine final action based on confidence
        action = "WAIT"
        if confidence >= self.min_confidence:
            action = "ENTER"
        
        # Generate explanation
        if len(reasons) == 0:
            reasons.append("No clear entry signal for new traders")
            explanation = "Market conditions are complex - better to wait for clearer signals."
        else:
            explanation = f"Newbie-friendly entry signal with {confidence:.2f} confidence based on " + \
                          f"trend following and basic market analysis."
        
        # Create and return recommendation object
        return PersonaEntryRecommendation(
            persona_name="Newbie Trader",
            confidence=confidence,
            side=side,
            target_price=target_price,
            reasons=reasons,
            risk_level="moderate",
            time_horizon="medium-term",
            explanation=explanation,
            trap_awareness=0.2,  # Newbies have low trap awareness
            position_size=5.0,  # Moderate position size as percentage of capital 
            stop_loss=stop_loss,
            take_profit=take_profit,
            action=action
        )
    
    def _get_scalper_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Implementation will be expanded in future versions"""
        # Placeholder for Scalper Trader entry logic
        return PersonaEntryRecommendation(
            persona_name="Scalper Trader",
            confidence=0.0,
            side="long",
            target_price=current_price,
            reasons=["Placeholder for Scalper Trader entry logic"],
            risk_level="moderate",
            time_horizon="immediate",
            explanation="Scalper entry logic to be implemented",
            trap_awareness=0.7,
            position_size=1.0,
            stop_loss=current_price * 0.995,  # 0.5% below entry
            take_profit=current_price * 1.01,  # 1% above entry
            action="WAIT"
        )
    
    def _get_cosmic_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Cosmic entry recommendation logic based on time and celestial patterns."""
        symbol = market_data["symbol"]
        
        # Extract key cosmic data
        cosmic_confidence = market_data.get("cosmic_confidence", 0)
        cosmic_risk_adjustment = market_data.get("cosmic_risk_adjustment", 0)
        moon_phase = market_data.get("moon_phase", "unknown")
        day_of_week = market_data.get("day_of_week", 0)  # 0 = Monday, 6 = Sunday
        hour_of_day = market_data.get("hour_of_day", 0)
        
        # Extract market data for confluence
        change_24h = market_data.get("change_24h", 0)
        
        # Define reasons list to store entry signals
        reasons = []
        confidence = 0.0  # Base confidence
        side = "long"  # Default side
        target_price = current_price
        
        # Moon phase analysis
        if moon_phase == "new":
            reasons.append("New moon phase - beginning of cycle")
            confidence += 0.3
            side = "long"  # New moon favors long positions
        elif moon_phase == "full":
            reasons.append("Full moon phase - peak of cycle")
            confidence += 0.3
            side = "short"  # Full moon favors short positions
        elif moon_phase == "waxing":
            reasons.append("Waxing moon - increasing energy")
            confidence += 0.2
            side = "long"  # Waxing moon favors long positions
        elif moon_phase == "waning":
            reasons.append("Waning moon - decreasing energy")
            confidence += 0.2
            side = "short"  # Waning moon favors short positions
        else:
            reasons.append(f"Moon phase: {moon_phase}")
            
        # Day of week analysis
        if day_of_week == 1:  # Tuesday - Mars day
            reasons.append("Tuesday (Mars day) - favorable for aggressive action")
            confidence += 0.15
            side = "long"  # Mars energy favors bold action
        elif day_of_week == 3:  # Thursday - Jupiter day
            reasons.append("Thursday (Jupiter day) - favorable for expansion")
            confidence += 0.15
            side = "long"  # Jupiter energy favors growth
        elif day_of_week == 5:  # Saturday - Saturn day
            reasons.append("Saturday (Saturn day) - favorable for caution")
            confidence += 0.15
            side = "short"  # Saturn energy favors contraction
        
        # Hour of day analysis
        if 8 <= hour_of_day <= 11:
            reasons.append(f"Morning hours ({hour_of_day}:00) - rising energy")
            confidence += 0.1
            side = "long"  # Morning favors upward movement
        elif 16 <= hour_of_day <= 19:
            reasons.append(f"Evening hours ({hour_of_day}:00) - declining energy")
            confidence += 0.1
            side = "short"  # Evening favors downward movement
        
        # Fibonacci time cycles (simplified)
        current_day = datetime.now().day
        if current_day in [1, 2, 3, 5, 8, 13, 21]:
            reasons.append(f"Fibonacci day of month ({current_day})")
            confidence += 0.2
        
        # Market-cosmic confluence
        if (side == "long" and change_24h > 0) or (side == "short" and change_24h < 0):
            reasons.append("Cosmic alignment matches market trend")
            confidence += 0.15
        
        # Apply additional cosmic confidence from market data
        total_cosmic = cosmic_confidence + cosmic_risk_adjustment
        if total_cosmic > 0:
            reasons.append(f"Positive cosmic bias: {total_cosmic:.2f}")
            confidence += total_cosmic
        elif total_cosmic < 0:
            reasons.append(f"Negative cosmic bias: {total_cosmic:.2f}")
            confidence -= abs(total_cosmic)
        
        # Numerological analysis of the price
        price_digits = [int(d) for d in str(int(current_price)) if d.isdigit()]
        digit_sum = sum(price_digits)
        reduced_sum = digit_sum
        while reduced_sum >= 10:
            reduced_sum = sum([int(d) for d in str(reduced_sum) if d.isdigit()])
        
        # Check for numerological significance
        if reduced_sum in [1, 3, 9]:  # Growth numbers
            reasons.append(f"Price has growth numerology ({reduced_sum})")
            side = "long"
            confidence += 0.15
        elif reduced_sum in [4, 8]:  # Stability numbers
            reasons.append(f"Price has stability numerology ({reduced_sum})")
            confidence += 0.1
        elif reduced_sum in [2, 7]:  # Reversal numbers
            reasons.append(f"Price has reversal numerology ({reduced_sum})")
            side = "short" if side == "long" else "long"  # Flip the bias
            confidence += 0.15
        
        # Check for number patterns in price
        price_str = str(int(current_price))
        if len(set(price_str)) <= 2:  # e.g. 55555 or 45454
            reasons.append(f"Price shows harmonic pattern: {price_str}")
            confidence += 0.2
        
        # Set cosmic risk management parameters
        stop_loss = 0.0
        take_profit = 0.0
        if side == "long":
            stop_loss = current_price * 0.97  # 3% stop loss for long
            take_profit = current_price * 1.08  # 8% take profit for long
        else:
            stop_loss = current_price * 1.03  # 3% stop loss for short
            take_profit = current_price * 0.92  # 8% take profit for short
        
        # Determine final action based on confidence
        action = "WAIT"
        if confidence >= self.min_confidence:
            action = "ENTER"
        
        # Generate explanation
        if len(reasons) == 0:
            reasons.append("No clear cosmic entry signal")
            explanation = "Cosmic analysis shows no compelling entry opportunity at this time."
        else:
            explanation = f"Cosmic entry signal with {confidence:.2f} confidence based on " + \
                          f"celestial patterns and numerological significance."
        
        # Create and return recommendation object
        return PersonaEntryRecommendation(
            persona_name="Cosmic Trader",
            confidence=confidence,
            side=side,
            target_price=target_price,
            reasons=reasons,
            risk_level="moderate",
            time_horizon="variable",
            explanation=explanation,
            trap_awareness=0.5,  # Cosmic traders have moderate trap awareness
            position_size=6.0,  # Moderate position size as percentage of capital
            stop_loss=stop_loss,
            take_profit=take_profit,
            action=action
        )
    
    def _get_patient_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Patient entry recommendation logic."""
        symbol = market_data["symbol"]
        
        # Extract key market data for analysis
        change_24h = market_data.get("change_24h", 0)
        high_24h = market_data.get("high_24h", 0)
        low_24h = market_data.get("low_24h", 0)
        recent_high = market_data.get("recent_high", current_price * 1.05)
        recent_low = market_data.get("recent_low", current_price * 0.95)
        
        # Define reasons list to store entry signals
        reasons = []
        confidence = 0.0
        side = "long"  # Default side
        target_price = current_price
        
        # Patient traders wait for very clear setups and confluences
        # Calculate Fibonacci retracement levels for recent move
        fib_levels = {
            "0.382": recent_low + (recent_high - recent_low) * 0.382,
            "0.5": recent_low + (recent_high - recent_low) * 0.5,
            "0.618": recent_low + (recent_high - recent_low) * 0.618,
        }
        
        # Check for price at key Fibonacci retracement level - patient traders want exact matches
        near_fib_level = False
        nearest_fib = ""
        nearest_fib_dist_pct = float('inf')
        
        for level_name, level_price in fib_levels.items():
            dist_pct = abs(current_price - level_price) / current_price * 100
            if dist_pct < nearest_fib_dist_pct:
                nearest_fib_dist_pct = dist_pct
                nearest_fib = level_name
            
            # Consider price near a Fibonacci level if very close (within 0.2%)
            if dist_pct < 0.2:
                near_fib_level = True
                reasons.append(f"Price precisely at {level_name} Fibonacci retracement level")
                confidence += 0.3  # Patient traders give more weight to exact Fibonacci hits
        
        # Price touching recent swing high/low points
        if abs(current_price - recent_high) / recent_high < 0.002:  # Within 0.2% of recent high
            reasons.append("Price retesting recent swing high")
            side = "short"  # Patient traders prefer counter-trend at extremes
            confidence += 0.25
        elif abs(current_price - recent_low) / recent_low < 0.002:  # Within 0.2% of recent low
            reasons.append("Price retesting recent swing low")
            side = "long"  # Patient traders prefer counter-trend at extremes
            confidence += 0.25
        
        # Patient traders prefer reduced volatility for entries
        price_range_pct = (recent_high - recent_low) / recent_low * 100
        if price_range_pct < 2.0:  # Less than 2% range in recent period = low volatility
            reasons.append(f"Low volatility environment ({price_range_pct:.2f}% range)")
            confidence += 0.2
        
        # Multiple timeframe confluence - simulate by requiring multiple conditions
        confluence_count = len(reasons)
        if confluence_count >= 2:
            reasons.append(f"Multiple timeframe confluence ({confluence_count} factors)")
            confidence += 0.1 * confluence_count  # More confluence = higher confidence
        
        # Patient traders look for major trend changes
        if change_24h > 0 and current_price < fib_levels["0.382"]:
            reasons.append("Potential trend reversal: price below key retracement")
            side = "long"
            confidence += 0.2
        elif change_24h < 0 and current_price > fib_levels["0.618"]:
            reasons.append("Potential trend reversal: price above key retracement")
            side = "short"
            confidence += 0.2
        
        # Patient traders are skeptical of cosmic factors - unless very strong
        cosmic_confidence = market_data.get("cosmic_confidence", 0)
        cosmic_adjustment = market_data.get("cosmic_risk_adjustment", 0)
        total_cosmic = cosmic_confidence + cosmic_adjustment
        
        if abs(total_cosmic) > 0.2:  # Only significant cosmic readings matter
            if total_cosmic > 0.2:
                reasons.append("Strong positive cosmic alignment")
                confidence += 0.1
            else:
                reasons.append("Strong negative cosmic alignment")
                confidence -= 0.1
        
        # Set conservative risk management parameters
        stop_loss = 0.0
        take_profit = 0.0
        if side == "long":
            stop_loss = current_price * 0.98  # 2% stop loss for long
            take_profit = current_price * 1.06  # 6% take profit for long
        else:
            stop_loss = current_price * 1.02  # 2% stop loss for short
            take_profit = current_price * 0.94  # 6% take profit for short
        
        # Patient traders wait for higher confidence
        min_confidence_override = max(self.min_confidence, 0.6)  # Patient traders want at least 60% confidence
        
        # Determine final action based on confidence
        action = "WAIT"
        if confidence >= min_confidence_override:
            action = "ENTER"
        
        # Generate explanation
        if len(reasons) == 0:
            reasons.append("No clear patient entry signal")
            explanation = "Patient analysis shows no compelling entry opportunity at this time."
        else:
            explanation = f"Patient entry signal with {confidence:.2f} confidence based on " + \
                          f"precise technical levels and multiple confirmations."
        
        # Create and return recommendation object
        return PersonaEntryRecommendation(
            persona_name="Patient Trader",
            confidence=confidence,
            side=side,
            target_price=target_price,
            reasons=reasons,
            risk_level="low",
            time_horizon="long-term",
            explanation=explanation,
            trap_awareness=0.9,  # Patient traders have high trap awareness
            position_size=5.0,  # Moderate position size as percentage of capital
            stop_loss=stop_loss,
            take_profit=take_profit,
            action=action
        )
    
    def _get_contrarian_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Contrarian entry recommendation logic."""
        symbol = market_data["symbol"]
        
        # Extract key market data for analysis
        change_24h = market_data.get("change_24h", 0)
        high_24h = market_data.get("high_24h", 0)
        low_24h = market_data.get("low_24h", 0)
        recent_high = market_data.get("recent_high", current_price * 1.05)
        recent_low = market_data.get("recent_low", current_price * 0.95)
        
        # Define reasons list to store entry signals
        reasons = []
        confidence = 0.0
        side = "long"  # Will be set based on contrarian analysis
        target_price = current_price
        
        # Contrarian logic: look for extreme moves to fade
        # For strong moves up, look to short; for strong drops, look to long
        if change_24h > 8.0:  # Extreme upward movement
            reasons.append(f"Fading extreme upward move: {change_24h:.2f}% increase in 24h")
            side = "short"
            confidence += 0.3
            reasons.append("Market likely overextended to the upside")
        elif change_24h < -8.0:  # Extreme downward movement
            reasons.append(f"Fading extreme downward move: {change_24h:.2f}% decrease in 24h")
            side = "long"
            confidence += 0.3
            reasons.append("Market likely oversold")
        
        # Look for price at extremes
        if current_price > 0.98 * high_24h:  # Near 24h high
            reasons.append(f"Price near 24h high: {high_24h:.2f}")
            side = "short"  # Contrarian goes against the high
            confidence += 0.2
            target_price = current_price  # Enter at current price
        elif current_price < 1.02 * low_24h:  # Near 24h low
            reasons.append(f"Price near 24h low: {low_24h:.2f}")
            side = "long"  # Contrarian goes against the low
            confidence += 0.2
            target_price = current_price  # Enter at current price
        
        # RSI-like overbought/oversold logic (simplified)
        price_range = recent_high - recent_low
        if price_range > 0:
            relative_position = (current_price - recent_low) / price_range
            if relative_position > 0.8:  # In top 20% of recent range
                reasons.append("Price in upper range (overbought territory)")
                side = "short"
                confidence += 0.25
            elif relative_position < 0.2:  # In bottom 20% of recent range
                reasons.append("Price in lower range (oversold territory)")
                side = "long"
                confidence += 0.25
        
        # Contrarians often look at round psychological levels
        price_str = str(int(current_price))
        if price_str.endswith('000') or price_str.endswith('500'):
            reasons.append(f"Psychological level at {price_str} - expecting rejection")
            confidence += 0.1
            # If price approaching from below, expect rejection down; if from above, expect rejection up
            if current_price > float(price_str):
                side = "short"
            else:
                side = "long"
        
        # Contrarians take cosmic factors into account - but in reverse
        cosmic_confidence = market_data.get("cosmic_confidence", 0)
        if cosmic_confidence > 0:
            reasons.append("Fading positive cosmic bias")
            side = "short" if side == "long" else "long"  # Flip the side
            confidence += 0.1
        
        # Set contrarian risk management parameters
        stop_loss = 0.0
        take_profit = 0.0
        if side == "long":
            stop_loss = current_price * 0.96  # 4% stop loss for long
            take_profit = current_price * 1.08  # 8% take profit for long
        else:
            stop_loss = current_price * 1.04  # 4% stop loss for short
            take_profit = current_price * 0.92  # 8% take profit for short
        
        # Determine final action based on confidence
        action = "WAIT"
        if confidence >= self.min_confidence:
            action = "ENTER"
        
        # Generate explanation
        if len(reasons) == 0:
            reasons.append("No compelling contrarian entry signal")
            explanation = "Contrarian analysis shows no clear entry opportunity at this time."
        else:
            explanation = f"Contrarian entry signal with {confidence:.2f} confidence based on " + \
                          f"fading extreme moves and sentiment."
        
        # Create and return recommendation object
        return PersonaEntryRecommendation(
            persona_name="Contrarian Trader",
            confidence=confidence,
            side=side,
            target_price=target_price,
            reasons=reasons,
            risk_level="high",
            time_horizon="medium-term",
            explanation=explanation,
            trap_awareness=0.7,  # Contrarians are more aware of market traps
            position_size=7.0,  # Moderate-high position size percentage
            stop_loss=stop_loss,
            take_profit=take_profit,
            action=action
        )
    
    def format_recommendations_display(self, recommendations: List[PersonaEntryRecommendation], 
                                       symbol: str = "Unknown", current_price: float = 0.0) -> str:
        """
        Format entry recommendations for display.
        
        Args:
            recommendations: List of persona recommendations
            symbol: Market symbol
            current_price: Current price
            
        Returns:
            Formatted string for display
        """
        if not recommendations:
            return self.colorize(Colors.YELLOW, 'No recommendations available.')
        
        # Count entry vs wait recommendations
        enter_recs = [r for r in recommendations if r.action == "ENTER"]
        wait_recs = [r for r in recommendations if r.action == "WAIT"]
        
        output = []
        
        # Add entry recommendations section
        if enter_recs:
            output.append(f"\n{self.colorize(Colors.BOLD + Colors.GREEN, 'Entry Recommendations:')}")
            
            # Sort by confidence
            for rec in sorted(enter_recs, key=lambda r: r.confidence, reverse=True):
                output.append(self._format_single_recommendation(rec))
        
        # Add wait recommendations section
        if wait_recs:
            output.append(f"\n{self.colorize(Colors.BOLD + Colors.YELLOW, 'Wait Recommendations:')}")
            
            # Sort by confidence
            for rec in sorted(wait_recs, key=lambda r: r.confidence, reverse=True):
                output.append(self._format_single_recommendation(rec))
        
        return "\n".join(output)
        
    def _format_single_recommendation(self, rec: PersonaEntryRecommendation) -> str:
        """Format a single recommendation for display."""
        # Create confidence bar (10 chars wide)
        conf_val = max(0, min(1, rec.confidence))  # Ensure 0-1 range
        
        # Color the confidence bar based on confidence level
        if conf_val >= 0.8:
            conf_color = Colors.GREEN
        elif conf_val >= 0.5:
            conf_color = Colors.YELLOW
        else:
            conf_color = Colors.RED
            
        conf_bar = self.colorize(conf_color, "█" * int(conf_val * 10)) + self.colorize(Colors.RESET, "░" * (10 - int(conf_val * 10)))
        
        # Build the formatted output
        output = []
        
        # Persona name and confidence
        if rec.action == "ENTER":
            if rec.side == "long":
                side_color = Colors.GREEN
                side_display = f"{Colors.BOLD}{side_color}LONG{Colors.END}"
            else:
                side_color = Colors.RED
                side_display = f"{Colors.BOLD}{side_color}SHORT{Colors.END}"
                
            output.append(f"  {self.colorize(Colors.BOLD + Colors.CYAN, rec.persona_name)} ({self.colorize(conf_color, f'{rec.confidence:.2f}')}) - {side_display}:")
        else:
            output.append(f"  {self.colorize(Colors.BOLD + Colors.BLUE, rec.persona_name)} ({self.colorize(conf_color, f'{rec.confidence:.2f}')}):")
            
        # Confidence bar
        output.append(f"    {conf_bar}")
        
        # Reasons
        if hasattr(rec, 'reasons') and rec.reasons:
            reasons_text = f"{self.colorize(Colors.BOLD, 'Reasons:')} {self.colorize(Colors.PURPLE, ', '.join(rec.reasons))}"
            output.append(f"    {reasons_text}")
            
        # Explanation
        if hasattr(rec, 'explanation') and rec.explanation:
            output.append(f"    → {self.colorize(Colors.CYAN, rec.explanation)}")
            
        # Additional details for entry recommendations
        if rec.action == "ENTER":
            if hasattr(rec, 'risk_level') and hasattr(rec, 'time_horizon'):
                risk_color = Colors.RED if rec.risk_level == "high" else Colors.YELLOW if rec.risk_level == "moderate" else Colors.GREEN
                output.append(f"    {self.colorize(Colors.BOLD, 'Approach:')} {self.colorize(risk_color, rec.risk_level.capitalize())} risk, {self.colorize(Colors.BLUE, rec.time_horizon)} horizon")
                
            if hasattr(rec, 'position_size') and hasattr(rec, 'stop_loss') and hasattr(rec, 'take_profit'):
                position_text = f"{self.colorize(Colors.BOLD, 'Position Size:')} {self.colorize(Colors.GREEN, f'{rec.position_size:.2f}')}%"
                stop_text = f"{self.colorize(Colors.BOLD, 'Stop Loss:')} {self.colorize(Colors.RED, f'{rec.stop_loss:.1f}')}" 
                take_text = f"{self.colorize(Colors.BOLD, 'Take Profit:')} {self.colorize(Colors.GREEN, f'{rec.take_profit:.1f}')}"
                output.append(f"    {position_text} | {stop_text} | {take_text}")
                
        # Add empty line at the end
        output.append("")
        
        return "\n".join(output)

def demo():
    """Run a simple demo of the persona-based entry strategy."""
    # Create a persona entry manager
    persona_manager = PersonaEntryManager(min_confidence=0.5, use_color=True)
    
    # Sample market data for demonstration - optimized for cosmic entry signal
    market_data = {
        "symbol": "BTCUSDT",
        "price": 47700.0,  # Price very close to 0.618 Fibonacci level
        "volume": 1500000.0,
        "avg_volume": 800000.0,  # High volume (over 1.5x average)
        "change_24h": -6.5,  # Significant drop suggesting potential reversal
        "high_24h": 50000.0,
        "low_24h": 44000.0,  # 47700 is very close to 0.618 Fibonacci level (47708)
        "force_cosmic_conditions": True  # Force optimal cosmic conditions for demo
    }
    
    # Generate entry recommendations
    entry_strategy = persona_manager.generate_entry_recommendations(market_data)
    
    # Display recommendations
    print("\nOMEGA BTC AI - Persona-Based Entry Strategy Demo")
    print(f"Analyzing {market_data['symbol']} with {len(persona_manager.trader_personas)} trader personas")
    print(f"Minimum confidence threshold: {persona_manager.min_confidence}")
    print(persona_manager.format_recommendations_display(entry_strategy.recommendations))

def run_continuous_monitor(interval=60, min_confidence=0.5, use_color=True, use_mock=True):
    """
    Run the entry monitor in continuous mode.
    
    Args:
        interval: Seconds between updates
        min_confidence: Minimum confidence threshold for recommendations
        use_color: Whether to use colored output
        use_mock: Whether to use mock market data instead of real BitGet data
    """
    manager = PersonaEntryManager(
        min_confidence=min_confidence,
        use_color=use_color,
        continuous_mode=True
    )
    
    # Simple header (like the exit monitor)
    print(f"{Colors.BOLD}OMEGA BTC AI - Persona Entry Monitor{Colors.END}")
    print(f"Running continuously. Press Ctrl+C to stop.")
    print(f"Refreshing every {interval} seconds")
    print(f"=====================================")
    
    try:
        while True:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Print simplified header
            print(f"{Colors.BOLD}OMEGA BTC AI - Persona Entry Monitor{Colors.END}")
            print(f"Running continuously. Press Ctrl+C to stop.")
            print(f"Refreshing every {interval} seconds")
            print(f"=====================================")
            
            print(f"\nInitialized PersonaEntryManager with {len(manager.trader_personas)} trader personas")
            
            print(f"\n{Colors.BOLD}{Colors.GREEN}OMEGA BTC AI - Persona-Based Entry Strategy Demo{Colors.END}")
            print(f"{Colors.CYAN}Running in continuous monitoring mode{Colors.END}")
            
            # Get active positions from BitGet if not using mock data
            positions_data = None
            active_positions = []
            if not use_mock:
                positions_data = get_positions_from_bitget()
                if isinstance(positions_data, dict) and "error" in positions_data:
                    print(f"{Colors.RED}Error fetching positions: {positions_data['error']}{Colors.END}")
                elif isinstance(positions_data, dict) and positions_data.get("success", False):
                    active_positions = positions_data.get("positions", [])
                    connection_status = positions_data.get('connection', 'UNKNOWN')
                    print(f"{Colors.GREEN}CONNECTED TO BITGET MAINNET{Colors.END}")
                    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"Analyzing {len(active_positions)} positions with {len(manager.trader_personas)} trader personas")
                    print(f"Minimum confidence threshold: {min_confidence}")
                    
                    # Display position information
                    if active_positions:
                        for pos in active_positions:
                            if isinstance(pos, dict):
                                # Handle positions safely using dict.get with default values
                                symbol = pos.get('symbol', 'UNKNOWN')
                                side = str(pos.get('side', 'UNKNOWN')).upper()
                                entry_price = float(pos.get('entryPrice', 0))
                                unrealized_pnl = float(pos.get('unrealizedPnl', 0))
                                unrealized_pnl_pct = float(pos.get('unrealizedPnlPercentage', 0)) * 100
                                
                                # Get current price from position data
                                current_price = float(pos.get('markPrice', 0)) or entry_price
                                
                                side_color = Colors.GREEN if side == "LONG" else Colors.RED
                                pnl_color = Colors.GREEN if unrealized_pnl > 0 else Colors.RED
                                
                                print(f"\nPosition: {Colors.BOLD}{symbol} {side_color}{side}{Colors.END} @ {entry_price:.8f}")
                                print(f"Current Price: {current_price:.2f}")
                                print(f"PnL: {pnl_color}{unrealized_pnl_pct:.2f}%{Colors.END}")
            else:
                print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Analyzing mock data with {len(manager.trader_personas)} trader personas")
                print(f"Minimum confidence threshold: {min_confidence}")
            
            # Get market data for analysis
            symbols_to_analyze = ["BTCUSDT"]  # Default symbol
            
            # If we have position data, add those symbols to analysis
            for pos in active_positions:
                if isinstance(pos, dict):
                    symbol_raw = pos.get('symbol', '')
                    # Extract base symbol from format like "BTC/USDT:USDT"
                    if isinstance(symbol_raw, str) and '/' in symbol_raw and ':' in symbol_raw:
                        parts = symbol_raw.split('/')
                        if len(parts) > 0:
                            base = parts[0]
                            symbol = f"{base}USDT"
                            if symbol not in symbols_to_analyze:
                                symbols_to_analyze.append(symbol)
            
            # Get cosmic time data for sentiment adjustment
            current_hour = datetime.now().hour
            current_day = datetime.now().weekday()  # 0 = Monday, 6 = Sunday
            
            # Get moon phase data
            moon_phase = "waning"  # Placeholder - would come from actual lunar data
            
            # For demo: positive cosmic sentiment during weekday daytime, negative during nights/weekends
            cosmic_confidence = 0.05  # Base cosmic bias
            cosmic_risk_adjustment = 0.0
            
            # Weekend effect (negative)
            if current_day >= 5:  # Saturday or Sunday
                cosmic_risk_adjustment -= 0.1
                
            # After-hours effect (negative)
            if current_hour < 7 or current_hour > 19:
                cosmic_risk_adjustment -= 0.1
                
            # For each symbol, analyze market and show results
            for symbol in symbols_to_analyze:
                if use_mock:
                    market_data = get_mock_market_data(symbol)
                else:
                    market_data = get_real_market_data(symbol)
                
                # Add cosmic data
                market_data["cosmic_confidence"] = cosmic_confidence
                market_data["cosmic_risk_adjustment"] = cosmic_risk_adjustment
                market_data["moon_phase"] = moon_phase
                market_data["day_of_week"] = current_day
                market_data["hour_of_day"] = current_hour
                
                current_price = market_data["current_price"]
                change_24h = market_data["change_24h"]
                
                if not active_positions:
                    print(f"\nPosition: {Colors.BOLD}{symbol}{Colors.END}")
                    print(f"Current Price: {current_price:.2f}")
                    pnl_color = Colors.GREEN if change_24h > 0 else Colors.RED
                    print(f"PnL: {pnl_color}{change_24h:.2f}%{Colors.END}")
                
                # Generate entry recommendations
                strategy = manager.generate_entry_recommendations(market_data)
                
                # Display results - using styling similar to the exit monitor
                if "ENTER" in strategy.summary:
                    print(f"\n🔔 {Colors.YELLOW}SIGNIFICANT RECOMMENDATION CHANGE: {symbol}_{strategy.summary.split()[1].lower()}{Colors.END}")
                
                print(f"\n🧠 {Colors.BOLD}{Colors.PURPLE}PERSONA-BASED RECOMMENDATIONS:{Colors.END}")
                if "ENTER" in strategy.summary:
                    print(f"{Colors.GREEN}{strategy.summary}{Colors.END}")
                else:
                    print(f"{Colors.YELLOW}{strategy.summary}{Colors.END}")
                
                print(f"\nALL PERSONA OPINIONS:")
                
                # Separate recommendations by action
                enter_recs = [r for r in strategy.recommendations if r.action == "ENTER"]
                wait_recs = [r for r in strategy.recommendations if r.action == "WAIT"]
                
                if enter_recs:
                    print(f"\nEntry Recommendations:")
                    for rec in sorted(enter_recs, key=lambda r: r.confidence, reverse=True):
                        # Format similar to exit screen
                        conf_val = max(0, min(1, rec.confidence))
                        conf_color = Colors.GREEN if conf_val >= 0.8 else Colors.YELLOW if conf_val >= 0.5 else Colors.RED
                        conf_bar = "█" * int(conf_val * 10) + "░" * (10 - int(conf_val * 10))
                        
                        print(f"  {rec.persona_name} ({conf_color}{rec.confidence:.2f}{Colors.END}):")
                        print(f"    {conf_color}{conf_bar}{Colors.END}")
                        
                        if hasattr(rec, 'reasons') and rec.reasons:
                            print(f"    Reasons: {', '.join(rec.reasons)}")
                            
                        if hasattr(rec, 'risk_level') and hasattr(rec, 'time_horizon'):
                            print(f"    Approach: {rec.risk_level.capitalize()} risk, {rec.time_horizon} horizon")
                            
                        if hasattr(rec, 'explanation') and rec.explanation:
                            print(f"    → {rec.explanation}")
                
                if wait_recs:
                    print(f"\nWait Recommendations:")
                    for rec in sorted(wait_recs, key=lambda r: r.confidence, reverse=True):
                        # Format similar to exit screen
                        conf_val = max(0, min(1, rec.confidence))
                        conf_color = Colors.GREEN if conf_val >= 0.8 else Colors.YELLOW if conf_val >= 0.5 else Colors.RED
                        conf_bar = "█" * int(conf_val * 10) + "░" * (10 - int(conf_val * 10))
                        
                        print(f"  {rec.persona_name} ({conf_color}{rec.confidence:.2f}{Colors.END}):")
                        print(f"    {conf_color}{conf_bar}{Colors.END}")
                        
                        if hasattr(rec, 'reasons') and rec.reasons:
                            print(f"    Reasons: {', '.join(rec.reasons)}")
                            
                        if hasattr(rec, 'explanation') and rec.explanation:
                            print(f"    → {rec.explanation}")
            
            # Add last updated timestamp
            print(f"\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            print(f"\n{'='*70}")
            
            print(f"Analysis Complete")
            
            # Sleep until next interval
            print(f"\nNext update in {interval} seconds...")
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print(f"\nGracefully exiting the Persona-Based Entry Monitor...")

def get_mock_market_data(symbol="BTCUSDT"):
    """
    Generate mock market data for development and testing.
    """
    # Generate a random price between 60000 and 70000 for BTC
    # or between 2500 and 3500 for ETH
    if symbol.startswith("BTC"):
        base_price = random.uniform(60000, 70000)
        # Generate recent high and low for Fibonacci analysis
        recent_high = base_price * random.uniform(1.01, 1.05)  # 1-5% higher
        recent_low = base_price * random.uniform(0.95, 0.99)   # 1-5% lower
        vol_base = 100000000
    elif symbol.startswith("ETH"):
        base_price = random.uniform(2500, 3500)
        # Generate recent high and low for Fibonacci analysis
        recent_high = base_price * random.uniform(1.01, 1.05)  # 1-5% higher
        recent_low = base_price * random.uniform(0.95, 0.99)   # 1-5% lower
        vol_base = 50000000
    else:
        base_price = random.uniform(1, 100)
        # Generate recent high and low for Fibonacci analysis
        recent_high = base_price * random.uniform(1.01, 1.05)  # 1-5% higher
        recent_low = base_price * random.uniform(0.95, 0.99)   # 1-5% lower
        vol_base = 10000000

    # Generate mock market data
    return {
        "symbol": symbol,
        "current_price": base_price,
        "change_24h": random.uniform(-5.0, 5.0),
        "volume": vol_base * random.uniform(0.8, 1.2),
        "avg_volume": vol_base,
        "high_24h": base_price * random.uniform(1.01, 1.05),
        "low_24h": base_price * random.uniform(0.95, 0.99),
        "recent_high": recent_high,  # For Fibonacci analysis
        "recent_low": recent_low,    # For Fibonacci analysis
        "timestamp": int(time.time())
    }

def get_positions_from_bitget():
    """
    Fetch and return BitGet positions using CCXT.
    """
    # Get API credentials from environment
    api_key = os.environ.get('BITGET_API_KEY')
    api_secret = os.environ.get('BITGET_SECRET_KEY')
    api_passphrase = os.environ.get('BITGET_PASSPHRASE')
    
    # Verify API credentials
    if not api_key or not api_secret or not api_passphrase:
        print("❌ Missing BitGet API credentials in environment variables")
        return {"error": "Missing credentials"}
    
    # Create direct CCXT BitGet client
    try:
        if not HAVE_CCXT:
            print("❌ ccxt module not installed. Install with: pip install ccxt")
            return {"error": "ccxt module not installed"}
            
        # Create the exchange client
        exchange = ccxt.bitget({
            'apiKey': api_key,
            'secret': api_secret,
            'password': api_passphrase,
            'options': {
                'defaultType': 'swap',
            }
        })
        
        # Fetch positions - CCXT method names use camelCase
        positions = exchange.fetch_positions()
        
        # Filter out positions with zero contracts
        active_positions = [p for p in positions if float(p.get('contracts', 0)) > 0]
        
        # Return position data and API connection info
        return {
            "success": True,
            "positions": active_positions,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "connection": "CONNECTED TO BITGET MAINNET"
        }
        
    except ImportError:
        print("❌ ccxt module not installed. Install with: pip install ccxt")
        return {"error": "ccxt module not installed"}
    except Exception as e:
        print(f"❌ Error fetching positions: {str(e)}")
        return {"error": str(e)}

def get_real_market_data(symbol="BTCUSDT"):
    """
    Fetch real market data from BitGet API using CCXT.
    """
    # Get API credentials from environment
    api_key = os.environ.get('BITGET_API_KEY')
    api_secret = os.environ.get('BITGET_SECRET_KEY')
    api_passphrase = os.environ.get('BITGET_PASSPHRASE')
    
    # Verify API credentials
    if not api_key or not api_secret or not api_passphrase:
        print("⚠️ BitGet API credentials not found. Make sure to set BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE environment variables.")
        return get_mock_market_data(symbol)
    
    # Create CCXT BitGet client
    try:
        if not HAVE_CCXT:
            print("❌ ccxt module not installed. Install with: pip install ccxt")
            return get_mock_market_data(symbol)
            
        # Format symbol for CCXT
        formatted_symbol = f"{symbol.replace('USDT', '')}/USDT:USDT"
        
        # Create the exchange client
        exchange = ccxt.bitget({
            'apiKey': api_key,
            'secret': api_secret,
            'password': api_passphrase,
            'options': {
                'defaultType': 'swap',
            }
        })
        
        # Fetch ticker data
        ticker = exchange.fetch_ticker(formatted_symbol)
        
        # Fetch OHLCV (candlesticks) data for high/low analysis
        # Get last 24 hours of 15-minute candles
        try:
            ohlcv = exchange.fetch_ohlcv(
                formatted_symbol,
                timeframe='15m',
                limit=96  # 96 * 15min = 24 hours
            )
            
            # Process candle data for high and low
            recent_high = 0
            recent_low = float('inf')
            
            if ohlcv and len(ohlcv) > 0:
                for candle in ohlcv:
                    high = float(candle[2])  # High price is at index 2
                    low = float(candle[3])   # Low price is at index 3
                    recent_high = max(recent_high, high)
                    recent_low = min(recent_low, low)
            else:
                # Fallback if ohlcv data is not available
                recent_high = float(ticker.get('high', 0))
                recent_low = float(ticker.get('low', 0))
            
            # If we somehow still don't have valid values, use current price with adjustment
            current_price = float(ticker.get('last', 0))
            if recent_high <= 0:
                recent_high = current_price * 1.05
            if recent_low == float('inf') or recent_low <= 0:
                recent_low = current_price * 0.95
            
            # Build and return market data dictionary
            return {
                "symbol": symbol,
                "current_price": current_price,
                "change_24h": float(ticker.get('percentage', 0)),
                "volume": float(ticker.get('baseVolume', 0)),
                "avg_volume": float(ticker.get('baseVolume', 0)),  # Using current volume as avg for now
                "high_24h": float(ticker.get('high', 0)),
                "low_24h": float(ticker.get('low', 0)),
                "recent_high": recent_high,  # For Fibonacci analysis
                "recent_low": recent_low,    # For Fibonacci analysis
                "timestamp": int(time.time())
            }
            
        except Exception as e:
            print(f"⚠️ Error fetching OHLCV data: {e}")
            return get_mock_market_data(symbol)
            
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        print("Falling back to mock data...")
        return get_mock_market_data(symbol)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - Persona-Based Entry Strategy")
    parser.add_argument("--continuous", action="store_true", help="Run the monitor continuously")
    parser.add_argument("--interval", type=int, default=60, help="Interval between checks in seconds")
    parser.add_argument("--min-confidence", type=float, default=0.5, help="Minimum confidence threshold (0.0-1.0)")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--mock", action="store_true", help="Use mock data instead of real BitGet data")
    args = parser.parse_args()
    
    if args.continuous:
        try:
            run_continuous_monitor(
                interval=args.interval,
                min_confidence=args.min_confidence,
                use_color=not args.no_color,
                use_mock=args.mock  # Use mock data if specified, otherwise use real data
            )
        except KeyboardInterrupt:
            print("\nExiting...")
    else:
        # Just run once
        manager = PersonaEntryManager(min_confidence=args.min_confidence, use_color=not args.no_color)
        
        # Get market data
        if args.mock:
            market_data = get_mock_market_data()
        else:
            market_data = get_real_market_data()
        
        # Analyze and generate recommendations
        manager.analyze_market(market_data) 