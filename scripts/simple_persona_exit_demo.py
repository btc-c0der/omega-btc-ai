#!/usr/bin/env python3
"""
OMEGA BTC AI - Simplified Persona-Based Exit Strategy Demo
========================================================

This script demonstrates the concept of persona-based exit recommendations
without requiring the full OMEGA BTC AI infrastructure.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import time
import json
import random
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
class PersonaExitRecommendation:
    """Exit recommendation from a specific trader persona."""
    persona_name: str
    confidence: float  # 0.0 to 1.0
    price: float
    reasons: List[str]
    risk_level: str  # "conservative", "moderate", "aggressive"
    time_horizon: str  # "immediate", "short-term", "long-term"
    explanation: str
    trap_awareness: float  # 0.0 to 1.0
    color_code: str = Colors.YELLOW
    action: str = "EXIT"  # "EXIT" or "HODL"

    def __post_init__(self):
        # Set color based on confidence and action
        if self.action == "HODL":
            self.color_code = Colors.BLUE
        elif self.confidence >= 0.8:
            self.color_code = Colors.GREEN
        elif self.confidence >= 0.5:
            self.color_code = Colors.YELLOW
        else:
            self.color_code = Colors.RED

@dataclass
class PersonaBasedExitStrategy:
    """Collection of exit recommendations from different trader personas."""
    position_symbol: str
    position_side: str
    current_price: float
    entry_price: float
    pnl_percent: float
    recommendations: List[PersonaExitRecommendation] = field(default_factory=list)
    all_recommendations: Dict[str, PersonaExitRecommendation] = field(default_factory=dict)
    summary: str = ""
    
    def add_recommendation(self, recommendation: PersonaExitRecommendation) -> None:
        """Add a persona-based recommendation."""
        self.recommendations.append(recommendation)
        
    def get_average_confidence(self) -> float:
        """Get the average confidence across all recommendations."""
        if not self.recommendations:
            return 0.0
        return sum(r.confidence for r in self.recommendations) / len(self.recommendations)
    
    def get_highest_confidence_recommendation(self) -> Optional[PersonaExitRecommendation]:
        """Get the recommendation with the highest confidence."""
        if not self.recommendations:
            return None
        return max(self.recommendations, key=lambda r: r.confidence)
    
    def generate_summary(self) -> str:
        """Generate a summary of all recommendations."""
        if not self.recommendations:
            return "No exit recommendations available."
        
        avg_confidence = self.get_average_confidence()
        high_conf_rec = self.get_highest_confidence_recommendation()
        
        if avg_confidence >= 0.7:
            summary = f"STRONG EXIT SIGNAL: {len(self.recommendations)} personas recommend exiting"
            if high_conf_rec:
                summary += f", led by {high_conf_rec.persona_name} ({high_conf_rec.confidence:.2f})"
        elif avg_confidence >= 0.5:
            summary = f"MODERATE EXIT SIGNAL: Mixed recommendations from {len(self.recommendations)} personas"
        else:
            summary = f"WEAK EXIT SIGNAL: {len(self.recommendations)} personas with low confidence"
        
        # Add PnL context
        if self.pnl_percent >= 5.0:
            summary += f" - Currently in strong profit ({self.pnl_percent:.2f}%)"
        elif self.pnl_percent >= 1.0:
            summary += f" - Currently in profit ({self.pnl_percent:.2f}%)"
        elif self.pnl_percent <= -5.0:
            summary += f" - Currently in significant loss ({self.pnl_percent:.2f}%)"
        elif self.pnl_percent < 0:
            summary += f" - Currently in loss ({self.pnl_percent:.2f}%)"
        else:
            summary += f" - Position near breakeven ({self.pnl_percent:.2f}%)"
            
        self.summary = summary
        return summary

class PersonaExitManager:
    """Manages exit recommendations from different trader personas."""
    
    def __init__(self, min_confidence: float = 0.5, use_color: bool = True, continuous_mode: bool = False):
        """
        Initialize the persona-based exit recommendation system.
        
        Args:
            min_confidence: Minimum confidence threshold for exit recommendations
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
        
        print(f"Initialized PersonaExitManager with {len(self.trader_personas)} trader personas")
    
    def colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.use_color:
            return f"{color}{text}{Colors.END}"
        return text
    
    def get_bitget_positions(self):
        """Fetch and return BitGet positions"""
        # Update last fetch time
        self.last_fetch_time = datetime.now()
        
        # Get API credentials from environment
        api_key = os.getenv("BITGET_API_KEY", "")
        secret_key = os.getenv("BITGET_SECRET_KEY", "")
        passphrase = os.getenv("BITGET_PASSPHRASE", "")
        
        # Verify API credentials
        if not api_key or not secret_key or not passphrase:
            print(f"{Colors.RED}Missing BitGet API credentials in environment variables{Colors.END}")
            return {"error": "Missing credentials"}
        
        # Create direct CCXT BitGet client
        try:
            import ccxt
            
            # Create the exchange client
            exchange = ccxt.bitget({
                'apiKey': api_key,
                'secret': secret_key,
                'password': passphrase,
                'options': {
                    'defaultType': 'swap',
                }
            })
            
            # Fetch positions
            # Note: ccxt provides fetchPositions but linter might not recognize it
            positions = exchange.fetchPositions()  # type: ignore
            
            # Filter out positions with zero contracts
            active_positions = [p for p in positions if float(p.get('contracts', 0)) > 0]
            
            # Convert to format expected by this app
            formatted_positions = []
            for position in active_positions:
                # Get position details with proper type conversion
                symbol_raw = position.get('symbol', '')
                symbol = symbol_raw.split(':')[0] if ':' in symbol_raw else symbol_raw  # Remove :USDT suffix
                side = str(position.get('side', 'long')).lower()
                entry_price = float(position.get('entryPrice', 0))
                current_price = float(position.get('markPrice', 0))
                size = float(position.get('contracts', 0))
                leverage = float(position.get('leverage', 1))
                
                formatted_positions.append({
                    'symbol': symbol,
                    'side': side,
                    'entry_price': entry_price,
                    'current_price': current_price,
                    'size': size,
                    'leverage': leverage
                })
            
            return {
                "success": True,
                "positions": formatted_positions,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "connection": "CONNECTED TO BITGET MAINNET"
            }
            
        except ImportError:
            print(f"{Colors.RED}ccxt module not installed{Colors.END}")
            return {"error": "ccxt module not installed"}
        except Exception as e:
            print(f"{Colors.RED}An error occurred: {str(e)}{Colors.END}")
            return {"error": str(e)}
    
    def generate_exit_recommendations(self, position: Dict[str, Any]) -> PersonaBasedExitStrategy:
        """
        Generate exit recommendations from different trader personas.
        
        Args:
            position: Position data
            
        Returns:
            PersonaBasedExitStrategy with recommendations from different personas
        """
        # Extract position details
        symbol = position.get('symbol', 'BTCUSDT')
        side = position.get('side', 'long').lower()
        entry_price = float(position.get('entry_price', 45000))
        current_price = float(position.get('current_price', 45500))
        
        # Calculate PnL percentage
        if side == 'long':
            pnl_percent = ((current_price - entry_price) / entry_price) * 100
        else:  # short
            pnl_percent = ((entry_price - current_price) / entry_price) * 100
            
        # Create exit strategy object
        exit_strategy = PersonaBasedExitStrategy(
            position_symbol=symbol,
            position_side=side,
            current_price=current_price,
            entry_price=entry_price,
            pnl_percent=pnl_percent
        )
        
        # Generate recommendations from each persona - store all recommendations
        all_recommendations = {}
        exit_recommendations = []
        
        for persona_name in self.trader_personas:
            recommendation = self._get_persona_recommendation(
                persona_name, position, current_price, entry_price, pnl_percent
            )
            
            if recommendation:
                if recommendation.confidence >= self.min_confidence:
                    # This meets our threshold for an exit recommendation
                    exit_recommendations.append(recommendation)
                
                # Store all recommendations for display
                all_recommendations[persona_name] = recommendation
            else:
                # Generate a HODL recommendation if no exit recommendation was given
                all_recommendations[persona_name] = self._create_hodl_recommendation(
                    persona_name, symbol, side, current_price, entry_price, pnl_percent
                )
        
        # Add all exit recommendations that meet confidence threshold
        for rec in exit_recommendations:
            exit_strategy.add_recommendation(rec)
            
        # Store all recommendations (including HODL) for display
        exit_strategy.all_recommendations = all_recommendations
        
        # Generate summary
        exit_strategy.generate_summary()
        
        # In continuous mode, check for changes from previous recommendations
        if self.continuous_mode:
            position_key = f"{symbol}_{side}"
            is_changed = self._detect_recommendation_changes(position_key, exit_strategy)
            
            # Store for future comparison
            self.previous_recommendations[position_key] = exit_strategy
            
            # If recommendations changed, possibly send notifications here
            if is_changed:
                self._handle_recommendation_changes(position_key, exit_strategy)
        
        return exit_strategy
    
    def _detect_recommendation_changes(self, position_key: str, current: PersonaBasedExitStrategy) -> bool:
        """
        Detect changes in recommendations for continuous monitoring.
        
        Args:
            position_key: String identifier for the position
            current: Current exit strategy recommendations
            
        Returns:
            True if significant changes detected
        """
        if position_key not in self.previous_recommendations:
            return True  # First time seeing this position
            
        previous = self.previous_recommendations[position_key]
        
        # Check if average confidence changed significantly
        prev_conf = previous.get_average_confidence()
        curr_conf = current.get_average_confidence()
        
        # Check if new personas are recommending exit
        prev_personas = set(r.persona_name for r in previous.recommendations)
        curr_personas = set(r.persona_name for r in current.recommendations)
        
        # Significant change if:
        # 1. Confidence changed by more than 15%
        # 2. New personas recommending exit
        # 3. Previously recommending personas no longer recommend exit
        if abs(prev_conf - curr_conf) > 0.15:
            return True
        if len(curr_personas - prev_personas) > 0:
            return True
        if len(prev_personas - curr_personas) > 0:
            return True
            
        return False
    
    def _handle_recommendation_changes(self, position_key: str, strategy: PersonaBasedExitStrategy) -> None:
        """
        Handle detected changes in recommendations.
        
        Args:
            position_key: String identifier for the position
            strategy: Current exit strategy recommendations
        """
        # Here you could implement notifications, logging, etc.
        # For now, just highlight the change in the console
        if strategy.get_average_confidence() >= 0.7:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🔔 SIGNIFICANT RECOMMENDATION CHANGE: {position_key}{Colors.END}")
            print(f"{Colors.YELLOW}{strategy.summary}{Colors.END}\n")
    
    def _get_persona_recommendation(
        self,
        persona_name: str,
        position: Dict[str, Any],
        current_price: float,
        entry_price: float,
        pnl_percent: float
    ) -> Optional[PersonaExitRecommendation]:
        """
        Get exit recommendation from a specific trader persona.
        
        Args:
            persona_name: Name of the trader persona
            position: Position data
            current_price: Current market price
            entry_price: Entry price of the position
            pnl_percent: Percentage profit/loss
            
        Returns:
            PersonaExitRecommendation if the persona recommends exiting
        """
        symbol = position.get('symbol', 'BTCUSDT')
        side = position.get('side', 'long').lower()
        
        # Each persona has different exit criteria
        if persona_name == "strategic":
            return self._get_strategic_exit(symbol, side, current_price, entry_price, pnl_percent)
        elif persona_name == "aggressive":
            return self._get_aggressive_exit(symbol, side, current_price, entry_price, pnl_percent)
        elif persona_name == "newbie":
            return self._get_newbie_exit(symbol, side, current_price, entry_price, pnl_percent)
        elif persona_name == "scalper":
            return self._get_scalper_exit(symbol, side, current_price, entry_price, pnl_percent)
        elif persona_name == "cosmic":
            return self._get_cosmic_exit(symbol, side, current_price, entry_price, pnl_percent)
        
        return None
    
    def _get_strategic_exit(
        self, 
        symbol: str, 
        side: str, 
        current_price: float, 
        entry_price: float, 
        pnl_percent: float
    ) -> Optional[PersonaExitRecommendation]:
        """Get exit recommendation from Strategic Trader persona."""
        confidence = 0.0
        reasons = []
        explanation = ""
        
        # Strategic traders focus on significant profits and market structure
        if side == "long":
            # Strong profit - strategic traders take significant wins
            if pnl_percent >= 15.0:
                confidence = 0.9
                reasons.append("Significant profit achieved")
                explanation = "Strategic approach suggests securing substantial profits to maintain positive risk-reward ratio."
            # Moderate profit with potential resistance
            elif pnl_percent >= 8.0:
                confidence = 0.75
                reasons.append("Approaching key resistance level")
                explanation = "Price approaching key technical resistance level, consider securing profits or partial exit."
            # Small loss - strategic traders cut losses
            elif pnl_percent <= -5.0:
                confidence = 0.85
                reasons.append("Stop loss reached")
                explanation = "Strategic risk management suggests exiting to preserve capital."
        else:  # short
            # Strong profit for short
            if pnl_percent >= 15.0:
                confidence = 0.9
                reasons.append("Significant profit achieved")
                explanation = "Strategic approach suggests securing substantial profits to maintain positive risk-reward ratio."
            # Moderate profit with potential support
            elif pnl_percent >= 8.0:
                confidence = 0.75
                reasons.append("Approaching key support level")
                explanation = "Price approaching key technical support level, consider securing profits or partial exit."
            # Small loss - strategic traders cut losses
            elif pnl_percent <= -5.0:
                confidence = 0.85
                reasons.append("Stop loss reached")
                explanation = "Strategic risk management suggests exiting to preserve capital."
        
        if not reasons:
            return None
            
        return PersonaExitRecommendation(
            persona_name="Strategic Trader",
            confidence=confidence,
            price=current_price,
            reasons=reasons,
            risk_level="conservative",
            time_horizon="short-term",
            explanation=explanation,
            trap_awareness=0.8  # Strategic traders have high trap awareness
        )
    
    def _get_aggressive_exit(
        self, 
        symbol: str, 
        side: str, 
        current_price: float, 
        entry_price: float, 
        pnl_percent: float
    ) -> Optional[PersonaExitRecommendation]:
        """Get exit recommendation from Aggressive Trader persona."""
        confidence = 0.0
        reasons = []
        explanation = ""
        
        # Aggressive traders take quick profits and ride big winners
        if side == "long":
            # Very large profit - aggressive traders might ride even higher
            if pnl_percent >= 25.0:
                confidence = 0.6  # Lower confidence to exit - might want to ride higher
                reasons.append("Significant profit achieved, but potential for more")
                explanation = "Consider partial profit taking while keeping runner position."
            # Good profit - quick exit to secure gains
            elif pnl_percent >= 5.0:
                confidence = 0.8
                reasons.append("Quick profit target reached")
                explanation = "Aggressive strategy suggests taking quick profits and looking for next opportunity."
            # Big loss - aggressive traders might hold longer hoping for reversal
            elif pnl_percent <= -10.0:
                confidence = 0.75
                reasons.append("Major loss - consider exit")
                explanation = "Position showing significant loss, consider cutting to preserve capital."
        else:  # short
            # Very large profit - aggressive traders might ride even higher
            if pnl_percent >= 25.0:
                confidence = 0.6  # Lower confidence to exit - might want to ride higher
                reasons.append("Significant profit achieved, but potential for more")
                explanation = "Consider partial profit taking while keeping runner position."
            # Good profit - quick exit to secure gains
            elif pnl_percent >= 5.0:
                confidence = 0.8
                reasons.append("Quick profit target reached")
                explanation = "Aggressive strategy suggests taking quick profits and looking for next opportunity."
            # Big loss - aggressive traders might hold longer hoping for reversal
            elif pnl_percent <= -10.0:
                confidence = 0.75
                reasons.append("Major loss - consider exit")
                explanation = "Position showing significant loss, consider cutting to preserve capital."
        
        if not reasons:
            return None
            
        return PersonaExitRecommendation(
            persona_name="Aggressive Trader",
            confidence=confidence,
            price=current_price,
            reasons=reasons,
            risk_level="aggressive",
            time_horizon="immediate",
            explanation=explanation,
            trap_awareness=0.5  # Aggressive traders have moderate trap awareness
        )
    
    def _get_newbie_exit(
        self, 
        symbol: str, 
        side: str, 
        current_price: float, 
        entry_price: float, 
        pnl_percent: float
    ) -> Optional[PersonaExitRecommendation]:
        """Get exit recommendation from Newbie Trader persona."""
        confidence = 0.0
        reasons = []
        explanation = ""
        
        # Newbie traders often exit too early on profits and too late on losses
        if side == "long":
            # Small profit - newbies often take profits too early
            if pnl_percent >= 2.0:
                confidence = 0.85
                reasons.append("Small profit achieved")
                explanation = "Taking small profits may feel safe but reduces long-term profitability."
            # Small loss - newbies might hold too long
            elif pnl_percent <= -2.0:
                confidence = 0.4  # Low confidence to exit - tendency to hold losses
                reasons.append("Small loss developing")
                explanation = "While tempting to hold for recovery, cutting losses early is often better strategy."
            # Big loss - newbies still reluctant to exit
            elif pnl_percent <= -15.0:
                confidence = 0.6  # Still reluctant to exit
                reasons.append("Major loss - emotional difficulty exiting")
                explanation = "Despite significant loss, newbies struggle to accept and exit losing positions."
        else:  # short
            # Small profit - newbies often take profits too early
            if pnl_percent >= 2.0:
                confidence = 0.85
                reasons.append("Small profit achieved")
                explanation = "Taking small profits may feel safe but reduces long-term profitability."
            # For short positions, newbies are often more nervous about any loss
            # and might exit sooner than with longs
            elif pnl_percent <= -0.3:  # Much lower threshold than for longs
                confidence = 0.55  # Higher confidence to exit shorts at small loss
                reasons.append("Short position showing loss - newbie anxiety")
                explanation = "Newbies tend to be more nervous with short positions and may exit sooner than with longs."
            # Big loss - newbies still reluctant to exit
            elif pnl_percent <= -10.0:
                confidence = 0.7  # More likely to exit big loss shorts than longs
                reasons.append("Major loss - emotional difficulty exiting")
                explanation = "Despite significant loss, newbies struggle to accept and exit losing positions."
        
        if not reasons:
            return None
            
        return PersonaExitRecommendation(
            persona_name="Newbie Trader",
            confidence=confidence,
            price=current_price,
            reasons=reasons,
            risk_level="variable",
            time_horizon="immediate",
            explanation=explanation,
            trap_awareness=0.2  # Newbie traders have low trap awareness
        )
    
    def _get_scalper_exit(
        self, 
        symbol: str, 
        side: str, 
        current_price: float, 
        entry_price: float, 
        pnl_percent: float
    ) -> Optional[PersonaExitRecommendation]:
        """Get exit recommendation from Scalper Trader persona."""
        confidence = 0.0
        reasons = []
        explanation = ""
        
        # Scalpers take very quick, small profits and cut losses immediately
        if side == "long":
            # Even tiny profits are taken by scalpers
            if pnl_percent >= 1.0:
                confidence = 0.9
                reasons.append("Scalping profit target reached")
                explanation = "Scalping strategy demands quick profit taking on small moves."
            # Scalpers cut losses immediately
            elif pnl_percent <= -0.5:
                confidence = 0.95
                reasons.append("Scalper stop loss reached")
                explanation = "Scalping requires strict loss management - exit immediately."
        else:  # short
            # Even tiny profits are taken by scalpers
            if pnl_percent >= 1.0:
                confidence = 0.9
                reasons.append("Scalping profit target reached")
                explanation = "Scalping strategy demands quick profit taking on small moves."
            # Scalpers cut losses immediately at ANY negative PnL for short positions
            # Using a very small negative threshold to catch even tiny losses
            elif pnl_percent <= -0.2:  # Changed from -0.5 to -0.2 to be more sensitive
                confidence = 0.95
                reasons.append("Scalper stop loss reached")
                explanation = "Scalping requires strict loss management - exit immediately."
        
        if not reasons:
            return None
            
        return PersonaExitRecommendation(
            persona_name="Scalper Trader",
            confidence=confidence,
            price=current_price,
            reasons=reasons,
            risk_level="moderate",
            time_horizon="immediate",
            explanation=explanation,
            trap_awareness=0.6  # Scalpers have good trap awareness for quick moves
        )
    
    def _get_cosmic_exit(
        self, 
        symbol: str, 
        side: str, 
        current_price: float, 
        entry_price: float, 
        pnl_percent: float
    ) -> Optional[PersonaExitRecommendation]:
        """Get exit recommendation from Cosmic Trader persona based on divine market flow."""
        confidence = 0.0
        reasons = []
        explanation = ""
        
        # Get current time to determine cosmic influences
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        
        # Cosmic traders are influenced by time of day, moon cycles, and energy patterns
        
        # Determine if Mercury is retrograde (simplified simulation)
        mercury_retrograde = (now.day % 7 == 0)  # Every 7th day of month
        
        # Determine moon phase (simplified simulation)
        moon_day = now.day % 30
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
            
        # Base cosmic influences
        cosmic_risk_appetite = 0.0
        
        # Moon phase influences
        if moon_phase == "new_moon":
            cosmic_risk_appetite += 0.2  # New beginnings - more risk
            if side == "long" and pnl_percent < 0:
                cosmic_risk_appetite += 0.1  # Hold losing longs during new moon
        elif moon_phase == "full_moon":
            cosmic_risk_appetite -= 0.3  # Full moon - take profits, reduce risk
            if pnl_percent > 0:
                cosmic_risk_appetite -= 0.2  # Take profits during full moon
                
        # Mercury retrograde makes cosmic traders more cautious
        if mercury_retrograde:
            cosmic_risk_appetite -= 0.3
            if pnl_percent > 0:
                cosmic_risk_appetite -= 0.2  # Take any profits during retrograde
                
        # Time of day effects
        if hour >= 8 and hour <= 10:  # Morning market flow
            cosmic_risk_appetite += 0.1
        elif hour >= 14 and hour <= 16:  # Afternoon volatility
            cosmic_risk_appetite -= 0.1
        elif hour >= 2 and hour <= 4:  # Deep night hours - connected to universe
            cosmic_risk_appetite += 0.2
            
        # Day of week effects
        if day_of_week == 0:  # Monday - new energy
            cosmic_risk_appetite += 0.1
        elif day_of_week == 4:  # Friday - closing energy
            cosmic_risk_appetite -= 0.2
        
        # Position-specific quantum entanglement :)
        if side == "long":
            # In profit territory
            if pnl_percent >= 5.0:
                confidence = 0.8 + (0.1 * (pnl_percent / 10.0)) - cosmic_risk_appetite
                reasons.append("Significant profit energy harvested")
                explanation = "The cosmic flow indicates completion of the profit cycle. Energy should be rebalanced."
            elif pnl_percent >= 2.0 and cosmic_risk_appetite < -0.2:
                confidence = 0.7 - cosmic_risk_appetite
                reasons.append("Universal timing signals completion")
                explanation = "Cosmic cycles suggest taking profits according to universal timing."
            # In loss territory but with specific patterns
            elif pnl_percent <= -5.0:
                confidence = 0.8
                reasons.append("Energy imbalance detected")
                explanation = "Negative energy accumulation detected. Rebalance required to restore harmony."
            elif pnl_percent <= -2.0 and cosmic_risk_appetite < -0.2:
                confidence = 0.7 - cosmic_risk_appetite
                reasons.append("Disharmonious vibrations increasing")
                explanation = "The universal flow is not aligned with this position. Consider energy reallocation."
        else:  # short
            # In profit territory
            if pnl_percent >= 5.0:
                confidence = 0.8 + (0.1 * (pnl_percent / 10.0)) - cosmic_risk_appetite
                reasons.append("Negative energy cycle complete")
                explanation = "The cosmic polarity has shifted, suggesting completion of the negative cycle."
            elif pnl_percent >= 2.0 and cosmic_risk_appetite < -0.2:
                confidence = 0.7 - cosmic_risk_appetite
                reasons.append("Cosmic alignment signaling reversal")
                explanation = "The celestial alignments suggest taking profits on short energy."
            # In loss territory but with specific patterns
            elif pnl_percent <= -3.0:
                confidence = 0.8
                reasons.append("Vibrational resistance detected")
                explanation = "Universal frequencies are misaligned with this position. Realignment recommended."
            elif pnl_percent <= -1.5 and cosmic_risk_appetite < -0.2:
                confidence = 0.65 - cosmic_risk_appetite
                reasons.append("Energy field distortion increasing")
                explanation = "The harmonic resonance of the market suggests closing this position."
        
        if not reasons:
            return None
            
        return PersonaExitRecommendation(
            persona_name="Cosmic Trader",
            confidence=confidence,
            price=current_price,
            reasons=reasons,
            risk_level="balanced",
            time_horizon="universal",
            explanation=explanation,
            trap_awareness=0.9,  # Cosmic traders have excellent trap awareness
            color_code=Colors.PURPLE  # Special color for cosmic traders
        )
    
    def _create_hodl_recommendation(
        self,
        persona_name: str,
        symbol: str,
        side: str,
        current_price: float,
        entry_price: float,
        pnl_percent: float
    ) -> PersonaExitRecommendation:
        """Create a HODL recommendation when a persona doesn't recommend exit."""
        explanation = ""
        reasons = []
        risk_level = "moderate"
        time_horizon = "medium-term"
        trap_awareness = 0.5
        
        # Customize HODL recommendations based on persona
        if persona_name == "strategic":
            persona_display = "Strategic Trader"
            confidence = 0.8  # High confidence in HODL for strategic traders
            
            if side == "long":
                if pnl_percent > 0 and pnl_percent < 8.0:
                    reasons.append("Building profit - strategic targets not yet reached")
                    explanation = "Strategic approach suggests holding for larger profit targets."
                elif pnl_percent <= 0 and pnl_percent > -5.0:
                    reasons.append("Loss within acceptable range")
                    explanation = "Strategic approach allows for market fluctuations within risk parameters."
            else:  # short
                if pnl_percent > 0 and pnl_percent < 8.0:
                    reasons.append("Building profit - strategic targets not yet reached")
                    explanation = "Strategic approach suggests holding for larger profit targets."
                elif pnl_percent <= 0 and pnl_percent > -5.0:
                    reasons.append("Loss within acceptable range")
                    explanation = "Strategic approach allows for market fluctuations within risk parameters."
            
            risk_level = "conservative"
            time_horizon = "medium-term"
            trap_awareness = 0.8
            
        elif persona_name == "aggressive":
            persona_display = "Aggressive Trader"
            confidence = 0.7
            
            if pnl_percent > 0 and pnl_percent < 5.0:
                reasons.append("Building profit - expecting larger move")
                explanation = "Aggressive strategy suggests potential for significantly more profit."
            elif pnl_percent <= 0 and pnl_percent > -10.0:
                reasons.append("Potential reversal expected")
                explanation = "Aggressive approach allows for larger drawdowns expecting strong reversal."
            
            risk_level = "aggressive"
            time_horizon = "short-term"
            trap_awareness = 0.5
            
        elif persona_name == "newbie":
            persona_display = "Newbie Trader"
            confidence = 0.4  # Lower confidence for newbies
            
            if side == "long":
                if pnl_percent > 0 and pnl_percent < 2.0:
                    reasons.append("Waiting for more profit")
                    explanation = "Considering taking profits soon, but hoping for a bit more gain."
                elif pnl_percent < 0 and pnl_percent > -2.0:
                    reasons.append("Hoping for recovery")
                    explanation = "Typical newbie behavior of holding small losses hoping they'll turn to profits."
            else:  # short
                if pnl_percent > 0 and pnl_percent < 2.0:
                    reasons.append("Waiting for more profit")
                    explanation = "Considering taking profits soon, but hoping for a bit more gain."
                elif pnl_percent > -0.3:
                    reasons.append("Small loss - hoping for recovery")
                    explanation = "Typical newbie behavior of holding small losses hoping they'll turn to profits."
            
            risk_level = "variable"
            time_horizon = "uncertain"
            trap_awareness = 0.2
            
        elif persona_name == "scalper":
            persona_display = "Scalper Trader"
            confidence = 0.3  # Low confidence in holding for scalpers
            
            if side == "long":
                if pnl_percent > 0 and pnl_percent < 1.0:
                    reasons.append("Approaching scalp target")
                    explanation = "Close to profit target but not quite there. Monitor closely."
                elif pnl_percent > -0.5:
                    reasons.append("Within tight loss tolerance")
                    explanation = "Still within extremely tight scalping loss parameters, but nearing exit point."
            else:  # short
                if pnl_percent > 0 and pnl_percent < 1.0:
                    reasons.append("Approaching scalp target")
                    explanation = "Close to profit target but not quite there. Monitor closely."
                elif pnl_percent > -0.2:
                    reasons.append("Within tight loss tolerance")
                    explanation = "Still within extremely tight scalping loss parameters, but nearing exit point."
            
            risk_level = "moderate"
            time_horizon = "immediate"
            trap_awareness = 0.6
            
        elif persona_name == "cosmic":
            persona_display = "Cosmic Trader"
            
            # Get current time to determine cosmic influences
            now = datetime.now()
            hour = now.hour
            moon_day = now.day % 30
            
            # Determine moon phase (simplified)
            if moon_day < 4:  # New Moon
                moon_phase = "new_moon"
                confidence = 0.75  # High confidence in HODL during new moon
                reasons.append("New moon energy cycle building")
                explanation = "The new lunar cycle suggests patience as cosmic energies realign."
                time_horizon = "lunar-cycle"
            elif moon_day < 11:  # Waxing 
                moon_phase = "waxing"
                confidence = 0.65
                reasons.append("Energy accumulation phase")
                explanation = "Universal energies are building - alignment with position increasing."
                time_horizon = "medium-term"
            elif moon_day < 15:  # Full Moon approaching
                moon_phase = "full_approaching"
                confidence = 0.45  # Lower confidence as full moon approaches
                reasons.append("Energy peak approaching")
                explanation = "Approaching maximum energy point in lunar cycle - maintaining position to harvest."
                time_horizon = "short-term"
            elif moon_day < 19:  # Full Moon
                moon_phase = "full_moon"
                confidence = 0.3  # Low confidence during full moon
                reasons.append("Maximum energy point - vigilance required")
                explanation = "The full moon creates maximum cosmic volatility. Maintain active awareness."
                time_horizon = "immediate"
            else:  # Waning
                moon_phase = "waning"
                confidence = 0.55
                reasons.append("Releasing phase of cosmic cycle")
                explanation = "Energy is dissipating in this cycle. Patience advised as new cycles form."
                time_horizon = "medium-term"
            
            # Specific position analysis
            if side == "long":
                if pnl_percent < 0:
                    explanation += " Long positions accumulate positive energy as cycles progress."
                else:
                    explanation += " Current profit energies are still building toward optimal harvest point."
            else:  # short
                if pnl_percent < 0:
                    explanation += " Short position energies need time to align with cosmic market flow."
                else:
                    explanation += " Negative energy is still flowing in alignment with position."
            
            risk_level = "balanced"
            trap_awareness = 0.9
            
        else:
            persona_display = persona_name.capitalize()
            confidence = 0.5
            reasons.append("Position within acceptable parameters")
            explanation = "Current market conditions suggest holding this position."
        
        if not reasons:
            reasons.append("Position within acceptable parameters")
            explanation = "Current market conditions suggest holding this position."
            
        return PersonaExitRecommendation(
            persona_name=persona_display,
            confidence=confidence,
            price=current_price,
            reasons=reasons,
            risk_level=risk_level,
            time_horizon=time_horizon,
            explanation=explanation,
            trap_awareness=trap_awareness,
            action="HODL"
        )
    
    def format_recommendations_display(self, exit_strategy: PersonaBasedExitStrategy) -> str:
        """
        Format exit recommendations for display in the terminal.
        
        Args:
            exit_strategy: PersonaBasedExitStrategy with recommendations
            
        Returns:
            Formatted string for terminal display
        """
        # Header with summary
        display = f"\n{self.colorize('🧠 PERSONA-BASED RECOMMENDATIONS:', Colors.BOLD)}\n"
        
        if exit_strategy.recommendations:
            # Summary line for exit recommendations
            summary_color = Colors.GREEN if exit_strategy.get_average_confidence() >= 0.7 else Colors.YELLOW
            display += f"  {self.colorize(exit_strategy.summary, summary_color)}\n\n"
        else:
            display += f"  {self.colorize('No exit recommendations above minimum confidence threshold.', Colors.YELLOW)}\n\n"
        
        # Show all persona opinions, organized by action type
        display += f"{self.colorize('ALL PERSONA OPINIONS:', Colors.BOLD)}\n"
        
        # First display EXIT recommendations (sorted by confidence)
        exit_recs = [r for r in exit_strategy.all_recommendations.values() if r.action == "EXIT"]
        if exit_recs:
            display += f"\n{self.colorize('Exit Recommendations:', Colors.BOLD)}\n"
            
            # Sort by confidence
            for rec in sorted(exit_recs, key=lambda r: r.confidence, reverse=True):
                # Confidence indicator (visual bar)
                conf_bar = "█" * int(rec.confidence * 10)
                conf_empty = "░" * (10 - int(rec.confidence * 10))
                
                display += f"  {self.colorize(rec.persona_name, Colors.BOLD)} {self.colorize(f'({rec.confidence:.2f})', rec.color_code)}:\n"
                display += f"    {self.colorize(conf_bar, rec.color_code)}{self.colorize(conf_empty, Colors.END)}\n"
                display += f"    {self.colorize('Reasons:', Colors.CYAN)} {', '.join(rec.reasons)}\n"
                display += f"    {self.colorize('Approach:', Colors.CYAN)} {rec.risk_level.capitalize()} risk, {rec.time_horizon} horizon\n"
                display += f"    {self.colorize('→', Colors.YELLOW)} {rec.explanation}\n\n"
        
        # Then display HODL recommendations
        hodl_recs = [r for r in exit_strategy.all_recommendations.values() if r.action == "HODL"]
        if hodl_recs:
            display += f"\n{self.colorize('HODL Recommendations:', Colors.BOLD)}\n"
            
            # Sort by confidence
            for rec in sorted(hodl_recs, key=lambda r: r.confidence, reverse=True):
                # Confidence indicator (visual bar)
                conf_bar = "█" * int(rec.confidence * 10)
                conf_empty = "░" * (10 - int(rec.confidence * 10))
                
                display += f"  {self.colorize(rec.persona_name, Colors.BOLD)} {self.colorize(f'({rec.confidence:.2f})', rec.color_code)}:\n"
                display += f"    {self.colorize(conf_bar, rec.color_code)}{self.colorize(conf_empty, Colors.END)}\n"
                display += f"    {self.colorize('Reasons:', Colors.CYAN)} {', '.join(rec.reasons)}\n"
                display += f"    {self.colorize('Approach:', Colors.CYAN)} {rec.risk_level.capitalize()} risk, {rec.time_horizon} horizon\n"
                display += f"    {self.colorize('→', Colors.BLUE)} {rec.explanation}\n\n"
        
        # In continuous mode, add timestamp and fetch info
        if self.continuous_mode and self.last_fetch_time:
            time_str = self.last_fetch_time.strftime("%Y-%m-%d %H:%M:%S")
            display += f"\n{self.colorize(f'Last updated: {time_str}', Colors.CYAN)}\n"
        
        return display

