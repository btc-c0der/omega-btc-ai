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
    """Manages exit recommendations from different trader personas."""
    
    def __init__(self, min_confidence: float = 0.5, use_color: bool = True):
        """
        Initialize the persona-based exit recommendation system.
        
        Args:
            min_confidence: Minimum confidence threshold for exit recommendations
            use_color: Whether to use colored output in terminal
        """
        self.min_confidence = min_confidence
        self.use_color = use_color
        
        # Trader persona names
        self.trader_personas = ["strategic", "aggressive", "newbie", "scalper"]
        
        print(f"Initialized PersonaExitManager with {len(self.trader_personas)} trader personas")
    
    def colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.use_color:
            return f"{color}{text}{Colors.END}"
        return text
    
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
        
        # Generate recommendations from each persona
        for persona_name in self.trader_personas:
            recommendation = self._get_persona_recommendation(
                persona_name, position, current_price, entry_price, pnl_percent
            )
            if recommendation and recommendation.confidence >= self.min_confidence:
                exit_strategy.add_recommendation(recommendation)
        
        # Generate summary
        exit_strategy.generate_summary()
        return exit_strategy
    
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
    
    return parser.parse_args()

def main():
    """Main function to run the demo."""
    args = parse_arguments()
    
    # Initialize persona exit manager
    persona_manager = PersonaExitManager(
        min_confidence=args.min_confidence,
        use_color=not args.no_color
    )
    
    # Get sample positions
    sample_positions = create_sample_positions()
    
    print(f"\n{Colors.BOLD}OMEGA BTC AI - Persona-Based Exit Strategy Demo{Colors.END}")
    print(f"{Colors.CYAN}Analyzing {len(sample_positions)} positions with {len(persona_manager.trader_personas)} trader personas{Colors.END}")
    print(f"{Colors.CYAN}Minimum confidence threshold: {args.min_confidence}{Colors.END}\n")
    
    # Analyze each position
    for position in sample_positions:
        symbol = position['symbol']
        side = position['side']
        entry = position['entry_price']
        current = position['current_price']
        
        print(f"{Colors.BOLD}Position: {symbol} {side.upper()} @ {entry}{Colors.END}")
        print(f"Current Price: {current}")
        
        # Calculate PnL
        if side == 'long':
            pnl_percent = ((current - entry) / entry) * 100
        else:  # short
            pnl_percent = ((entry - current) / entry) * 100
            
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
    
    print(f"{Colors.BOLD}Demo Complete{Colors.END}")

if __name__ == "__main__":
    main() 