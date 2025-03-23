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
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field

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
    """Collection of entry recommendations from different trader personas."""
    market_symbol: str
    current_price: float
    recommendations: List[PersonaEntryRecommendation] = field(default_factory=list)
    summary: str = ""
    
    def add_recommendation(self, recommendation: PersonaEntryRecommendation) -> None:
        """Add a persona-based recommendation."""
        self.recommendations.append(recommendation)
        
    def get_average_confidence(self) -> float:
        """Get the average confidence across all entry recommendations."""
        if not self.recommendations:
            return 0.0
        entry_recs = [r for r in self.recommendations if r.action == "ENTER"]
        if not entry_recs:
            return 0.0
        return sum(r.confidence for r in entry_recs) / len(entry_recs)
    
    def get_highest_confidence_recommendation(self) -> Optional[PersonaEntryRecommendation]:
        """Get the recommendation with the highest confidence."""
        entry_recs = [r for r in self.recommendations if r.action == "ENTER"]
        if not entry_recs:
            return None
        return max(entry_recs, key=lambda r: r.confidence)
    
    def generate_summary(self) -> str:
        """Generate a summary of all recommendations."""
        if not self.recommendations:
            return "No entry recommendations available."
        
        # Count entry vs. wait recommendations
        entry_recs = [r for r in self.recommendations if r.action == "ENTER"]
        wait_recs = [r for r in self.recommendations if r.action == "WAIT"]
        
        if not entry_recs:
            summary = f"NO ENTRY SIGNAL: {len(wait_recs)} personas recommend waiting"
            self.summary = summary
            return summary
            
        # For entry recommendations, check the confidence
        avg_confidence = self.get_average_confidence()
        high_conf_rec = self.get_highest_confidence_recommendation()
        
        # Calculate if entry recommendations are primarily long or short
        long_recs = [r for r in entry_recs if r.side == "long"]
        short_recs = [r for r in entry_recs if r.side == "short"]
        
        # Determine the predominant direction
        direction = "LONG" if len(long_recs) > len(short_recs) else "SHORT"
        
        if avg_confidence >= 0.7:
            summary = f"STRONG {direction} ENTRY SIGNAL: {len(entry_recs)} personas recommend entering"
            if high_conf_rec:
                summary += f", led by {high_conf_rec.persona_name} ({high_conf_rec.confidence:.2f})"
        elif avg_confidence >= 0.5:
            summary = f"MODERATE {direction} ENTRY SIGNAL: Mixed recommendations from {len(entry_recs)} personas"
        else:
            summary = f"WEAK {direction} ENTRY SIGNAL: {len(entry_recs)} personas with low confidence"
        
        if wait_recs:
            summary += f" - {len(wait_recs)} personas recommend waiting"
            
        self.summary = summary
        return summary

