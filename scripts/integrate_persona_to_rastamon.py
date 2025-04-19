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
OMEGA BTC AI - Integrate Persona-Based Exit Strategies to RastaBitgetMonitor
=========================================================================

This script adds persona-based exit strategy functionality to the existing
RastaBitgetMonitor, providing personalized exit recommendations based on
different trader profiles.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import argparse
import asyncio
import signal
import logging
from typing import Dict, Any, List, Optional

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from omega_ai.exchange.bitget_client import BitGetClient
from omega_ai.trading.bitget.exit_strategy_enhancements import ExitStrategyEnhancements
from scripts.simple_bitget_positions import RastaBitgetMonitor, Colors
from scripts.integration_persona_exit_strategies import PersonaExitManager

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('persona_integration')

class PersonaEnhancedRastaBitgetMonitor(RastaBitgetMonitor):
    """
    RastaBitgetMonitor enhanced with persona-based exit recommendations.
    """
    
    def __init__(self, 
                 api_key: str, 
                 api_secret: str, 
                 passphrase: str,
                 interval: int = 5,
                 use_color: bool = True,
                 debug_mode: bool = False,
                 enable_advanced_exits: bool = True,
                 fee_coverage_threshold: float = 200.0,
                 show_complementary: bool = True,
                 show_all_fib_levels: bool = True,
                 enable_persona_exits: bool = True,
                 min_persona_confidence: float = 0.5):
        """
        Initialize the RastaBitgetMonitor with persona-based exit recommendations.
        
        Args:
            api_key: BitGet API key
            api_secret: BitGet API secret
            passphrase: BitGet API passphrase
            interval: Refresh interval in seconds
            use_color: Whether to use colored output
            debug_mode: Whether to show additional debug info
            enable_advanced_exits: Whether to enable advanced exit strategies
            fee_coverage_threshold: Minimum fee coverage percentage for exit recommendations
            show_complementary: Whether to show complementary position info
            show_all_fib_levels: Whether to show Fibonacci levels for both directions
            enable_persona_exits: Whether to enable persona-based exit recommendations
            min_persona_confidence: Minimum confidence for persona recommendations
        """
        super().__init__(
            api_key=api_key,
            api_secret=api_secret,
            passphrase=passphrase,
            interval=interval,
            use_color=use_color,
            debug_mode=debug_mode,
            enable_advanced_exits=enable_advanced_exits,
            fee_coverage_threshold=fee_coverage_threshold,
            show_complementary=show_complementary,
            show_all_fib_levels=show_all_fib_levels
        )
        
        # Persona-based exit strategy configuration
        self.enable_persona_exits = enable_persona_exits
        self.min_persona_confidence = min_persona_confidence
        
        # Initialize persona exit manager if enabled
        if self.enable_persona_exits:
            self.persona_exit_manager = PersonaExitManager(
                client=self.client,
                exit_enhancer=self.exit_enhancer,
                min_confidence=min_persona_confidence,
                use_color=use_color
            )
            logger.info(self.colorize("Persona-based exit recommendations enabled", Colors.GREEN))
    
    async def analyze_positions(self) -> Dict[str, Any]:
        """Analyze positions and generate metrics."""
        # Get base analysis from parent class
        analysis = await super().analyze_positions()
        
        # Add persona-based exit recommendations if enabled
        if self.enable_persona_exits and self.positions:
            position_analyses = analysis.get('position_analyses', {})
            
            for symbol, pos_analysis in position_analyses.items():
                position = pos_analysis['position']
                
                # Generate persona-based exit recommendations
                try:
                    persona_exit_strategy = await self.persona_exit_manager.generate_exit_recommendations(position)
                    pos_analysis['persona_recommendations'] = persona_exit_strategy
                except Exception as e:
                    logger.error(f"Error generating persona recommendations: {e}")
        
        return analysis
    
    def render_display(self, analysis: Dict[str, Any]):
        """Override render_display to add persona-based recommendations."""
        # Clear screen
        print('\033c', end='')
        
        # Display header
        self._display_header(analysis)
        
        # Display positions
        self._display_positions(analysis)
        
        # Display persona-based recommendations
        if self.enable_persona_exits:
            self._display_persona_recommendations(analysis)
        
        # Display footer
        self._display_footer()
    
    def _display_persona_recommendations(self, analysis: Dict[str, Any]):
        """Display persona-based exit recommendations."""
        position_analyses = analysis.get('position_analyses', {})
        
        if not position_analyses:
            return
        
        # Header for the persona section
        print(self.colorize("\n🧠 OMEGA PERSONA-BASED EXIT STRATEGY RECOMMENDATIONS", Colors.BOLD + Colors.PURPLE))
        print(self.colorize("════════════════════════════════════════════════════════════════════", Colors.PURPLE))
        
        for symbol, pos_analysis in position_analyses.items():
            persona_recommendations = pos_analysis.get('persona_recommendations')
            
            if persona_recommendations:
                # Show position context
                position = pos_analysis['position']
                side = position.get('side', '').lower()
                symbol = position.get('symbol', 'UNKNOWN')
                pnl_percent = persona_recommendations.pnl_percent
                
                side_display = "LONG 📈" if side == "long" else "SHORT 📉"
                side_color = Colors.GREEN if side == "long" else Colors.RED
                pnl_color = Colors.GREEN if pnl_percent >= 0 else Colors.RED
                
                print(self.colorize(f"\n{symbol} {side_color}{side_display}{Colors.END} - PnL: {pnl_color}{pnl_percent:.2f}%{Colors.END}", Colors.BOLD))
                
                # Format and display recommendations
                recommendations_display = self.persona_exit_manager.format_recommendations_display(
                    persona_recommendations
                )
                print(recommendations_display)
                
                # Separator between positions
                print(self.colorize('──────────────────────────────────────────────────────────────────────', Colors.BLUE))

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Persona-Enhanced BitGet Position Monitor")
    
    # Authentication options
    parser.add_argument("--api-key", type=str, help="BitGet API key")
    parser.add_argument("--api-secret", type=str, help="BitGet API secret")
    parser.add_argument("--passphrase", type=str, help="BitGet API passphrase")
    
    # Display options
    parser.add_argument("--interval", type=int, default=5,
                        help="Refresh interval in seconds (default: 5)")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable colored output")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode")
    
    # Exit strategy options
    parser.add_argument("--disable-advanced-exits", action="store_true",
                        help="Disable advanced exit strategies")
    parser.add_argument("--fee-coverage", type=float, default=200.0,
                        help="Minimum fee coverage percentage (default: 200.0)")
    parser.add_argument("--disable-complementary", action="store_true",
                        help="Disable complementary position recommendations")
    parser.add_argument("--disable-fib-levels", action="store_true",
                        help="Disable Fibonacci level display")
    parser.add_argument("--disable-persona-exits", action="store_true",
                        help="Disable persona-based exit recommendations")
    parser.add_argument("--min-persona-confidence", type=float, default=0.5,
                        help="Minimum confidence for persona recommendations (default: 0.5)")
    
    return parser.parse_args()

