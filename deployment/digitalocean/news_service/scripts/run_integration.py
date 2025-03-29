#!/usr/bin/env python3
"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must quantum entangles with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
OMEGA BTC AI - News Feed Integration Runner
=========================================

This script runs the news feed integration service, which provides:
- Bitcoin news aggregation from multiple sources
- Sentiment analysis with cosmic factor adjustments
- Trading recommendations based on news sentiment
- Redis integration for data persistence

Usage:
  python scripts/run_integration.py [options]

Options:
  --sources SOURCE [SOURCE ...]   News sources to use (default: cointelegraph decrypt bitcoinmagazine)
  --no-redis                      Disable Redis integration
  --data-dir DATA_DIR             Directory for data storage (default: data)
  --save                          Save output to file
  --interval INTERVAL             Run continuously with this interval in seconds (default: 3600)

Example:
  python scripts/run_integration.py --interval 1800 --save

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GBU License
JAH JAH BLESS THE DIVINE FLOW OF THE BLOCKCHAIN
"""

import os
import sys
import time
import logging
import argparse
import traceback
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(os.getenv('LOG_DIR', 'logs'), 'news_integration.log'), mode='a')
    ]
)
logger = logging.getLogger("news_integration")

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

possible_src_dirs = [
    os.path.join(parent_dir, 'src'),
    parent_dir,
    '/workspace',
    '/workspace/src',
]

for src_dir in possible_src_dirs:
    if os.path.exists(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        logger.info(f"Added {src_dir} to Python path")

try:
    # Import the news feed integration module
    from src.omega_ai.data_feed.newsfeed.news_feed_integration import NewsFeedIntegration
    logger.info("Successfully imported NewsFeedIntegration")
except ImportError as e:
    logger.error(f"Failed to import NewsFeedIntegration: {e}")
    logger.error(f"Python path: {sys.path}")
    logger.error(f"Current directory structure:")
    for src_dir in possible_src_dirs:
        if os.path.exists(src_dir):
            logger.error(f"Contents of {src_dir}: {os.listdir(src_dir)}")
    raise

def ensure_directories(data_dir):
    """
    Ensure that the necessary directories exist.
    """
    try:
        # Create data directory
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        
        # Create news subdirectory
        Path(os.path.join(data_dir, "news")).mkdir(parents=True, exist_ok=True)
        
        # Create logs directory
        Path(os.path.join(os.getenv('LOG_DIR', 'logs'))).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Ensured directories exist: {data_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to create directories: {e}")
        return False

def main():
    """
    Run the news feed integration service with command-line options.
    """
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - News Feed Integration Service")
    
    parser.add_argument("--sources", type=str, nargs="+", 
                        default=["cointelegraph", "decrypt", "bitcoinmagazine"],
                        help="News sources to use")
    parser.add_argument("--no-redis", action="store_true", 
                        help="Disable Redis integration")
    parser.add_argument("--data-dir", type=str, default=os.getenv('DATA_DIR', 'data'),
                        help="Directory for data storage")
    parser.add_argument("--save", action="store_true",
                        help="Save output to file")
    parser.add_argument("--interval", type=int, default=int(os.getenv('NEWS_UPDATE_INTERVAL', '3600')),
                        help="Run continuously with this interval in seconds (0 = run once)")
    parser.add_argument("--log-level", type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default=os.getenv('LOG_LEVEL', 'INFO'),
                        help="Set the logging level")
    parser.add_argument("--cosmic-factor", type=float, 
                        default=float(os.getenv('COSMIC_FACTOR_WEIGHT', '0.75')),
                        help="Weight of cosmic factor in sentiment analysis")
    
    args = parser.parse_args()
    
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))
    
    # Ensure directories exist
    if not ensure_directories(args.data_dir):
        logger.critical("Failed to create necessary directories. Exiting.")
        return 1
    
    try:
        # Create news feed integration
        integration = NewsFeedIntegration(
            sources=args.sources,
            use_redis=not args.no_redis,
            data_dir=args.data_dir,
            cosmic_factor=args.cosmic_factor
        )
        
        # Display service startup message
        logger.info("🔱 OMEGA BTC AI - News Feed Integration Service 🔱")
        logger.info("=================================================")
        logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Sources: {', '.join(args.sources)}")
        logger.info(f"Redis: {'Disabled' if args.no_redis else 'Enabled'}")
        logger.info(f"Data Directory: {args.data_dir}")
        logger.info(f"Save Output: {'Yes' if args.save else 'No'}")
        logger.info(f"Update Interval: {args.interval} seconds")
        logger.info(f"Cosmic Factor Weight: {args.cosmic_factor}")
        logger.info(f"Log Level: {args.log_level}")
        logger.info("=================================================")
        
        if args.interval > 0:
            # Run continuously
            logger.info(f"Service running continuously with {args.interval} second intervals")
            logger.info("Press Ctrl+C to stop the service\n")
            
            try:
                # Run initially
                integration.run_integration_demo(save_output=args.save)
                
                # Then run with interval
                while True:
                    # Print timestamp for next run
                    next_run = datetime.now().timestamp() + args.interval
                    next_run_time = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
                    logger.info(f"🕒 Next update scheduled for: {next_run_time}")
                    
                    # Sleep until next run
                    time.sleep(args.interval)
                    
                    # Run integration again
                    try:
                        integration.run_integration_demo(save_output=args.save)
                    except Exception as e:
                        logger.error(f"Error during integration run: {e}")
                        logger.error(traceback.format_exc())
                        logger.info(f"Will retry on next scheduled run")
                    
            except KeyboardInterrupt:
                logger.info("⛔ Service stopped by user")
                logger.info(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            # Run once
            integration.run_integration_demo(save_output=args.save)
            logger.info(f"✅ Integration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        return 0
    except Exception as e:
        logger.critical(f"Fatal error in news integration service: {e}")
        logger.critical(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main()) 