class PersonaEntryManager:
    """
    Manages entry recommendations from different trader personas.
    """
    
    def __init__(self, min_confidence: float = 0.5, use_color: bool = True, continuous_mode: bool = False):
        """
        Initialize the persona-based entry recommendation system.
        
        Args:
            min_confidence: Minimum confidence threshold for entry recommendations
            use_color: Whether to use colored output in terminal
            continuous_mode: Whether the monitor is running in continuous mode
        """
        self.min_confidence = min_confidence
        self.use_color = use_color
        self.continuous_mode = continuous_mode
        
        # Trader persona names
        self.trader_personas = ["strategic", "aggressive", "newbie", "scalper", "cosmic"]
        
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

    def generate_entry_recommendations(self, market_data: Dict[str, Any]) -> PersonaBasedEntryStrategy:
        """
        Generate entry recommendations from different trader personas.
        
        Args:
            market_data: Market data including price, volume, etc.
            
        Returns:
            PersonaBasedEntryStrategy with recommendations from different personas
        """
        # Extract market details
        symbol = market_data.get('symbol', 'BTCUSDT')
        current_price = float(market_data.get('price', 0))
        
        # Create entry strategy object
        entry_strategy = PersonaBasedEntryStrategy(
            market_symbol=symbol,
            current_price=current_price
        )
        
        # Generate recommendations from each persona
        for persona_name in self.trader_personas:
            # Get entry recommendation for current persona
            recommendation = self._get_persona_recommendation(
                persona_name, market_data, current_price
            )
            
            # Add recommendation if confidence meets threshold
            if recommendation and (recommendation.action == "WAIT" or recommendation.confidence >= self.min_confidence):
                entry_strategy.add_recommendation(recommendation)
        
        # Generate summary
        entry_strategy.generate_summary()
        return entry_strategy
    
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
        
        return None
        
    def _get_strategic_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Implementation will be expanded in future versions"""
        # Placeholder for Strategic Trader entry logic
        return PersonaEntryRecommendation(
            persona_name="Strategic Trader",
            confidence=0.0,  # Will be calculated based on actual conditions
            side="long",     # Will be determined based on analysis
            target_price=current_price,
            reasons=["Placeholder for Strategic Trader entry logic"],
            risk_level="conservative",
            time_horizon="long-term",
            explanation="Strategic entry logic to be implemented",
            trap_awareness=0.8,
            position_size=2.0,  # % of capital
            stop_loss=current_price * 0.95,  # 5% below entry
            take_profit=current_price * 1.08,  # 8% above entry
            action="WAIT"  # Default to WAIT until proper implementation
        )
    
    def _get_aggressive_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Implementation will be expanded in future versions"""
        # Placeholder for Aggressive Trader entry logic
        return PersonaEntryRecommendation(
            persona_name="Aggressive Trader",
            confidence=0.0,
            side="long",
            target_price=current_price,
            reasons=["Placeholder for Aggressive Trader entry logic"],
            risk_level="aggressive",
            time_horizon="medium-term",
            explanation="Aggressive entry logic to be implemented",
            trap_awareness=0.6,
            position_size=4.0,
            stop_loss=current_price * 0.90,  # 10% below entry
            take_profit=current_price * 1.15,  # 15% above entry
            action="WAIT"
        )
    
    def _get_newbie_entry(self, market_data: Dict[str, Any], current_price: float) -> PersonaEntryRecommendation:
        """Implementation will be expanded in future versions"""
        # Placeholder for Newbie Trader entry logic
        return PersonaEntryRecommendation(
            persona_name="Newbie Trader",
            confidence=0.0,
            side="long",
            target_price=current_price,
            reasons=["Placeholder for Newbie Trader entry logic"],
            risk_level="moderate",
            time_horizon="variable",
            explanation="Newbie entry logic to be implemented",
            trap_awareness=0.3,
            position_size=5.0,
            stop_loss=current_price * 0.95,  # 5% below entry
            take_profit=current_price * 1.02,  # 2% above entry
            action="WAIT"
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
        """Get entry recommendation from Cosmic Trader persona based on divine market flow."""
        confidence = 0.0
        reasons = []
        explanation = ""
        side = "long"  # Default to long, will determine based on cosmic influences
        
        # Get current time to determine cosmic influences
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        
        # For demo purposes - force new moon and Monday for optimal entry conditions
        if 'force_cosmic_conditions' in market_data and market_data['force_cosmic_conditions']:
            moon_day = 1  # New moon
            day_of_week = 0  # Monday
            hour = 9  # Morning trading
            mercury_retrograde = False
        else:
            # Determine if Mercury is retrograde (simplified simulation)
            mercury_retrograde = (now.day % 7 == 0)  # Every 7th day of month
            moon_day = now.day % 30
        
        # Determine moon phase (simplified simulation)
        if moon_day < 4:  # New Moon
            moon_phase = "new_moon"
        elif moon_day < 11:  # Waxing 
            moon_phase = "waxing"
        elif moon_day < 15:  # Full Moon approaching
            moon_phase = "full_approaching"
        elif moon_day < 19:  # Full Moon
            moon_phase = "full_moon"
        else:  # Waning
            moon_phase = "waning"
        
        print(f"Cosmic Analysis - Moon phase: {moon_phase}, Day of week: {day_of_week}, Hour: {hour}")
            
        # Base cosmic influences
        cosmic_risk_appetite = 0.0
        
        # Moon phase influences
        if moon_phase == "new_moon":
            cosmic_risk_appetite += 0.3  # New beginnings - more risk
            reasons.append("New moon cycle initiation")
            explanation = "The new lunar cycle begins, perfect for planting the seeds of new positions."
            confidence += 0.3
        elif moon_phase == "waxing":
            cosmic_risk_appetite += 0.2  # Building energy
            reasons.append("Waxing moon energy accumulation")
            explanation = "The lunar cycle is building energy, favorable for establishing positions."
            confidence += 0.2
        elif moon_phase == "full_approaching":
            cosmic_risk_appetite -= 0.1  # Caution as we approach peak
            reasons.append("Approaching energy peak")
            explanation = "Approaching the full moon, energy is high but volatile."
            confidence += 0.1
        elif moon_phase == "full_moon":
            cosmic_risk_appetite -= 0.3  # Full moon - peak energy, potential reversal
            reasons.append("Full moon cycle peak")
            explanation = "The lunar energy is at maximum, signaling potential completion of cycles."
            # Less favorable for new entries
            confidence -= 0.2
        else:  # waning
            cosmic_risk_appetite -= 0.2  # Declining energy
            reasons.append("Waning moon cycle dissolution")
            explanation = "The lunar cycle is releasing energy, better to wait for new beginnings."
            confidence -= 0.1
            
        # Mercury retrograde makes cosmic traders more cautious
        if mercury_retrograde:
            cosmic_risk_appetite -= 0.3
            reasons.append("Mercury retrograde caution")
            explanation += " Mercury retrograde suggests communication and transaction issues, exercise caution."
            confidence -= 0.2
            
        # Time of day effects
        if hour >= 8 and hour <= 10:  # Morning market flow
            cosmic_risk_appetite += 0.1
            reasons.append("Morning market flow initiation")
            explanation += " Morning hours bring fresh energy and ideal entry conditions."
            confidence += 0.1
        elif hour >= 14 and hour <= 16:  # Afternoon volatility
            cosmic_risk_appetite -= 0.1
            reasons.append("Afternoon volatility fluctuation")
            explanation += " Afternoon brings uncertain energy, proceed with awareness."
            confidence -= 0.05
        elif hour >= 2 and hour <= 4:  # Deep night hours - connected to universe
            cosmic_risk_appetite += 0.2
            reasons.append("Deep night universal connection")
            explanation += " Night hours connect to deeper cosmic wisdom, favorable for intuitive entries."
            confidence += 0.15
        
        # Day of week effects
        if day_of_week == 0:  # Monday - new energy
            cosmic_risk_appetite += 0.1
            reasons.append("Weekly cycle initiation")
            explanation += " Beginning of trading week brings fresh market energy."
            confidence += 0.05
        elif day_of_week == 4:  # Friday - closing energy
            cosmic_risk_appetite -= 0.2
            reasons.append("Weekly cycle completion")
            explanation += " End of trading week suggests waiting for new cycles to begin."
            confidence -= 0.1
        
        # Market data analysis for cosmic patterns
        # Check for Fibonacci relationships in recent price movements
        if "high_24h" in market_data and "low_24h" in market_data:
            high_24h = float(market_data.get("high_24h", current_price))
            low_24h = float(market_data.get("low_24h", current_price))
            range_24h = high_24h - low_24h
            
            # Check if current price is at a key Fibonacci level
            if range_24h > 0:
                fib_618_level = low_24h + (range_24h * 0.618)
                fib_382_level = low_24h + (range_24h * 0.382)
                
                # Price near the golden ratio retracement (0.618)
                if abs(current_price - fib_618_level) / range_24h < 0.05:
                    reasons.append("Golden ratio alignment (0.618)")
                    explanation += " Price is aligned with the divine golden ratio (0.618), a cosmic harmony point."
                    confidence += 0.3
                    side = "long"  # Golden ratio retracement is bullish
                    
                # Price near the 0.382 Fibonacci level
                elif abs(current_price - fib_382_level) / range_24h < 0.05:
                    reasons.append("Fibonacci harmony point (0.382)")
                    explanation += " Price found balance at the 0.382 Fibonacci level, a cosmic support zone."
                    confidence += 0.2
                    side = "long"
        
        # Check for potential reversal patterns - suggests short position
        if "change_24h" in market_data:
            change_24h = float(market_data.get("change_24h", 0))
            
            # Strong upward movement may be nearing completion
            if change_24h > 5.0:
                reasons.append("Energy cycle completion")
                explanation += " Strong recent rise suggests completion of positive energy cycle."
                confidence += 0.25
                side = "short"  # Suggest reversal short
                
            # Strong downward movement may be bottoming
            elif change_24h < -5.0:
                reasons.append("Negative energy cycle exhaustion")
                explanation += " Strong recent decline suggests negative energy depletion and potential reversal."
                confidence += 0.25
                side = "long"  # Suggest reversal long
        
        # Volume analysis as energy flow indicator
        if "volume" in market_data and "avg_volume" in market_data:
            volume = float(market_data.get("volume", 0))
            avg_volume = float(market_data.get("avg_volume", volume))
            
            # High volume can indicate energy shift points
            if volume > (avg_volume * 1.5):
                reasons.append("Elevated energy flow (volume)")
                explanation += " Increased transaction energy suggests important vibrational shift."
                confidence += 0.15
            
        # Adjust overall confidence based on cosmic risk appetite
        final_confidence = confidence + cosmic_risk_appetite
        print(f"Cosmic confidence: {confidence:.2f} + cosmic risk appetite: {cosmic_risk_appetite:.2f} = final: {final_confidence:.2f}")
        
        # Cap confidence between 0 and 1
        final_confidence = max(0.0, min(1.0, final_confidence))
        
        # Determine action based on confidence
        action = "ENTER" if final_confidence >= 0.5 else "WAIT"
        
        # If cosmic confidence is low, recommend waiting
        if final_confidence < 0.5:
            action = "WAIT"
            if not reasons:
                reasons.append("Cosmic alignment not optimal")
            if not explanation:
                explanation = "The universal energies do not favor entry at this time. Patience is advised."
        
        # Ensure there's always at least one reason
        if not reasons:
            if final_confidence >= 0.5:
                reasons.append("Favorable cosmic alignment")
            else:
                reasons.append("Awaiting cosmic alignment")
            
        # Set appropriate stop loss and take profit based on side and risk profile
        if side == "long":
            stop_loss = current_price * 0.97  # 3% stop loss for long
            take_profit = current_price * 1.05  # 5% take profit for long
        else:  # short
            stop_loss = current_price * 1.03  # 3% stop loss for short
            take_profit = current_price * 0.95  # 5% take profit for short
        
        # Position size - varies based on cosmic alignment
        position_size = 2.0  # Base position size
        if final_confidence > 0.7:
            position_size = 3.0  # Increase for stronger signals
        elif final_confidence < 0.6:
            position_size = 1.0  # Decrease for weaker signals
        
        return PersonaEntryRecommendation(
            persona_name="Cosmic Trader",
            confidence=final_confidence,
            side=side,
            target_price=current_price,
            reasons=reasons,
            risk_level="balanced",
            time_horizon="universal",
            explanation=explanation,
            trap_awareness=0.9,  # Cosmic traders have excellent trap awareness
            position_size=position_size,
            stop_loss=stop_loss,
            take_profit=take_profit,
            color_code=Colors.PURPLE,
            action=action
        )
    
    def format_recommendations_display(self, entry_strategy: PersonaBasedEntryStrategy) -> str:
        """
        Format entry recommendations for display.
        
        Args:
            entry_strategy: PersonaBasedEntryStrategy with recommendations
            
        Returns:
            Formatted string for display
        """
        output = []
        
        # Add market information
        output.append(f"\nMarket: {entry_strategy.market_symbol}")
        output.append(f"Current Price: {entry_strategy.current_price}")
        
        # Add summary
        output.append(f"\n🧠 PERSONA-BASED RECOMMENDATIONS:")
        output.append(f"  {entry_strategy.summary}")
        
        # Group recommendations by action type
        entry_recs = [r for r in entry_strategy.recommendations if r.action == "ENTER"]
        wait_recs = [r for r in entry_strategy.recommendations if r.action == "WAIT"]
        
        # Sort by confidence (highest first)
        entry_recs.sort(key=lambda r: r.confidence, reverse=True)
        wait_recs.sort(key=lambda r: r.confidence, reverse=True)
        
        if entry_recs or wait_recs:
            output.append("\nALL PERSONA OPINIONS:")
        
        # Display Entry recommendations
        if entry_recs:
            output.append("\nEntry Recommendations:")
            for rec in entry_recs:
                # Create confidence bar (10 chars wide)
                conf_bar = "█" * int(rec.confidence * 10) + "░" * (10 - int(rec.confidence * 10))
                
                output.append(f"  {self.colorize(rec.persona_name, rec.color_code)} ({rec.confidence:.2f}) - {rec.side.upper()}:")
                output.append(f"    {self.colorize(conf_bar, rec.color_code)}")
                output.append(f"    Reasons: {', '.join(rec.reasons)}")
                output.append(f"    Approach: {rec.risk_level.capitalize()} risk, {rec.time_horizon} horizon")
                output.append(f"    → {rec.explanation}")
                output.append(f"    Position Size: {rec.position_size:.1f}% | Stop Loss: {rec.stop_loss:.1f} | Take Profit: {rec.take_profit:.1f}")
                output.append("")
        
        # Display Wait recommendations
        if wait_recs:
            output.append("\nWait Recommendations:")
            for rec in wait_recs:
                # Create confidence bar (10 chars wide)
                conf_bar = "█" * int(rec.confidence * 10) + "░" * (10 - int(rec.confidence * 10))
                
                output.append(f"  {self.colorize(rec.persona_name, rec.color_code)} ({rec.confidence:.2f}):")
                output.append(f"    {self.colorize(conf_bar, rec.color_code)}")
                output.append(f"    Reasons: {', '.join(rec.reasons)}")
                output.append(f"    → {rec.explanation}")
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
    print(persona_manager.format_recommendations_display(entry_strategy))

if __name__ == "__main__":
    demo() 