def create_sample_positions():
    """Create sample positions for demonstration."""
    return [
        {
            'symbol': 'BTCUSDT',
            'side': 'long',
            'entry_price': 45000,
            'current_price': 47250,  # 5% profit
            'size': 0.5,
            'leverage': 10,
        },
        {
            'symbol': 'ETHUSDT',
            'side': 'long',
            'entry_price': 3000,
            'current_price': 2850,  # 5% loss
            'size': 5,
            'leverage': 10,
        },
        {
            'symbol': 'SOLUSDT',
            'side': 'short',
            'entry_price': 120,
            'current_price': 112.8,  # 6% profit
            'size': 10,
            'leverage': 5,
        },
        {
            'symbol': 'DOGEUSDT',
            'side': 'short',
            'entry_price': 0.12,
            'current_price': 0.14,  # 16.7% loss
            'size': 1000,
            'leverage': 10,
        }
    ]

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Persona-Based Exit Strategy Demo")
    
    parser.add_argument("--no-color", action="store_true",
                        help="Disable colored output")
    parser.add_argument("--min-confidence", type=float, default=0.5,
                        help="Minimum confidence for persona recommendations (default: 0.5)")
    parser.add_argument("--use-real-positions", action="store_true",
                        help="Use real BitGet positions instead of sample data")
    parser.add_argument("--continuous", action="store_true",
                        help="Enable continuous monitoring mode")
    
    return parser.parse_args()

