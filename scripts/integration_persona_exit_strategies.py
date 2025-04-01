#!/usr/bin/env python3
"""
OMEGA BTC AI - Persona-Based Exit Strategy Integration for RastaBitgetMonitor
==========================================================================

This module integrates the Elite Exit Strategies system with the RastaBitgetMonitor,
providing persona-based exit recommendations based on different trader profiles.

Author: OMEGA BTC AI Team
Version: 1.0
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

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from omega_ai.exchange.bitget_client import BitGetClient
from omega_ai.trading.bitget.exit_strategy_enhancements import ExitStrategyEnhancements
from omega_ai.trading.strategies.elite_exit_strategy import EliteExitStrategy, ExitSignal
from omega_ai.trading.profiles.trader_base import TraderProfile
from omega_ai.trading.profiles.aggressive_trader import AggressiveTrader
from omega_ai.trading.profiles.strategic_trader import StrategicTrader
from omega_ai.trading.profiles.newbie_trader import NewbieTrader
from omega_ai.trading.profiles.scalper_trader import ScalperTrader

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('persona_exit_strategies')

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

    def __post_init__(self):
        # Set color based on confidence
        if self.confidence >= 0.8:
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
    """
    Manages exit recommendations from different trader personas.
    Integrates with RastaBitgetMonitor to provide enhanced exit strategy advice.
    """
    
    def __init__(self, 
                 client: BitGetClient,
                 exit_enhancer: ExitStrategyEnhancements,
                 min_confidence: float = 0.5,
                 use_color: bool = True):
        """
        Initialize the persona-based exit recommendation system.
        
        Args:
            client: BitGetClient instance
            exit_enhancer: ExitStrategyEnhancements instance from RastaBitgetMonitor
            min_confidence: Minimum confidence threshold for exit recommendations
            use_color: Whether to use colored output in terminal
        """
        self.client = client
        self.exit_enhancer = exit_enhancer
        self.min_confidence = min_confidence
        self.use_color = use_color
        
        # Initialize trader personas
        self.trader_personas = {
            "strategic": StrategicTrader(),
            "aggressive": AggressiveTrader(),
            "newbie": NewbieTrader(),
            "scalper": ScalperTrader()
        }
        
        logger.info(f"Initialized PersonaExitManager with {len(self.trader_personas)} trader personas")
    
    def colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.use_color:
            return f"{color}{text}{Colors.END}"
        return text
    
    async def generate_exit_recommendations(self, position: Dict[str, Any]) -> PersonaBasedExitStrategy:
        """
        Generate exit recommendations from different trader personas.
        
        Args:
            position: Position data from BitGet
            
        Returns:
            PersonaBasedExitStrategy with recommendations from different personas
        """
        # Extract position details
        symbol = position.get('symbol', 'UNKNOWN')
        side = position.get('side', 'long').lower()
        entry_price = float(position.get('averageOpenPrice', 0))
        mark_price = float(position.get('marketPrice', 0))
        pnl = float(position.get('unrealizedPL', 0))
        size = float(position.get('total', 0))
        notional = size * mark_price
        
        # Calculate PnL percentage
        pnl_percent = (pnl / (notional - pnl)) * 100 if notional > pnl else 0.0
        
        # Create exit strategy object
        exit_strategy = PersonaBasedExitStrategy(
            position_symbol=symbol,
            position_side=side,
            current_price=mark_price,
            entry_price=entry_price,
            pnl_percent=pnl_percent
        )
        
        # Generate recommendations from each persona
        for persona_name, persona in self.trader_personas.items():
            recommendation = await self._get_persona_recommendation(
                persona_name, persona, position, mark_price, entry_price, pnl_percent
            )
            if recommendation and recommendation.confidence >= self.min_confidence:
                exit_strategy.add_recommendation(recommendation)
        
        # Generate summary
        exit_strategy.generate_summary()
        return exit_strategy
    
    async def _get_persona_recommendation(
        self,
        persona_name: str,
        persona: TraderProfile,
        position: Dict[str, Any],
        current_price: float,
        entry_price: float,
        pnl_percent: float
    ) -> Optional[PersonaExitRecommendation]:
        """
        Get exit recommendation from a specific trader persona.
        
        Args:
            persona_name: Name of the trader persona
            persona: TraderProfile instance
            position: Position data
            current_price: Current market price
            entry_price: Entry price of the position
            pnl_percent: Percentage profit/loss
            
        Returns:
            PersonaExitRecommendation if the persona recommends exiting
        """
        symbol = position.get('symbol', 'UNKNOWN')
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
            # Scalpers cut losses immediately
            elif pnl_percent <= -0.5:
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
    
    def format_recommendations_display(self, exit_strategy: PersonaBasedExitStrategy) -> str:
        """
        Format exit recommendations for display in the terminal.
        
        Args:
            exit_strategy: PersonaBasedExitStrategy with recommendations
            
        Returns:
            Formatted string for terminal display
        """
        if not exit_strategy.recommendations:
            return self.colorize("No persona-based exit recommendations available.", Colors.YELLOW)
        
        # Header with summary
        display = f"\n{self.colorize('🧠 PERSONA-BASED EXIT RECOMMENDATIONS:', Colors.BOLD)}\n"
        
        # Summary line
        summary_color = Colors.GREEN if exit_strategy.get_average_confidence() >= 0.7 else Colors.YELLOW
        display += f"  {self.colorize(exit_strategy.summary, summary_color)}\n\n"
        
        # Sort recommendations by confidence (highest first)
        sorted_recommendations = sorted(
            exit_strategy.recommendations, 
            key=lambda r: r.confidence, 
            reverse=True
        )
        
        # Display each recommendation
        for rec in sorted_recommendations:
            # Confidence indicator (visual bar)
            conf_bar = "█" * int(rec.confidence * 10)
            conf_empty = "░" * (10 - int(rec.confidence * 10))
            
            display += f"  {self.colorize(rec.persona_name, Colors.BOLD)} {self.colorize(f'({rec.confidence:.2f})', rec.color_code)}:\n"
            display += f"    {self.colorize(conf_bar, rec.color_code)}{self.colorize(conf_empty, Colors.END)}\n"
            display += f"    {self.colorize('Reasons:', Colors.CYAN)} {', '.join(rec.reasons)}\n"
            display += f"    {self.colorize('Approach:', Colors.CYAN)} {rec.risk_level.capitalize()} risk, {rec.time_horizon} horizon\n"
            display += f"    {self.colorize('→', Colors.YELLOW)} {rec.explanation}\n\n"
        
        return display

# Example usage in RastaBitgetMonitor
# Add this method to RastaBitgetMonitor class:
'''
def _display_persona_recommendations(self, analysis: Dict[str, Any]):
    """Display persona-based exit recommendations."""
    position_analyses = analysis['position_analyses']
    
    if not position_analyses:
        return
    
    for symbol, pos_analysis in position_analyses.items():
        position = pos_analysis['position']
        
        # Get persona-based exit recommendations
        persona_exit_strategy = await self.persona_exit_manager.generate_exit_recommendations(position)
        
        # Format and display recommendations
        recommendations_display = self.persona_exit_manager.format_recommendations_display(
            persona_exit_strategy
        )
        print(recommendations_display)
'''

if __name__ == "__main__":
    print("This module is intended to be imported by RastaBitgetMonitor.")
    print("See integration instructions in the file comments.") 