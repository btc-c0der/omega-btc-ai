#!/usr/bin/env python3

"""
Omega Bots Bundle CLI

Command-line interface for running and managing bundled Omega trading bots.
Version: 1.0.0
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("omega_bots_bundle.cli")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Omega Bots Bundle CLI")
    
    # Main command argument
    parser.add_argument("command", choices=["run", "list", "info", "version"], 
                        help="Command to execute")
    
    # Bot selection
    parser.add_argument("--bot", "-b", type=str, default="trading_analyzer",
                        help="Bot type to run (default: trading_analyzer)")
    
    # Data options
    parser.add_argument("--data", "-d", type=str, default=None,
                        help="Path to data file (if applicable)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Path for output data (if applicable)")
    
    # Verbosity
    parser.add_argument("--verbose", "-v", action="count", default=0,
                        help="Increase verbosity (can be used multiple times)")
    
    return parser.parse_args()

def list_available_bots():
    """List all available trading bots."""
    bots = {
        "trading_analyzer": "Basic market analysis bot (v1.0.0)",
    }
    
    print("\nAvailable Omega Trading Bots:")
    print("-----------------------------")
    for bot_id, description in bots.items():
        print(f"{bot_id:20} - {description}")
    print()

async def run_trading_analyzer(args):
    """Run the trading analyzer bot."""
    from omega_bots_bundle.analyzers.trading_analyzer import TradingAnalyzerB0t
    
    analyzer = TradingAnalyzerB0t()
    logger.info(f"Initialized Trading Analyzer Bot v{analyzer.get_version()}")
    
    # Sample data for demonstration
    sample_prices = [
        9100.0, 9150.0, 9200.0, 9180.0, 9250.0, 9300.0, 9350.0, 9400.0,
        9380.0, 9350.0, 9320.0, 9280.0, 9220.0, 9150.0, 9100.0, 9050.0,
        9000.0, 8950.0, 8900.0, 8850.0, 8800.0, 8850.0, 8900.0, 8950.0,
        9000.0, 9050.0, 9100.0, 9150.0, 9200.0, 9250.0
    ]
    
    # Perform analysis
    trend = analyzer.analyze_trend(sample_prices)
    volatility = analyzer.calculate_volatility(sample_prices)
    support, resistance = analyzer.detect_support_resistance(sample_prices)
    regime = analyzer.analyze_market_regime(sample_prices)
    
    # Create market context for risk calculation
    market_context = {
        "trend": trend,
        "recent_volatility": volatility,
        "price": sample_prices[-1],
        "support": support,
        "resistance": resistance
    }
    
    risk_factor = analyzer.calculate_risk_factor(market_context)
    
    # Display results
    print("\nTrading Analyzer Results")
    print("======================")
    print(f"Current Price: ${sample_prices[-1]:.2f}")
    print(f"Market Trend: {trend}")
    print(f"Volatility: {volatility:.2f}")
    print(f"Support Level: ${support:.2f}")
    print(f"Resistance Level: ${resistance:.2f}")
    print(f"Market Regime: {regime}")
    print(f"Risk Factor: {risk_factor:.2f}")
    
    # Sample trader state
    trader_state = {"emotional_state": "neutral"}
    should_enter, direction, confidence = analyzer.should_enter_market(
        market_context, trader_state
    )
    
    print(f"Trade Signal: {'Enter' if should_enter else 'Wait'}")
    if should_enter:
        print(f"Direction: {direction.upper()}")
        print(f"Confidence: {confidence:.2f}")
    print()
    
    return True

async def run_bot(args):
    """Run the selected trading bot."""
    bot_type = args.bot.lower()
    
    if bot_type == "trading_analyzer":
        return await run_trading_analyzer(args)
    else:
        logger.error(f"Unknown bot type: {bot_type}")
        list_available_bots()
        return False

def show_version():
    """Display the version information."""
    from omega_bots_bundle import __version__
    
    print(f"\nOmega Bots Bundle v{__version__}")
    print("-------------------------")
    print("A comprehensive cryptocurrency trading bot system.")
    print("© 2023 Omega BTC AI Team\n")

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Set logging level based on verbosity
    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Process the command
    if args.command == "list":
        list_available_bots()
    elif args.command == "run":
        asyncio.run(run_bot(args))
    elif args.command == "info":
        # Display info about a specific bot
        print(f"Information about {args.bot} bot:")
        # Implementation would go here
    elif args.command == "version":
        show_version()
    else:
        logger.error(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main() 