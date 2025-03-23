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

try:
    from pybitget import Spot  # Import BitGet SDK
except ImportError:
    print("⚠️ BitGet SDK not found. Please install it with: pip install pybitget")
    print("For now, using mock data only.")

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
        """Generate entry recommendation from Cosmic Trader persona."""
        symbol = market_data["symbol"]
        
        # Get current time for cosmic analysis
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()  # 0-6 (Monday-Sunday)
        day_of_month = now.day
        month = now.month
        
        # Determine moon phase (simplified calculation)
        # This is a simplified approach - in production we could use an astronomy API
        days_since_new_moon = (now.date() - datetime(2024, 2, 9).date()).days % 29.53  # Feb 9, 2024 was a new moon
        if days_since_new_moon < 7.38:
            moon_phase = "waxing crescent"
            cosmic_confidence_adj = 0.2  # Growing energy, good for entries
        elif days_since_new_moon < 14.76:
            moon_phase = "waxing gibbous"
            cosmic_confidence_adj = 0.3  # Strong energy, very good for entries
        elif days_since_new_moon < 21.76:
            moon_phase = "waning gibbous"
            cosmic_confidence_adj = -0.1  # Declining energy, less favorable
        else:
            moon_phase = "waning crescent"
            cosmic_confidence_adj = -0.2  # Low energy, poor for entries
            
        # Day of week influence
        if day_of_week in [1, 4]:  # Tuesday and Friday have historically positive energy
            dow_influence = 0.15
        elif day_of_week in [2, 5]:  # Wednesday and Saturday have neutral energy
            dow_influence = 0.0
        else:  # Monday, Thursday, Sunday have historically negative energy
            dow_influence = -0.1
            
        # Hour of day influence (certain trading hours align with cosmic energy)
        if 8 <= hour <= 11:  # Morning alignment
            hour_influence = 0.1
        elif 14 <= hour <= 16:  # Afternoon alignment
            hour_influence = 0.15
        elif 19 <= hour <= 22:  # Evening alignment
            hour_influence = 0.05
        else:  # Nighttime/early morning - low cosmic energy
            hour_influence = -0.15
            
        # Analyze Fibonacci alignment
        fib_alignment = 0.0
        
        # Check if price is near Fibonacci level from recent high/low range
        if "recent_high" in market_data and "recent_low" in market_data:
            recent_high = market_data["recent_high"]
            recent_low = market_data["recent_low"]
            range_size = recent_high - recent_low
            
            if range_size > 0:
                # Calculate key Fibonacci levels
                fib_levels = {
                    0.236: recent_low + (range_size * 0.236),
                    0.382: recent_low + (range_size * 0.382),
                    0.5: recent_low + (range_size * 0.5),
                    0.618: recent_low + (range_size * 0.618),
                    0.786: recent_low + (range_size * 0.786),
                    0.888: recent_low + (range_size * 0.888)
                }
                
                # Check if price is near any Fibonacci level
                for level, price in fib_levels.items():
                    # If price is within 0.5% of a Fibonacci level
                    if current_price > 0 and abs(current_price - price) / current_price < 0.005:
                        # Golden ratio and its derivatives have highest cosmic significance
                        if level in [0.618, 0.382]:
                            fib_alignment = 0.4
                        elif level == 0.5:  # Square root alignment
                            fib_alignment = 0.3
                        else:
                            fib_alignment = 0.2
                        break
        
        # Combine cosmic factors
        cosmic_confidence = cosmic_confidence_adj + dow_influence + hour_influence + fib_alignment
        
        # Calculate cosmic risk appetite based on moon phase
        cosmic_risk_appetite = {
            "waxing crescent": 0.1,  # Growing energy - moderate risk
            "waxing gibbous": 0.2,   # Peak energy - higher risk tolerance
            "waning gibbous": -0.1,  # Declining energy - reduce risk
            "waning crescent": -0.2  # Low energy - very low risk tolerance
        }[moon_phase]
        
        # Calculate final confidence
        final_confidence = max(0.0, min(1.0, cosmic_confidence + cosmic_risk_appetite))
        
        # Determine if we should enter or wait
        action = "ENTER" if final_confidence >= self.min_confidence else "WAIT"
        
        # Determine entry side based on cosmic alignment
        # In a comprehensive system, this would use more factors
        side = "long"  # Default
        if "change_24h" in market_data:
            change_24h = market_data["change_24h"]
            # If 24h change is negative but we have strong cosmic alignment, this 
            # could be a reversal opportunity for long
            if change_24h < -1.0 and final_confidence > 0.65:
                side = "long"  # Potential reversal
            # If 24h change is positive but cosmic alignment is weakening,
            # consider a short position
            elif change_24h > 2.0 and final_confidence < 0.4:
                side = "short"
        
        # Generate cosmic analysis details for explanation
        analysis_details = [
            f"Moon phase: {moon_phase}",
            f"Day of week: {day_of_week}",
            f"Hour: {hour}"
        ]
        
        if fib_alignment > 0:
            analysis_details.append(f"Price aligned with Fibonacci level")
            
        # Generate explanation
        explanation = f"Cosmic confidence: {cosmic_confidence:.2f} + cosmic risk appetite: {cosmic_risk_appetite:.2f} = final: {final_confidence:.2f}"
        
        # Generate reasons
        if action == "ENTER":
            reasons = ["Cosmic conditions are favorable for entry"]
            if fib_alignment > 0:
                reasons.append(f"Price is aligned with sacred Fibonacci level")
            if moon_phase in ["waxing crescent", "waxing gibbous"]:
                reasons.append(f"Waxing moon provides positive energy for new positions")
            if cosmic_risk_appetite > 0:
                reasons.append(f"Celestial risk appetite supports position taking")
                
            # If confidence is very high, add more spiritual reasoning
            if final_confidence > 0.7:
                reasons.append("Strong universal alignment supports this entry")
        else:
            reasons = ["Cosmic conditions not optimal"]
            reasons.append(f"→ Current moon phase: {moon_phase}, day: {'weekend' if day_of_week >= 5 else 'weekday'}, hour: {'morning' if hour < 12 else 'evening' if hour >= 18 else 'afternoon'}")
            
            if cosmic_risk_appetite < 0:
                reasons.append("→ Celestial risk appetite is low")
                
            if fib_alignment <= 0:
                reasons.append("→ Price not aligned with sacred Fibonacci levels")
        
        # Set target price slightly above current for long, below for short
        adjustment = 0.01  # 1% adjustment
        target_price = current_price * (1 + adjustment) if side == "long" else current_price * (1 - adjustment)
        
        # More conservative stop loss for cosmic trader
        stop_loss = current_price * (1 - 0.05) if side == "long" else current_price * (1 + 0.05)
        
        # Take profit aligned with Fibonacci extensions
        take_profit = current_price * (1 + 0.118) if side == "long" else current_price * (1 - 0.118)  # 11.8% is 0.618 * 0.382 * 50
        
        # Return recommendation
        return PersonaEntryRecommendation(
            persona_name="Cosmic Trader",
            confidence=final_confidence,
            side=side,
            target_price=target_price,
            reasons=reasons,
            risk_level="moderate",
            time_horizon="medium-term",
            explanation=explanation,
            trap_awareness=0.7,  # Cosmic trader has higher trap awareness due to universal perspective
            position_size=0.03,  # Conservative position size
            stop_loss=stop_loss,
            take_profit=take_profit,
            action=action
        )
    
    def format_recommendations_display(self, recommendations: List[PersonaEntryRecommendation], 
                                     symbol: str = "Unknown", current_price: float = 0.0) -> str:
        """Format the entry recommendations into a human-readable display."""
        if not recommendations:
            return "No recommendations available."
            
        # Get the market from the trading pair or use provided symbol
        market = symbol
        
        # Calculate how many personas recommend entry
        entry_recommendations = [rec for rec in recommendations if rec.action == "ENTER"]
        wait_recommendations = [rec for rec in recommendations if rec.action == "WAIT"]
        
        # Sort by confidence level (descending)
        entry_recommendations.sort(key=lambda x: x.confidence, reverse=True)
        wait_recommendations.sort(key=lambda x: x.confidence, reverse=True)
        
        # Generate header
        header = f"\nMarket: {market}\nCurrent Price: {current_price:.2f}\n"
        
        # Generate summary section
        summary = "\n🧠 PERSONA-BASED RECOMMENDATIONS:"
        
        if entry_recommendations:
            best_persona = entry_recommendations[0].persona_name
            entry_count = len(entry_recommendations)
            if entry_count > 1:
                other_count = entry_count - 1
                summary += f"\n  {self.colorize(Colors.GREEN, f'ENTRY SIGNAL: {entry_count} personas recommend entry, led by {best_persona}')} "
                summary += f"({other_count} other{'s' if other_count > 1 else ''})"
            else:
                summary += f"\n  {self.colorize(Colors.GREEN, f'ENTRY SIGNAL: {best_persona} recommends entry')}"
        else:
            summary += f"\n  {self.colorize(Colors.RESET, 'NO ENTRY SIGNAL: ')}"\
                      f"{len(wait_recommendations)} personas recommend waiting"
        
        # Generate detailed section
        details = "\n\nALL PERSONA OPINIONS:\n"
        
        # Format entry recommendations
        if entry_recommendations:
            details += "\nEntry Recommendations:\n"
            for rec in entry_recommendations:
                details += self._format_single_recommendation(rec)
        
        # Format wait recommendations
        if wait_recommendations:
            details += "\nWait Recommendations:\n"
            for rec in wait_recommendations:
                details += self._format_single_recommendation(rec)
        
        return header + summary + details
        
    def _format_single_recommendation(self, rec: PersonaEntryRecommendation) -> str:
        """Format a single recommendation for display."""
        # Create confidence bar (10 chars wide)
        conf_val = max(0, min(1, rec.confidence))  # Ensure 0-1 range
        conf_bar = "█" * int(conf_val * 10) + "░" * (10 - int(conf_val * 10))
        
        # Build the formatted output
        output = []
        
        # Persona name and confidence
        if rec.action == "ENTER":
            color = Colors.GREEN
            output.append(f"  {self.colorize(color, rec.persona_name)} ({rec.confidence:.2f}) - {rec.side.upper()}:")
        else:
            color = Colors.RESET
            output.append(f"  {self.colorize(color, rec.persona_name)} ({rec.confidence:.2f}):")
            
        # Confidence bar
        output.append(f"    {conf_bar}")
        
        # Reasons
        if hasattr(rec, 'reasons') and rec.reasons:
            output.append(f"    Reasons: {', '.join(rec.reasons)}")
            
        # Explanation
        if hasattr(rec, 'explanation') and rec.explanation:
            output.append(f"    → {rec.explanation}")
            
        # Additional details for entry recommendations
        if rec.action == "ENTER":
            if hasattr(rec, 'risk_level') and hasattr(rec, 'time_horizon'):
                output.append(f"    Approach: {rec.risk_level.capitalize()} risk, {rec.time_horizon} horizon")
                
            if hasattr(rec, 'position_size') and hasattr(rec, 'stop_loss') and hasattr(rec, 'take_profit'):
                output.append(f"    Position Size: {rec.position_size:.2f}% | Stop Loss: {rec.stop_loss:.1f} | Take Profit: {rec.take_profit:.1f}")
                
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
    Run the persona entry strategy monitor continuously.
    
    Args:
        interval (int): Interval between checks in seconds.
        min_confidence (float): Minimum confidence threshold for recommendations.
        use_color (bool): Whether to use color in output.
        use_mock (bool): Whether to use mock market data instead of real market data.
    """
    print(f"Starting Persona Entry Monitor")
    print(f"Interval: {interval} seconds")
    print(f"Minimum confidence: {min_confidence}")
    print(f"{'Using mock data' if use_mock else 'Using real BitGet data'}")
    print(f"Press Ctrl+C to stop\n")
    
    # Initialize entry manager
    manager = PersonaEntryManager(min_confidence=min_confidence, use_color=use_color)
    
    # Set up symbols to monitor
    symbols = ["BTCUSDT", "ETHUSDT"]
    
    try:
        while True:
            print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Analyzing markets...")
            
            for symbol in symbols:
                # Get market data
                if use_mock:
                    market_data = get_mock_market_data(symbol)
                else:
                    market_data = get_real_market_data(symbol)
                    
                if market_data:
                    # Get entry recommendations
                    manager.analyze_market(market_data)
                else:
                    print(f"❌ Failed to get market data for {symbol}")
            
            # Sleep until next check
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nPersona Entry Monitor stopped by user.")

def get_mock_market_data(symbol="BTCUSDT"):
    """
    Generate mock market data for testing.
    In a real implementation, this would fetch data from an exchange API.
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

