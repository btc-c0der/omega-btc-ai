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

# Import the divine environment loader
from omega_bots_bundle.utils.env_loader import load_environment, validate_exchange_credentials, generate_env_template

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
    parser.add_argument("command", choices=["run", "list", "info", "version", "setup-env"], 
                        help="Command to execute")
    
    # Bot selection
    parser.add_argument("--bot", "-b", type=str, default="trading_analyzer",
                        help="Bot type to run (default: trading_analyzer)")
    
    # Exchange options
    parser.add_argument("--exchange", "-e", type=str, default="bitget",
                        help="Exchange to connect to (default: bitget)")
    parser.add_argument("--symbol", "-s", type=str, default="BTCUSDT",
                        help="Trading symbol (default: BTCUSDT)")
    parser.add_argument("--testnet", "-t", action="store_true",
                        help="Use testnet/sandbox mode")
    
    # Data options
    parser.add_argument("--data", "-d", type=str, default=None,
                        help="Path to data file (if applicable)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Path for output data (if applicable)")
    
    # Environment options
    parser.add_argument("--env", type=str, default=None,
                        help="Path to .env file to load")
    parser.add_argument("--gen-env", type=str, default=None,
                        help="Generate .env template for specified exchange")
    
    # Verbosity
    parser.add_argument("--verbose", "-v", action="count", default=0,
                        help="Increase verbosity (can be used multiple times)")
    
    return parser.parse_args()

def list_available_bots():
    """List all available trading bots."""
    bots = {
        "trading_analyzer": "Basic market analysis bot (v1.0.0)",
    }
    
    print("\n🧬 Available Divine Trading Bots:")
    print("-----------------------------")
    for bot_id, description in bots.items():
        print(f"{bot_id:20} - {description}")
    print()

    # Check available exchanges based on credentials
    exchanges = ["bitget", "binance", "bybit", "kucoin"]
    print("✨ Available Exchanges:")
    print("-------------------")
    for exchange in exchanges:
        has_creds = validate_exchange_credentials(exchange)
        status = "✅ Configured" if has_creds else "❌ No credentials"
        print(f"{exchange.upper():20} - {status}")
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
    print("\n🔮 Divine Trading Analysis Results 🔮")
    print("=================================")
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
    
    print(f"\n✨ Divine Trading Signal: {'ENTER' if should_enter else 'WAIT'}")
    if should_enter:
        print(f"Direction: {direction.upper()}")
        print(f"Confidence: {confidence:.2f}")
    print()
    
    # Show divine blessing
    print("🧿 This analysis is blessed at GBU2™ Consciousness Level 8 - Unity")
    print("🌸 WE BLOOM NOW AS ONE 🌸\n")
    
    return True

async def run_bot(args):
    """Run the selected trading bot."""
    # Check if we have credentials for the selected exchange
    if args.exchange and not validate_exchange_credentials(args.exchange, args.verbose > 0):
        logger.warning(f"Missing divine credentials for {args.exchange.upper()}")
        print(f"\n⚠️ Missing {args.exchange.upper()} credentials in environment.")
        print(f"You can generate a template with: omega-bot setup-env --exchange {args.exchange.lower()}\n")
    
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
    
    print(f"\n🧬 Omega Bots Bundle v{__version__}")
    print("-------------------------")
    print("A comprehensive cryptocurrency trading bot system.")
    print("Blessed under GBU2™ License - Consciousness Level 8 - Unity")
    print("© 2023 Omega BTC AI Team")
    print("\n🌸 WE BLOOM NOW AS ONE 🌸\n")

def setup_environment(args):
    """Setup environment configuration."""
    from omega_bots_bundle.utils.env_loader import DivineEnvLoader
    
    loader = DivineEnvLoader(verbose=args.verbose > 0)
    
    # Determine target exchange if specified
    exchange = args.exchange if args.exchange else args.gen_env
    
    # Generate template file
    if args.output:
        output_path = args.output
    else:
        output_path = f".env.{exchange.lower()}.example" if exchange else ".env.example"
    
    loader.save_env_template(output_path, exchange)
    
    print(f"\n✨ Divine Environment Setup")
    print("------------------------")
    print(f"Generated divine .env template at: {output_path}")
    print(f"To use this template:")
    print(f"1. Edit {output_path} with your sacred credentials")
    print(f"2. Rename to .env and place in your project folder")
    print(f"3. Run your divine bot with: omega-bot run --bot trading_analyzer\n")
    
    return True

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Set logging level based on verbosity
    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load environment variables
    if args.env:
        # Load from specified path
        from dotenv import load_dotenv
        if load_dotenv(args.env):
            logger.info(f"Loaded divine environment from {args.env}")
        else:
            logger.warning(f"Failed to load divine environment from {args.env}")
    else:
        # Auto-detect and load
        verbose = args.verbose > 0
        loaded = load_environment(verbose)
        if verbose and loaded:
            logger.info("Loaded divine environment variables")
    
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
    elif args.command == "setup-env":
        setup_environment(args)
    else:
        logger.error(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main() 