async def main(args):
    """Main function to run the persona-enhanced monitor."""
    # Get API credentials from command line args or environment
    api_key = args.api_key or os.environ.get("BITGET_API_KEY", "")
    api_secret = args.api_secret or os.environ.get("BITGET_SECRET_KEY", "")
    passphrase = args.passphrase or os.environ.get("BITGET_PASSPHRASE", "")
    
    if not all([api_key, api_secret, passphrase]):
        print("Error: API credentials are required")
        print("Please provide them as command line arguments or set environment variables:")
        print("  BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE")
        return
    
    # Initialize the persona-enhanced monitor
    monitor = PersonaEnhancedRastaBitgetMonitor(
        api_key=api_key,
        api_secret=api_secret,
        passphrase=passphrase,
        interval=args.interval,
        use_color=not args.no_color,
        debug_mode=args.debug,
        enable_advanced_exits=not args.disable_advanced_exits,
        fee_coverage_threshold=args.fee_coverage,
        show_complementary=not args.disable_complementary,
        show_all_fib_levels=not args.disable_fib_levels,
        enable_persona_exits=not args.disable_persona_exits,
        min_persona_confidence=args.min_persona_confidence
    )
    
    # Set up signal handler for clean exit
    def signal_handler(sig, frame):
        print("\nStopping monitor...")
        monitor.stop()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Display startup message
    print(f"""
{Colors.BOLD}{Colors.GREEN}OMEGA BTC AI - PERSONA-ENHANCED RASTAMON{Colors.END}
{Colors.YELLOW}Integrating Persona-Based Exit Strategies with RastaBitgetMonitor{Colors.END}
{Colors.CYAN}Starting monitor with interval: {args.interval}s | Debug: {args.debug} | Persona exits: {not args.disable_persona_exits}{Colors.END}
{Colors.PURPLE}Press Ctrl+C to exit{Colors.END}
""")
    
    # Start monitoring
    await monitor.start_monitoring()

if __name__ == "__main__":
    args = parse_arguments()
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nExiting...") 