def get_real_market_data(symbol="BTCUSDT"):
    """
    Fetch real market data from BitGet API.
    """
    # Check if BitGet SDK is available
    if 'Spot' not in globals():
        print("❌ BitGet SDK not available. Install with: pip install pybitget")
        print("Falling back to mock data...")
        return get_mock_market_data(symbol)
        
    try:
        # Initialize BitGet client
        api_key = os.environ.get('BITGET_API_KEY')
        api_secret = os.environ.get('BITGET_SECRET_KEY')
        api_passphrase = os.environ.get('BITGET_PASSPHRASE')
        
        if not api_key or not api_secret or not api_passphrase:
            print("⚠️ BitGet API credentials not found. Make sure to set BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE environment variables.")
            return get_mock_market_data(symbol)
        
        client = Spot(api_key=api_key, api_secret=api_secret, passphrase=api_passphrase)
        
        # Fetch current market data
        ticker = client.market_ticker(symbol=symbol)
        
        # Fetch klines (candlesticks) for recent high/low and Fibonacci analysis
        # Get last 24 hours of 15-minute klines
        klines = []
        try:
            klines = client.market_candles(
                symbol=symbol,
                granularity="15m",
                startTime=int((time.time() - 86400) * 1000),  # 24 hours ago
                endTime=int(time.time() * 1000)               # Now
            )
        except Exception as e:
            print(f"⚠️ Error fetching klines: {e}")
        
        # Process kline data for high and low
        recent_high = 0
        recent_low = float('inf')
        
        if klines and len(klines) > 0:
            for kline in klines:
                high = float(kline[2])
                low = float(kline[3])
                recent_high = max(recent_high, high)
                recent_low = min(recent_low, low)
        else:
            # Fallback if klines are not available
            recent_high = float(ticker.get('high24h', 0)) 
            recent_low = float(ticker.get('low24h', 0))
        
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
            "change_24h": float(ticker.get('change24h', 0)),
            "volume": float(ticker.get('baseVolume', 0)),
            "avg_volume": float(ticker.get('baseVolume', 0)),  # Using current volume as avg for now
            "high_24h": float(ticker.get('high24h', 0)),
            "low_24h": float(ticker.get('low24h', 0)),
            "recent_high": recent_high,  # For Fibonacci analysis
            "recent_low": recent_low,    # For Fibonacci analysis
            "timestamp": int(time.time())
        }
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        print("Falling back to mock data...")
        return get_mock_market_data(symbol)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - Persona-Based Entry Strategy")
    parser.add_argument("--continuous", action="store_true", help="Run the monitor continuously")
    parser.add_argument("--interval", type=int, default=60, help="Interval between checks in seconds")
    parser.add_argument("--min-confidence", type=float, default=0.5, help="Minimum confidence threshold for recommendations")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--mock", action="store_true", help="Use mock market data")
    args = parser.parse_args()
    
    # Load environment variables from .env file if present
    if os.path.exists(".env"):
        load_dotenv()
    
    # Run the monitor
    if args.continuous:
        run_continuous_monitor(
            interval=args.interval,
            min_confidence=args.min_confidence,
            use_color=not args.no_color,
            use_mock=args.mock
        )
    else:
        # Single run
        manager = PersonaEntryManager(min_confidence=args.min_confidence, use_color=not args.no_color)
        
        # Analyze BTC and ETH markets
        symbols = ["BTCUSDT", "ETHUSDT"]
        
        print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Analyzing markets...")
        
        for symbol in symbols:
            # Get market data
            if args.mock:
                market_data = get_mock_market_data(symbol)
            else:
                market_data = get_real_market_data(symbol)
                
            if market_data:
                # Get entry recommendations
                manager.analyze_market(market_data)
            else:
                print(f"❌ Failed to get market data for {symbol}") 