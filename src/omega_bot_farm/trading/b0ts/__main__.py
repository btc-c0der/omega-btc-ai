#!/usr/bin/env python3

"""
Main entry point for running trading bots directly.

This file allows running bots from the command line with:
python -m src.omega_bot_farm.trading.bots
"""

import asyncio
import argparse
import logging
import os
import sys
from dotenv import load_dotenv

# Try to load environment variables from the root .env file
try:
    # First try loading from the project root
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
    env_path = os.path.join(root_dir, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment variables from {env_path}")
    else:
        print(f"No .env file found at {env_path}")
except Exception as e:
    print(f"Failed to load environment variables: {e}")

# Configure logging
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.getcwd(), "logs", "bot.log"), "a")
    ]
)

logger = logging.getLogger("bot_main")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run a trading bot")
    parser.add_argument(
        "--bot", 
        type=str, 
        default="ccxt_strategic",
        choices=["ccxt_strategic", "aggressive", "cosmic", "scalper"],
        help="Bot type to run"
    )
    parser.add_argument(
        "--symbol", 
        type=str, 
        default=os.environ.get("SYMBOL", "BTCUSDT"),
        help="Trading symbol"
    )
    parser.add_argument(
        "--interval", 
        type=int, 
        default=60,
        help="Trading cycle interval in seconds"
    )
    parser.add_argument(
        "--exchange", 
        type=str, 
        default="bitget",
        help="Exchange ID to use (default: bitget)"
    )
    return parser.parse_args()

async def run_ccxt_strategic_trader(args):
    """Run the CCXT strategic trader."""
    from src.omega_bot_farm.trading.bots.ccxt.ccxt_strategic_trader import CCXTStrategicTraderB0t
    
    logger.info(f"Starting CCXT Strategic Trader with {args.symbol} on {args.exchange}")
    
    # Create Redis client if REDIS_HOST is set
    redis_client = None
    redis_host = os.environ.get("REDIS_HOST")
    if redis_host:
        try:
            from src.omega_bot_farm.utils.redis_client import RedisClient
            redis_client = RedisClient(
                host=redis_host,
                port=int(os.environ.get("REDIS_PORT", 6379)),
                db=0
            )
            await redis_client.connect()
            logger.info(f"Connected to Redis at {redis_host}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
    
    # Initialize the trader
    trader = CCXTStrategicTraderB0t(
        name=f"CCXT_Strategic_{args.symbol}",
        exchange_id=args.exchange,
        symbol=args.symbol,
        redis_client=redis_client
    )
    
    # Start trading
    await trader.start_trading(interval_seconds=args.interval)

async def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Ensure logs directory exists
    os.makedirs(os.path.join(os.getcwd(), "logs"), exist_ok=True)
    
    logger.info(f"Starting {args.bot} bot")
    
    try:
        if args.bot == "ccxt_strategic":
            await run_ccxt_strategic_trader(args)
        else:
            logger.error(f"Bot type {args.bot} not implemented yet")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.exception(f"Bot failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 