def main():
    """Main function to run the demo."""
    args = parse_arguments()
    
    # Initialize persona exit manager
    persona_manager = PersonaExitManager(
        min_confidence=args.min_confidence,
        use_color=not args.no_color,
        continuous_mode=args.continuous
    )
    
    # Show header
    print(f"\n{Colors.BOLD}OMEGA BTC AI - Persona-Based Exit Strategy Demo{Colors.END}")
    if args.continuous:
        print(f"{Colors.CYAN}Running in continuous monitoring mode{Colors.END}")
    
    # Get positions - either from API or sample data
    if args.use_real_positions:
        result = persona_manager.get_bitget_positions()
        
        if "error" in result:
            print(f"{Colors.RED}Error fetching positions: {result['error']}{Colors.END}")
            print(f"{Colors.YELLOW}Falling back to sample positions...{Colors.END}")
            positions = create_sample_positions()
        else:
            positions = result["positions"]
            print(f"{Colors.GREEN}{result['connection']}{Colors.END}")
            print(f"{Colors.CYAN}Timestamp: {result['timestamp']}{Colors.END}")
            
            if not positions:
                print(f"{Colors.YELLOW}No active positions found. Falling back to sample positions...{Colors.END}")
                positions = create_sample_positions()
    else:
        positions = create_sample_positions()
        
        # In continuous demo mode, slightly adjust sample position prices
        # for more realistic change simulation
        if args.continuous:
            for position in positions:
                # Add a small random price change (±2%)
                current = float(position['current_price'])
                change_pct = random.uniform(-0.02, 0.02)
                position['current_price'] = current * (1 + change_pct)
    
    print(f"{Colors.CYAN}Analyzing {len(positions)} positions with {len(persona_manager.trader_personas)} trader personas{Colors.END}")
    print(f"{Colors.CYAN}Minimum confidence threshold: {args.min_confidence}{Colors.END}\n")
    
    # Analyze each position
    for position in positions:
        if not isinstance(position, dict):
            print(f"{Colors.RED}Invalid position data format{Colors.END}")
            continue
            
        # Safely access keys with proper type handling
        symbol = position.get('symbol', 'UNKNOWN')  # type: ignore
        side = position.get('side', 'long')  # type: ignore
        entry = float(position.get('entry_price', 0))  # type: ignore
        current = float(position.get('current_price', 0))  # type: ignore
        
        print(f"{Colors.BOLD}Position: {symbol} {side.upper()} @ {entry}{Colors.END}")
        print(f"Current Price: {current}")
        
        # Calculate PnL with proper float conversion
        if str(side).lower() == 'long':
            pnl_percent = ((current - entry) / entry) * 100 if entry != 0 else 0
        else:  # short
            pnl_percent = ((entry - current) / entry) * 100 if entry != 0 else 0
            
        if pnl_percent >= 0:
            pnl_color = Colors.GREEN
        else:
            pnl_color = Colors.RED
            
        print(f"PnL: {pnl_color}{pnl_percent:.2f}%{Colors.END}")
        
        # Generate exit recommendations
        exit_strategy = persona_manager.generate_exit_recommendations(position)
        
        # Display recommendations
        recommendations_display = persona_manager.format_recommendations_display(exit_strategy)
        print(recommendations_display)
        
        print(f"{Colors.YELLOW}{'=' * 80}{Colors.END}\n")
    
    print(f"{Colors.BOLD}Analysis Complete{Colors.END}")
    
    # If not in continuous mode (for use with tmux wrapper),
    # add a "press any key to exit" message
    if not args.continuous:
        print(f"{Colors.CYAN}Press Enter to exit...{Colors.END}")
        input()

if __name__ == "__main__":
    main() 